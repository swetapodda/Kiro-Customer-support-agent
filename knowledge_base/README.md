# Knowledge Base

This folder contains the mock databases used by the Credit Card Customer Support Agent.

## Structure

```
knowledge_base/
├── __init__.py           # Package initialization
├── customers.py          # Customer database
├── transactions.py       # Transaction database
└── README.md            # This file
```

## Files

### customers.py

**Purpose**: Customer identity verification

**Data Structure**:
```python
{
    "mobile_last4": {
        "customer_id": str,
        "name": str,
        "card_id": str,
        "mobile": str,
        "last_4": str,
        "email": str,
        "account_status": str,
        "member_since": str
    }
}
```

**Functions**:
- `get_customer(mobile, last4)` - Retrieve customer by credentials
- `list_all_customers()` - Get all customers (for testing)

**Test Data**:
- Customer 1: John Doe (9876543210/1234)
- Customer 2: Jane Smith (9998887776/5678)

---

### transactions.py

**Purpose**: Transaction history and fraud detection

**Data Structure**:
```python
{
    "customer_id": [
        {
            "transaction_id": str,
            "date": str,
            "amount": float,
            "merchant": str,
            "merchant_category": str,
            "status": str,
            "location": str,
            "card_last_4": str,
            "fraud_score": float (optional)
        }
    ]
}
```

**Functions**:
- `get_transactions(customer_id, limit)` - Get recent transactions
- `get_transaction_by_id(transaction_id)` - Get specific transaction
- `get_suspicious_transactions(customer_id)` - Get high-risk transactions

**Test Data**:
- CUST001: 3 transactions (including $8900 suspicious one)
- CUST002: 2 transactions (all legitimate)

---

## Usage

### Import in Python

```python
from knowledge_base import get_customer, get_transactions

# Verify customer
customer = get_customer("9876543210", "1234")
if customer:
    print(f"Welcome, {customer['name']}")
    
    # Get transactions
    transactions = get_transactions(customer['customer_id'])
    for trans in transactions:
        print(f"{trans['date']}: ${trans['amount']} at {trans['merchant']}")
```

### Used By

- `tools.py` - Imports and uses these databases
- `agent_nodes.py` - Indirectly through tools
- `main.py` - Demo scenarios use this data

---

## Production Migration

To migrate to production databases:

### 1. Customer Database

Replace `customers.py` with database queries:

```python
import psycopg2

def get_customer(mobile, last4):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM customers WHERE mobile = %s AND last_4 = %s",
        (mobile, last4)
    )
    result = cursor.fetchone()
    conn.close()
    return result
```

### 2. Transaction Database

Replace `transactions.py` with database queries:

```python
def get_transactions(customer_id, limit=5):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM transactions WHERE customer_id = %s ORDER BY date DESC LIMIT %s",
        (customer_id, limit)
    )
    results = cursor.fetchall()
    conn.close()
    return results
```

---

## Security Notes

⚠️ **Important**: This is mock data for demonstration purposes only.

In production:
- ✅ Use encrypted database connections
- ✅ Implement proper authentication
- ✅ Add rate limiting
- ✅ Log all access attempts
- ✅ Mask sensitive data
- ✅ Follow PCI-DSS compliance
- ✅ Implement data retention policies

---

## Adding New Data

### Add a New Customer

Edit `customers.py`:

```python
CUSTOMER_DB["1234567890_9999"] = {
    "customer_id": "CUST003",
    "name": "New Customer",
    "card_id": "CARD_9999",
    "mobile": "1234567890",
    "last_4": "9999",
    "email": "new@example.com",
    "account_status": "active",
    "member_since": "2026-01-01"
}
```

### Add Transactions

Edit `transactions.py`:

```python
TRANSACTIONS_DB["CUST003"] = [
    {
        "transaction_id": "TXN006",
        "date": "2026-01-25",
        "amount": 500.00,
        "merchant": "Target",
        "merchant_category": "Retail",
        "status": "completed",
        "location": "Chicago, IL",
        "card_last_4": "9999"
    }
]
```

---

## Testing

Test the knowledge base:

```bash
python -c "from knowledge_base import get_customer, get_transactions; print(get_customer('9876543210', '1234'))"
```

Expected output:
```python
{
    'customer_id': 'CUST001',
    'name': 'John Doe',
    ...
}
```

---

## Statistics

- **Total Customers**: 2
- **Total Transactions**: 5
- **Suspicious Transactions**: 1 (CUST001, $8900)
- **Average Transaction**: $2,610.10
- **Date Range**: 2026-01-20 to 2026-01-23

---

## Future Enhancements

- [ ] Add more customer profiles
- [ ] Add transaction patterns (recurring, seasonal)
- [ ] Add merchant database
- [ ] Add fraud rules engine
- [ ] Add customer preferences
- [ ] Add transaction categories
- [ ] Add spending limits
- [ ] Add alert history
