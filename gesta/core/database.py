# =============================================================================
# database.py
# =============================================================================
# Maneja la conexión a la base de datos. Crea el engine (el objeto que sabe
# hablar con SQLite o PostgreSQL), inicializa las tablas, y provee un context
# manager (get_session) que abre una sesión, hace commit si todo sale bien, o
# rollback si algo falla. Todo el código que necesite tocar la BD pasa por aquí.
# =============================================================================


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator

from gesta.core.entities import Base


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

def create_db_engine(db_url: str, echo: bool = False):
    """
    Crea el engine de SQLAlchemy.

    db_url ejemplos:
        SQLite  → "sqlite:///mi_negocio.db"
        SQLite  → "sqlite:///:memory:"   (para tests)
        Postgres → "postgresql://user:pass@localhost/gesta"

    echo=True imprime el SQL generado — útil durante desarrollo.
    """
    connect_args = {}

    if db_url.startswith("sqlite"):
        # SQLite necesita este flag para funcionar correctamente
        # con múltiples threads (ej. en un servidor web futuro)
        connect_args["check_same_thread"] = False

    engine = create_engine(
        db_url,
        echo=echo,
        connect_args=connect_args,
    )
    return engine


# ---------------------------------------------------------------------------
# Tablas
# ---------------------------------------------------------------------------

def init_db(engine) -> None:
    """
    Crea todas las tablas en la base de datos si no existen.
    Es seguro llamarlo múltiples veces — no destruye datos existentes.
    """
    Base.metadata.create_all(engine)


def drop_db(engine) -> None:
    """
    Elimina todas las tablas. Úsese solo en tests o desarrollo.
    NUNCA en producción.
    """
    Base.metadata.drop_all(engine)


# ---------------------------------------------------------------------------
# Sesión
# ---------------------------------------------------------------------------

def create_session_factory(engine) -> sessionmaker:
    """
    Retorna una fábrica de sesiones ligada al engine dado.
    """
    return sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,  # los objetos siguen accesibles después del commit
    )


@contextmanager
def get_session(session_factory: sessionmaker) -> Generator[Session, None, None]:
    """
    Context manager que provee una sesión con manejo automático
    de commit y rollback.

    Uso:
        with get_session(session_factory) as session:
            session.add(persona)
    """
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ---------------------------------------------------------------------------
# Healthcheck
# ---------------------------------------------------------------------------

def check_connection(engine) -> bool:
    """
    Verifica que la base de datos sea accesible.
    Retorna True si la conexión es exitosa, False si falla.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False