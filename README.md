# Gesta

A Python library for business administration — appointments, transactions, payments, and reporting in a clean, extensible API.

---

## Features

- **Appointment management** — book, reschedule, cancel, and complete appointments with conflict detection
- **Transaction tracking** — register services rendered and products sold, with cost and profit tracking
- **Payment management** — register payments against one or multiple transactions, including partial payments and refunds
- **Reporting** — revenue summaries, profit margins, popular offerings, frequent clients, and more
- **Extensible** — adapt Gesta to any business type by extending the base `Gesta` class
- **SQLite & PostgreSQL** — works locally out of the box, ready for production with Postgres

---

## Installation

```bash
pip install gesta
```

Requires Python 3.12+.

---

## Quick start

```python
from datetime import datetime, timedelta
from gesta.extensions import WellnessStudio

# Initialize — creates the database and tables automatically
studio = WellnessStudio(db_url="sqlite:///my_business.db")
studio.setup()

# Register a client and a provider
with studio.session() as s:
    client    = studio.add_client(s, name="Ana García",  phone="5551234567")
    therapist = studio.add_provider(s, name="Marta López", role="therapist")

# Book an appointment
with studio.session() as s:
    ana   = studio.list_clients(s)[0]
    marta = studio.list_providers(s)[0]

    appointment = studio.appointments(s).book(
        service_id   = "svc_masaje_sueco",
        client_ids   = [ana.id],
        provider_ids = [marta.id],
        scheduled_at = datetime.now() + timedelta(days=3),
    )

# Register the transaction when the service is delivered
with studio.session() as s:
    tx = studio.transactions(s).register_from_appointment(
        appointment_id = appointment.id,
        occurred_at    = datetime.now(),
    )

# Register payment
with studio.session() as s:
    from gesta.core.entities import PaymentMethod
    studio.payments(s).register(
        transaction_ids = [tx.id],
        amount          = tx.amount,
        method          = PaymentMethod.CASH,
        paid_at         = datetime.now(),
    )

# Monthly revenue report
with studio.session() as s:
    summary = studio.reports(s).monthly_summary(
        year  = datetime.now().year,
        month = datetime.now().month,
    )
    print(f"Revenue:   ${summary.total_revenue}")
    print(f"Collected: ${summary.total_collected}")
    print(f"Profit:    ${summary.total_profit}")
    print(f"Margin:    {summary.profit_margin}%")
```

---

## Core concepts

### Entities

| Entity | Description |
|---|---|
| `Person` | Any participant — client, therapist, instructor, etc. |
| `Role` | What role a person plays (`is_provider`, `is_recipient`) |
| `Service` | An offering that requires scheduling and a provider |
| `Product` | A physical offering with inventory |
| `Appointment` | A future reservation of a service |
| `Transaction` | A record that a service was delivered or a product was sold |
| `Payment` | A money movement linked to one or more transactions |

### Transaction vs Appointment

These are two distinct events in time:

```
Monday 10am  →  Ana books a massage for Thursday     =  Appointment
Thursday 3pm →  Marta gives Ana the massage           =  Transaction
Thursday 3pm →  Ana pays $600 cash                   =  Payment (direct)

— or —

Thursday 3pm →  Ana doesn't pay that day             =  Payment pending
Friday 11am  →  Ana transfers $600                   =  Payment (indirect)
```

### Price, cost, and profit

Every `Service` and `Product` has:
- `price` — what the client pays (per person / per unit)
- `cost`  — what it costs the business to deliver
- `margin` — `price - cost` (property, computed automatically)

Every `Transaction` tracks:
- `amount` — total charged (`price × number of clients`)
- `cost_amount` — actual cost at the time of the transaction
- `profit` — `amount - cost_amount` (property)

---

## Extending Gesta

Gesta is designed to adapt to any appointment-based business. Create your own extension by subclassing `Gesta`:

```python
from gesta import Gesta
from gesta.core.entities import Role

class HairSalon(Gesta):
    def setup(self):
        with self.session() as s:
            roles = [
                Role(id="role_client",  name="client",  is_recipient=True,  is_provider=False),
                Role(id="role_stylist", name="stylist", is_recipient=False, is_provider=True),
            ]
            for role in roles:
                if not s.get(Role, role.id):
                    s.add(role)

salon = HairSalon(db_url="sqlite:///salon.db")
salon.setup()
```

---

## Using with PostgreSQL

```python
studio = WellnessStudio(
    db_url="postgresql://user:password@localhost/gesta_db"
)
```

Install the PostgreSQL driver:

```bash
pip install psycopg2-binary
```

---

## Running tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Project structure

```
gesta/
├── gesta/
│   ├── __init__.py
│   ├── gesta.py                # Main Gesta class
│   ├── core/
│   │   ├── entities.py         # Person, Role, Offering, Appointment, Transaction, Payment
│   │   ├── database.py         # Engine, session, init_db
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── validators.py       # Reusable validation functions
│   ├── managers/
│   │   ├── calendar.py         # AppointmentManager
│   │   ├── transactions.py     # TransactionManager, PaymentManager
│   │   └── reports.py          # ReportManager
│   └── extensions/
│       └── wellness.py         # WellnessStudio — example extension
├── tests/
├── scripts/
│   └── demo.py
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## License

GNU Affero General Public License v3.0 — see [LICENSE](LICENSE) for details.