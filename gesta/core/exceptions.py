# =============================================================================
# exceptions.py
# =============================================================================
# Define la jerarquía de errores propios de Gesta. En lugar de dejar que
# SQLAlchemy o Python lancen errores genéricos, los managers atrapan esos
# errores y lanzan excepciones de Gesta con mensajes claros y contexto de
# negocio. Permite que el usuario de la librería maneje errores sin depender
# de los internos de SQLAlchemy.
# =============================================================================


class GestaError(Exception):
    """Base de todos los errores de Gesta."""
    pass


# ---------------------------------------------------------------------------
# Validación
# ---------------------------------------------------------------------------

class ValidationError(GestaError):
    """
    Datos inválidos antes de tocar la base de datos.
    Ejemplos: precio negativo, fecha en el pasado, campo requerido vacío.
    """
    pass


class AppointmentConflictError(ValidationError):
    """
    Traslape de horarios — el proveedor ya tiene una cita
    en el rango de fecha/hora solicitado.
    """
    pass


# ---------------------------------------------------------------------------
# Búsqueda
# ---------------------------------------------------------------------------

class NotFoundError(GestaError):
    """
    La entidad solicitada no existe en la base de datos.
    Ejemplo: buscar un cliente por ID que no existe.
    """
    def __init__(self, entity: str, identifier: str):
        super().__init__(f"{entity} no encontrado: {identifier!r}")
        self.entity     = entity
        self.identifier = identifier


# ---------------------------------------------------------------------------
# Unicidad
# ---------------------------------------------------------------------------

class DuplicateError(GestaError):
    """
    Violación de unicidad — se intenta crear un registro
    que ya existe. Ejemplo: email duplicado en persons.
    """
    def __init__(self, entity: str, field: str, value: str):
        super().__init__(f"Ya existe un {entity} con {field}={value!r}")
        self.entity = entity
        self.field  = field
        self.value  = value


# ---------------------------------------------------------------------------
# Reglas de negocio
# ---------------------------------------------------------------------------

class BusinessRuleError(GestaError):
    """
    Violación de una regla de negocio.
    Base para errores semánticos que van más allá de la validación de datos.
    """
    pass


class UnpaidTransactionError(BusinessRuleError):
    """
    Se intenta realizar una operación que requiere que la
    transacción esté saldada, pero tiene balance pendiente.
    """
    def __init__(self, transaction_id: str, balance):
        super().__init__(
            f"La transacción {transaction_id!r} tiene un balance pendiente de {balance}"
        )
        self.transaction_id = transaction_id
        self.balance        = balance


class InactiveOfferingError(BusinessRuleError):
    """
    Se intenta agendar o vender un servicio/producto
    que está marcado como inactivo.
    """
    def __init__(self, offering_name: str):
        super().__init__(f"El offering {offering_name!r} no está activo")
        self.offering_name = offering_name


class NoProviderError(BusinessRuleError):
    """
    Se intenta agendar un servicio que requiere proveedor
    sin asignar ninguno.
    """
    def __init__(self, service_name: str):
        super().__init__(
            f"El servicio {service_name!r} requiere al menos un proveedor asignado"
        )
        self.service_name = service_name


class InvalidRoleError(BusinessRuleError):
    """
    Se asigna una persona a un rol que no le corresponde.
    Ejemplo: registrar como proveedor a alguien sin rol is_provider=True.
    """
    def __init__(self, person_name: str, role: str):
        super().__init__(
            f"{person_name!r} no tiene el rol requerido: {role!r}"
        )
        self.person_name = person_name
        self.role        = role


# ---------------------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------------------

class DatabaseError(GestaError):
    """
    Error de conexión o de operación en la base de datos.
    Envuelve excepciones de SQLAlchemy para no exponerlas directamente.
    """
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error