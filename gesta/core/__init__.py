# =============================================================================
# __init__.py
# =============================================================================
# Expone la API pública del módulo core. Permite importar directamente desde
# gesta.core en lugar de tener que conocer en qué archivo vive cada clase.
#
#   from gesta.core import Person, Appointment, Transaction
# =============================================================================

from gesta.core.entities import (
    Base,
    Person,
    Role,
    Offering,
    Service,
    Product,
    Appointment,
    Transaction,
    Payment,
    PaymentMethod,
    AppointmentStatus,
    TransactionStatus,
    OfferingType,
)

from gesta.core.database import (
    init_db,
    check_connection,
)

from gesta.core.exceptions import (
    GestaError,
    ValidationError,
    AppointmentConflictError,
    NotFoundError,
    DuplicateError,
    BusinessRuleError,
    UnpaidTransactionError,
    InactiveOfferingError,
    NoProviderError,
    InvalidRoleError,
    DatabaseError,
)

__all__ = [
    # Entidades
    "Base",
    "Person",
    "Role",
    "Offering",
    "Service",
    "Product",
    "Appointment",
    "Transaction",
    "Payment",
    # Enums
    "PaymentMethod",
    "AppointmentStatus",
    "TransactionStatus",
    "OfferingType",
    # Base de datos (uso común)
    "init_db",
    "check_connection",
    # Excepciones
    "GestaError",
    "ValidationError",
    "AppointmentConflictError",
    "NotFoundError",
    "DuplicateError",
    "BusinessRuleError",
    "UnpaidTransactionError",
    "InactiveOfferingError",
    "NoProviderError",
    "InvalidRoleError",
    "DatabaseError",
]