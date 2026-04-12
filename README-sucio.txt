Clases principales:
1. Person          → cualquier participante (cliente, colaborador, etc.)
2. Role            → qué papel juega una Person en el negocio
3. Offering        → abstracta: lo que el negocio ofrece
   ├── Service     → oferta que requiere agenda y proveedor
   └── Product     → oferta física con inventario
4. Appointment     → reserva futura de un Service
5. Transaction     → hecho consumado: qué se entregó, a quién, cuándo
6. Payment         → movimiento de dinero ligado a una Transaction
7. Gesta           → clase principal que orquesta todo


Person ──────────────────────────────┐
                                     ▼
Service ──────► Appointment ──────► Transaction ──────► Payment
                    │
                    └── fecha de cita (≠ fecha de registro)
