"""Credit Card Policies and Rules - Knowledge Base for RAG"""

# Transaction Lifecycle
TRANSACTION_LIFECYCLE = {
    "pending": {
        "description": "Transaction initiated but not yet settled",
        "duration": "1-3 business days",
        "can_dispute": True,
        "can_block": True
    },
    "completed": {
        "description": "Transaction settled and posted to account",
        "duration": "Permanent unless disputed",
        "can_dispute": True,
        "can_block": False
    },
    "declined": {
        "description": "Transaction rejected by system or bank",
        "duration": "Immediate",
        "can_dispute": False,
        "can_block": False
    }
}

# Fraud Handling Policies
FRAUD_POLICIES = {
    "immediate_actions": [
        "Block card immediately upon customer confirmation",
        "Raise fraud verification ticket",
        "Stop all pending transactions",
        "Notify customer via SMS and email"
    ],
    "investigation_process": [
        "Fraud team reviews transaction within 24 hours",
        "Customer may be contacted for additional verification",
        "Merchant verification conducted",
        "Decision made within 5-7 business days"
    ],
    "customer_liability": {
        "reported_within_24h": "Zero liability",
        "reported_within_7_days": "Maximum ₹500 liability",
        "reported_after_7_days": "As per bank policy, up to ₹10,000"
    }
}

# Card Block/Unblock Rules
CARD_BLOCK_RULES = {
    "block_reasons": [
        "Unauthorized transaction reported",
        "Card lost or stolen",
        "Suspected fraud activity",
        "Customer request for security",
        "Multiple failed PIN attempts"
    ],
    "block_process": {
        "requires_consent": True,
        "immediate_effect": True,
        "notification": "SMS + Email within 5 minutes",
        "new_card_dispatch": "3-5 business days"
    },
    "unblock_rules": {
        "allowed_for": ["Temporary blocks", "Customer-initiated blocks"],
        "not_allowed_for": ["Fraud cases", "Lost/stolen cards"],
        "verification_required": True,
        "processing_time": "Immediate to 2 hours"
    }
}

# Dispute & Ticket Process
DISPUTE_PROCESS = {
    "ticket_types": {
        "fraud_verification": {
            "priority": "High",
            "sla": "24 hours for initial review",
            "resolution_time": "5-7 business days",
            "requires_documents": False
        },
        "unauthorized_transaction": {
            "priority": "High",
            "sla": "48 hours for initial review",
            "resolution_time": "7-10 business days",
            "requires_documents": True
        },
        "merchant_dispute": {
            "priority": "Medium",
            "sla": "3 business days",
            "resolution_time": "30-45 days",
            "requires_documents": True
        }
    },
    "ticket_format": {
        "prefix": "FRD" if "fraud" else "CCB",
        "length": 6,
        "example": "FRD123456"
    },
    "customer_rights": [
        "Right to dispute within 60 days",
        "Right to provisional credit during investigation",
        "Right to appeal decision",
        "Right to escalate to banking ombudsman"
    ]
}

# Regulatory & Compliance Rules
COMPLIANCE_RULES = {
    "rbi_guidelines": {
        "customer_consent": "Mandatory for all actions",
        "data_protection": "No storage of CVV, PIN, or OTP",
        "notification": "All actions must be notified within 24 hours",
        "liability": "Zero liability for reported fraud within 3 days"
    },
    "pci_dss": {
        "card_number": "Never ask for full card number",
        "cvv": "Never ask for CVV",
        "pin": "Never ask for PIN",
        "otp": "Never ask for OTP",
        "last_4_digits": "Allowed for verification"
    },
    "data_retention": {
        "transaction_data": "7 years",
        "customer_data": "Until account closure + 7 years",
        "dispute_records": "10 years",
        "call_recordings": "90 days"
    }
}

# SMS Alert Formats
SMS_FORMATS = {
    "transaction_alert": {
        "template": "Your card ending {last4} used for Rs.{amount} at {merchant} on {date}. If not you, call {support_number} immediately.",
        "example": "Your card ending 1234 used for Rs.8900 at Unknown Merchant XYZ on 21-Jan-2026. If not you, call 1800-XXX-XXXX immediately."
    },
    "card_blocked": {
        "template": "Your card ending {last4} has been blocked as per your request. Ticket ID: {ticket_id}. New card will be dispatched in 3-5 days.",
        "example": "Your card ending 1234 has been blocked as per your request. Ticket ID: FRD123456. New card will be dispatched in 3-5 days."
    },
    "dispute_raised": {
        "template": "Dispute ticket {ticket_id} raised for Rs.{amount} transaction. Resolution in {sla} days. Track at {url}",
        "example": "Dispute ticket CCB789012 raised for Rs.8900 transaction. Resolution in 5-7 days. Track at www.bank.com/disputes"
    }
}

# Fraud SLA Timelines
FRAUD_SLA = {
    "initial_response": "Immediate (during call)",
    "card_block": "Immediate (within 2 minutes)",
    "ticket_creation": "Immediate (within 5 minutes)",
    "sms_notification": "Within 5 minutes",
    "email_notification": "Within 30 minutes",
    "fraud_team_review": "Within 24 hours",
    "investigation_completion": "5-7 business days",
    "provisional_credit": "Within 10 business days (if eligible)",
    "final_resolution": "30-45 days maximum",
    "new_card_dispatch": "3-5 business days",
    "new_card_delivery": "7-10 business days"
}

# Escalation Rules
ESCALATION_RULES = {
    "auto_escalate": [
        "Multiple unauthorized transactions (>3)",
        "High-value fraud (>₹50,000)",
        "Customer extremely distressed (angry/anxious)",
        "Identity verification failed twice",
        "Customer explicitly requests human agent"
    ],
    "escalation_levels": {
        "level_1": "Senior Support Agent",
        "level_2": "Fraud Investigation Team",
        "level_3": "Branch Manager",
        "level_4": "Banking Ombudsman"
    },
    "escalation_sla": {
        "level_1": "Immediate",
        "level_2": "Within 2 hours",
        "level_3": "Within 24 hours",
        "level_4": "As per RBI guidelines"
    }
}

def get_policy(policy_type: str, key: str = None):
    """
    Retrieve policy information from knowledge base
    
    Args:
        policy_type: Type of policy (fraud, block, dispute, etc.)
        key: Specific key within policy (optional)
        
    Returns:
        Policy information
    """
    policies = {
        "transaction_lifecycle": TRANSACTION_LIFECYCLE,
        "fraud": FRAUD_POLICIES,
        "block": CARD_BLOCK_RULES,
        "dispute": DISPUTE_PROCESS,
        "compliance": COMPLIANCE_RULES,
        "sms": SMS_FORMATS,
        "sla": FRAUD_SLA,
        "escalation": ESCALATION_RULES
    }
    
    policy = policies.get(policy_type)
    if key and isinstance(policy, dict):
        return policy.get(key)
    return policy
