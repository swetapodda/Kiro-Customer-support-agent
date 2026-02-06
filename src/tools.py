"""Customer support tools for identity verification, transaction retrieval, and actions"""
import random
from datetime import datetime, timedelta
from knowledge_base import get_customer, get_transactions

def verify_customer(mobile_number: str, last_4_digits: str) -> dict:
    """
    Verify customer identity using mobile number and last 4 digits of card
    
    Args:
        mobile_number: Registered mobile number
        last_4_digits: Last 4 digits of credit card
        
    Returns:
        dict with verified status and customer_id
    """
    customer = get_customer(mobile_number, last_4_digits)
    
    if customer:
        return {
            "verified": True,
            "customer_id": customer["customer_id"],
            "name": customer["name"],
            "card_id": customer["card_id"]
        }
    return {"verified": False, "customer_id": None}

def fetch_recent_transactions(customer_id: str, limit: int = 5) -> list:
    """
    Fetch recent credit card transactions for a customer
    
    Args:
        customer_id: Customer identifier
        limit: Number of recent transactions to fetch
        
    Returns:
        List of transactions with masked sensitive data
    """
    transactions = get_transactions(customer_id, limit)
    return transactions
    return transactions[:limit]

def block_card(card_id: str) -> dict:
    """
    Block a credit card immediately
    
    Args:
        card_id: Card identifier
        
    Returns:
        dict with success status and ticket number
    """
    ticket_number = f"BLK{random.randint(100000, 999999)}"
    return {
        "success": True,
        "ticket_number": ticket_number,
        "message": f"Card {card_id} has been blocked successfully",
        "timestamp": datetime.now().isoformat()
    }

def raise_dispute_ticket(customer_id: str, transaction_details: dict) -> dict:
    """
    Raise a dispute ticket for unauthorized transaction
    
    Args:
        customer_id: Customer identifier
        transaction_details: Details of the disputed transaction
        
    Returns:
        dict with ticket information
    """
    ticket_number = f"CCB{random.randint(100000, 999999)}"
    return {
        "success": True,
        "ticket_number": ticket_number,
        "message": "Dispute ticket created successfully",
        "estimated_resolution": "5-7 business days",
        "timestamp": datetime.now().isoformat()
    }

def escalate_to_human_agent(context: dict) -> dict:
    """
    Escalate conversation to human agent
    
    Args:
        context: Current conversation context
        
    Returns:
        dict with escalation details
    """
    escalation_id = f"ESC{random.randint(100000, 999999)}"
    return {
        "success": True,
        "escalation_id": escalation_id,
        "message": "Connecting you to a human agent",
        "estimated_wait_time": "2-3 minutes",
        "priority": context.get("risk_level", "medium")
    }
