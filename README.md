<<<<<<< HEAD
# Pharmacy Warehouse Management System (Django)

Features:
- Login / Logout / Signup (user management)
- Medicine master with dosage form, strength, barcode
- Batches with Lot, MFG Date, EXP Date, Location, Quantity, Unit Price
- Dashboard with KPIs, **expiry alerts**, **low stock**, recent movements
- Search and filter for medicines and batches
- Locations (warehouse/aisle/shelf/bin)
- Addresses (shipping/receiving parties)
- Inbound/Outbound **Stock Movements** with references and counterparties
- Admin panel for advanced management

## Quick Start

```bash
# 1) Create virtual env (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Initialize DB
python manage.py migrate

# 4) Create a superuser for admin
python manage.py createsuperuser

# 5) Run the server
python manage.py runserver 0.0.0.0:8000
```

Open http://localhost:8000 for the app, and http://localhost:8000/admin for admin.

## Usage Tips
- Create a few **Locations** (admin or UI) like `Main Warehouse / A1 / S1 / B1`
- Add **Medicines**, then **Batches** (with MFG/EXP/Qty/Location)
- Use **Stock Movements** to receive more stock (`IN`) or ship out (`OUT`). Quantities automatically adjust the batch.
- The **Dashboard** warns about **expiring** and **low stock** items.

## Notes
- FEFO (first-expiry-first-out) can be added by auto-selecting the earliest `exp_date` batch for `OUT` moves.
- For production, switch to PostgreSQL, add proper logging, audit trails, and background emails/SMS for alerts.
=======
# pharmacy_warehouse_management_system
Django-based Pharmacy Warehouse Management System with login/signup, dashboard, expiry alerts, low-stock tracking, medicine &amp; batch management, stock movement, and shipping details. Built with Django, SQLite, Bootstrap, and includes an admin panel for full inventory control.
>>>>>>> a57b823eb31805198706f13728b3d815e639b018
