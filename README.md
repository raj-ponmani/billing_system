# 🧾 Billing System - FastAPI (async) + Postgres + Jinja & Invoice System with Email Notifications

A complete FastAPI-based billing system that:
- Records purchase details with tax calculations.
- Generates a customer invoice page.
- Sends an invoice email (with HTML + plain text versions).
- Displays a summary with purchase breakdown.

---

## 🚀 Features
- **Purchase Table**: Shows product name, quantity, purchase price, tax %, tax payable, and total item price.
- **Summary**: Displays totals, net price, tax payable, balance, and denominations.
- **Email Invoice**: Sends a fully formatted HTML invoice.
- **Reusable Calculation Utils**: All calculations are done in a central utility function for consistency.
- **Async Architecture**: Non-blocking email sending & DB queries.

---

## 📂 Project Structure

- .
- ├── app/
- │ ├── main.py # FastAPI entry point
- │ ├── crud.py # CRUD helper functions
- │ ├── database.py # Initiate DB connection
- │ ├── models.py # ORM models
- │ ├── schemas.py # Pydantic models
- │ ├── routes/
- │ │ ├── billing.py # Routes for bill generation & email sending
- │ │ ├── purchases.py # Routes for list purchase & view details
- │ ├── templates/
- │ │ ├── invoice.html # Email template
- │ │ ├── bill_result.html # List customer purchases
- │ │ ├── billing_form.html # Billing page
- │ │ ├── purchase_detail.html # Purchase details page
- │ └── static/ # CSS, JS, assets
- ├── schema.sql # DB schema
- ├── requirements.txt # Python dependencies
- ├── .env.example # Environment variables template
- └── README.md # This file

## Requirements
- Python 3.10<= to <=3.12  (recommended)
- PostgreSQL

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/billing-invoice-system.git
cd billing-invoice-system


1. Clone/copy this project directory.

```

### 2️⃣ Create a Python venv & install deps:

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```
### 3️⃣ Setup Environment Variables
Create a .env file in the project root:
```dtd
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
BREVO_API_KEY=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
```

- For email sending I've integrated Brevo so please use the same API key I provided here.

### 4️⃣ Setup Database

```bash
psql -U youruser -d yourdb -f schema.sql
```

### 5️⃣ Run Application

```bash
uvicorn app.main:app --reload
```
Visit: http://127.0.0.1:8000

### 🧮 Calculation Logic

All totals, tax amounts, and balance calculations are handled in utils.py and reused in:
- Bill generation route 
- Purchase display route

- Example output:
```yaml
Total without tax: ₹1000
Total tax payable: ₹180
Net price: ₹1180
Rounded net price: ₹1180
Paid amount: ₹1200
Balance payable: ₹20
Denominations: {10: 2}
```
