"""Customer database - Mock data for identity verification"""

# Mock customer database
# In production, this would connect to a real customer database (PostgreSQL, DynamoDB, etc.)
CUSTOMER_DB = {
    "9876543210_1234": {
        "customer_id": "CUST001",
        "name": "John Doe",
        "card_id": "CARD_1234",
        "mobile": "9876543210",
        "last_4": "1234",
        "email": "john.doe@example.com",
        "account_status": "active",
        "member_since": "2020-01-15",
        "reward_points": {
            "total_points": 12500,
            "cashback_value": 3125.00,
            "points_expiring_soon": 450,
            "expiry_date": "2026-03-31",
            "redemption_options": ["Shopping vouchers", "Travel bookings", "Bill payments", "Cashback to account"]
        }
    },
    "9998887776_5678": {
        "customer_id": "CUST002",
        "name": "Jane Smith",
        "card_id": "CARD_5678",
        "mobile": "9998887776",
        "last_4": "5678",
        "email": "jane.smith@example.com",
        "account_status": "active",
        "member_since": "2019-06-20",
        "reward_points": {
            "total_points": 8750,
            "cashback_value": 2187.50,
            "points_expiring_soon": 200,
            "expiry_date": "2026-03-31",
            "redemption_options": ["Shopping vouchers", "Travel bookings", "Bill payments", "Cashback to account"]
        }
    },
    "9123456789_9012": {
        "customer_id": "CUST003",
        "name": "Rajesh Kumar",
        "card_id": "CARD_9012",
        "mobile": "9123456789",
        "last_4": "9012",
        "email": "rajesh.kumar@example.com",
        "account_status": "active",
        "member_since": "2021-03-10",
        "reward_points": {
            "total_points": 15200,
            "cashback_value": 3800.00,
            "points_expiring_soon": 350,
            "expiry_date": "2026-03-31",
            "redemption_options": ["Shopping vouchers", "Travel bookings", "Bill payments", "Cashback to account"]
        }
    }
}

def get_customer(mobile_number: str, last_4_digits: str) -> dict:
    """
    Retrieve customer information by mobile number and last 4 digits
    
    Args:
        mobile_number: Customer's registered mobile number
        last_4_digits: Last 4 digits of credit card
        
    Returns:
        Customer information dict or None if not found
    """
    key = f"{mobile_number}_{last_4_digits}"
    return CUSTOMER_DB.get(key)

def list_all_customers() -> list:
    """
    Get list of all customers (for testing/demo purposes)
    
    Returns:
        List of customer dictionaries
    """
    return list(CUSTOMER_DB.values())
