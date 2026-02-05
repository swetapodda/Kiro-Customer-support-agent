"""Transaction database - Mock data for transaction history"""

# Mock transaction database
# In production, this would query a real transaction database with proper indexing
TRANSACTIONS_DB = {
    "CUST001": [
        {
            "transaction_id": "TXN001",
            "date": "2026-01-23",
            "amount": 1250.00,
            "merchant": "Amazon",
            "merchant_category": "E-commerce",
            "status": "completed",
            "location": "Online",
            "card_last_4": "1234"
        },
        {
            "transaction_id": "TXN002",
            "date": "2026-01-22",
            "amount": 450.50,
            "merchant": "Starbucks",
            "merchant_category": "Food & Beverage",
            "status": "completed",
            "location": "New York, NY",
            "card_last_4": "1234"
        },
        {
            "transaction_id": "TXN003",
            "date": "2026-01-21",
            "amount": 8900.00,
            "merchant": "Unknown Merchant XYZ",
            "merchant_category": "Unknown",
            "status": "pending",
            "location": "International",
            "card_last_4": "1234",
            "fraud_score": 0.85  # High fraud probability
        },
    ],
    "CUST002": [
        {
            "transaction_id": "TXN004",
            "date": "2026-01-23",
            "amount": 350.00,
            "merchant": "Walmart",
            "merchant_category": "Retail",
            "status": "completed",
            "location": "Los Angeles, CA",
            "card_last_4": "5678"
        },
        {
            "transaction_id": "TXN005",
            "date": "2026-01-20",
            "amount": 2100.00,
            "merchant": "Best Buy",
            "merchant_category": "Electronics",
            "status": "completed",
            "location": "San Francisco, CA",
            "card_last_4": "5678"
        },
    ],
    "CUST003": [
        {
            "transaction_id": "TXN006",
            "date": "2026-02-04",
            "amount": 1200.00,
            "merchant": "Target",
            "merchant_category": "Retail",
            "status": "completed",
            "location": "Mumbai, India",
            "card_last_4": "9012"
        },
        {
            "transaction_id": "TXN007",
            "date": "2026-02-05 02:30 AM",
            "amount": 18900.00,
            "merchant": "GlobalTech Solutions Ltd",
            "merchant_category": "Electronics",
            "status": "pending",
            "location": "Singapore (International)",
            "card_last_4": "9012",
            "fraud_score": 0.75,  # High risk
            "transaction_time": "Late night",
            "merchant_status": "Newly added"
        },
    ]
}

def get_transactions(customer_id: str, limit: int = 5) -> list:
    """
    Retrieve recent transactions for a customer
    
    Args:
        customer_id: Customer identifier
        limit: Maximum number of transactions to return
        
    Returns:
        List of transaction dictionaries
    """
    transactions = TRANSACTIONS_DB.get(customer_id, [])
    return transactions[:limit]

def get_transaction_by_id(transaction_id: str) -> dict:
    """
    Retrieve a specific transaction by ID
    
    Args:
        transaction_id: Transaction identifier
        
    Returns:
        Transaction dictionary or None if not found
    """
    for customer_transactions in TRANSACTIONS_DB.values():
        for transaction in customer_transactions:
            if transaction["transaction_id"] == transaction_id:
                return transaction
    return None

def get_suspicious_transactions(customer_id: str) -> list:
    """
    Get transactions with high fraud scores
    
    Args:
        customer_id: Customer identifier
        
    Returns:
        List of suspicious transactions
    """
    transactions = TRANSACTIONS_DB.get(customer_id, [])
    return [t for t in transactions if t.get("fraud_score", 0) > 0.7]
