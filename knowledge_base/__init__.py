"""Knowledge Base - Customer and Transaction Data with RAG"""

from .customers import CUSTOMER_DB, get_customer, list_all_customers
from .transactions import TRANSACTIONS_DB, get_transactions, get_transaction_by_id, get_suspicious_transactions
from .policies import (
    TRANSACTION_LIFECYCLE,
    FRAUD_POLICIES,
    CARD_BLOCK_RULES,
    DISPUTE_PROCESS,
    COMPLIANCE_RULES,
    SMS_FORMATS,
    FRAUD_SLA,
    ESCALATION_RULES,
    get_policy
)
from .rag_retriever import KnowledgeBaseRAG, rag

__all__ = [
    # Customer data
    'CUSTOMER_DB',
    'get_customer',
    'list_all_customers',
    # Transaction data
    'TRANSACTIONS_DB',
    'get_transactions',
    'get_transaction_by_id',
    'get_suspicious_transactions',
    # Policies
    'TRANSACTION_LIFECYCLE',
    'FRAUD_POLICIES',
    'CARD_BLOCK_RULES',
    'DISPUTE_PROCESS',
    'COMPLIANCE_RULES',
    'SMS_FORMATS',
    'FRAUD_SLA',
    'ESCALATION_RULES',
    'get_policy',
    # RAG
    'KnowledgeBaseRAG',
    'rag'
]
