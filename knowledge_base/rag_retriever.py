"""RAG (Retrieval-Augmented Generation) for Knowledge Base"""

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

class KnowledgeBaseRAG:
    """RAG system for retrieving policy and compliance information"""
    
    def __init__(self):
        self.knowledge = {
            "transaction_lifecycle": TRANSACTION_LIFECYCLE,
            "fraud_policies": FRAUD_POLICIES,
            "card_block_rules": CARD_BLOCK_RULES,
            "dispute_process": DISPUTE_PROCESS,
            "compliance_rules": COMPLIANCE_RULES,
            "sms_formats": SMS_FORMATS,
            "fraud_sla": FRAUD_SLA,
            "escalation_rules": ESCALATION_RULES
        }
    
    def retrieve(self, query: str) -> dict:
        """
        Retrieve relevant information based on query
        
        Args:
            query: Natural language query
            
        Returns:
            Relevant knowledge base information
        """
        query_lower = query.lower()
        results = {}
        
        # Transaction lifecycle queries
        if any(word in query_lower for word in ["transaction", "pending", "completed", "status"]):
            results["transaction_lifecycle"] = TRANSACTION_LIFECYCLE
        
        # Fraud policy queries
        if any(word in query_lower for word in ["fraud", "unauthorized", "suspicious"]):
            results["fraud_policies"] = FRAUD_POLICIES
            results["fraud_sla"] = FRAUD_SLA
        
        # Card block queries
        if any(word in query_lower for word in ["block", "unblock", "card", "stop"]):
            results["card_block_rules"] = CARD_BLOCK_RULES
        
        # Dispute queries
        if any(word in query_lower for word in ["dispute", "ticket", "complaint"]):
            results["dispute_process"] = DISPUTE_PROCESS
        
        # SLA queries
        if any(word in query_lower for word in ["sla", "timeline", "how long", "when"]):
            results["fraud_sla"] = FRAUD_SLA
        
        # Compliance queries
        if any(word in query_lower for word in ["compliance", "rbi", "pci", "regulation"]):
            results["compliance_rules"] = COMPLIANCE_RULES
        
        # Escalation queries
        if any(word in query_lower for word in ["escalate", "human", "manager", "senior"]):
            results["escalation_rules"] = ESCALATION_RULES
        
        return results
    
    def get_card_block_policy(self) -> dict:
        """Get card blocking policy"""
        return CARD_BLOCK_RULES
    
    def get_fraud_sla(self) -> dict:
        """Get fraud handling SLA timelines"""
        return FRAUD_SLA
    
    def get_dispute_process(self) -> dict:
        """Get dispute and ticket process"""
        return DISPUTE_PROCESS
    
    def get_compliance_rules(self) -> dict:
        """Get regulatory compliance rules"""
        return COMPLIANCE_RULES
    
    def can_block_card(self, transaction_status: str) -> bool:
        """Check if card can be blocked for given transaction status"""
        lifecycle = TRANSACTION_LIFECYCLE.get(transaction_status, {})
        return lifecycle.get("can_block", False)
    
    def requires_customer_consent(self, action: str) -> bool:
        """Check if action requires customer consent"""
        if action in ["block_card", "raise_dispute", "stop_transaction"]:
            return COMPLIANCE_RULES["rbi_guidelines"]["customer_consent"] == "Mandatory for all actions"
        return False
    
    def get_sla_for_action(self, action: str) -> str:
        """Get SLA timeline for specific action"""
        return FRAUD_SLA.get(action, "Not specified")
    
    def should_escalate(self, scenario: str) -> bool:
        """Check if scenario requires escalation"""
        return scenario in ESCALATION_RULES["auto_escalate"]
    
    def format_sms(self, sms_type: str, **kwargs) -> str:
        """Format SMS message based on template"""
        template_info = SMS_FORMATS.get(sms_type, {})
        template = template_info.get("template", "")
        return template.format(**kwargs)

# Global RAG instance
rag = KnowledgeBaseRAG()
