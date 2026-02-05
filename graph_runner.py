"""Graph Runner - Wrapper to invoke the agent cleanly from Streamlit UI"""

import sys
import os
from io import StringIO
from contextlib import redirect_stdout
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.unified_agent import UnifiedCustomerSupportAgent
from knowledge_base import get_customer, get_transactions

# Load environment variables
load_dotenv()

class AgentRunner:
    """
    Wrapper class to run the UnifiedCustomerSupportAgent in a stateful manner
    suitable for Streamlit's interactive UI
    """
    
    def __init__(self):
        self.agent = UnifiedCustomerSupportAgent()
        self.current_stage = "initial"
        self.selected_option = None
        self.verification_attempts = 0
        self.max_verification_attempts = 3
        self.pending_transaction = None
        self.general_query = None
        
    def get_state(self):
        """Get current agent state"""
        return {
            "customer_id": self.agent.customer_id,
            "customer_name": self.agent.customer_name,
            "last_4": self.agent.last_4,
            "stage": self.current_stage,
            "verified": self.agent.customer_id is not None
        }
    
    def process_input(self, user_input: str, current_stage: str):
        """
        Process user input based on current conversation stage
        
        Args:
            user_input: User's text input
            current_stage: Current conversation stage
            
        Returns:
            tuple: (response_text, execution_trace)
        """
        user_input = user_input.strip()
        trace = {"action": "process_input", "stage": current_stage, "input": user_input}
        
        # Check for termination keywords at any stage (except initial and critical confirmation stages)
        user_lower = user_input.lower()
        termination_keywords = ["no thanks", "thanks", "thank you", "no thank you", "that's all", "thats all"]
        
        # Check if user wants to terminate (but not during fraud confirmation where "no" has specific meaning)
        if current_stage not in ["initial", "fraud_confirmation", "fraud_action"]:
            if user_lower in termination_keywords or (user_lower == "no" and current_stage not in ["verify_mobile", "verify_card", "fraud_details"]):
                self.current_stage = "initial"
                self.selected_option = None
                self.pending_transaction = None
                self.general_query = None
                
                response = """Thank you for contacting us! 

How can I help you today?

Please select an option:
1. General Enquiry (Reward points, Statement, Credit limit, etc.)
2. Fraud Transaction (Report suspicious transaction)

Type **1** or **2** to continue."""
                trace["action"] = "conversation_terminated"
                return response, trace
        
        # Stage: Initial - Select option
        if current_stage == "initial":
            if user_input in ["1", "2"]:
                self.selected_option = user_input
                self.current_stage = "verify_mobile"
                
                if user_input == "1":
                    response = """Sure! I'd be happy to help you with your general enquiry.

For security purposes, I need to verify your identity.

Please provide your registered mobile number:"""
                    trace["action"] = "option_selected"
                    trace["option"] = "general_enquiry"
                else:
                    response = """I understand you received a suspicious transaction SMS. Let me help you with that.

For security purposes, I need to verify your identity.

Please provide your registered mobile number:"""
                    trace["action"] = "option_selected"
                    trace["option"] = "fraud_transaction"
                
                return response, trace
            else:
                response = "Please select a valid option: Type **1** for General Enquiry or **2** for Fraud Transaction."
                trace["action"] = "invalid_option"
                return response, trace
        
        # Stage: Verify Mobile Number
        elif current_stage == "verify_mobile":
            mobile_number = user_input.strip()
            
            # Check if mobile number exists in database
            from knowledge_base import CUSTOMER_DB
            
            customer_found = None
            for customer in CUSTOMER_DB:
                if customer["mobile_number"] == mobile_number:
                    customer_found = customer
                    break
            
            if customer_found:
                # Store mobile number temporarily and ask for last 4 digits
                self.agent.mobile_number = mobile_number
                self.current_stage = "verify_card"
                self.verification_attempts = 0
                
                response = f"""Thank you! Mobile number verified. ✓

Now, please provide the last 4 digits of your card:"""
                trace["action"] = "mobile_verified"
                trace["mobile_number"] = mobile_number
                return response, trace
            else:
                self.verification_attempts += 1
                if self.verification_attempts >= self.max_verification_attempts:
                    response = "Mobile number verification failed. Please contact customer support or try again later."
                    self.current_stage = "initial"
                    self.verification_attempts = 0
                    trace["action"] = "mobile_verification_failed_max_attempts"
                    return response, trace
                
                response = f"""Sorry, I couldn't find this mobile number in our records.

Please check and try again.

Attempts remaining: {self.max_verification_attempts - self.verification_attempts}"""
                trace["action"] = "mobile_not_found"
                return response, trace
        
        # Stage: Verify Card Last 4 Digits
        elif current_stage == "verify_card":
            last_4 = user_input.strip()
            
            # Verify customer with mobile number and last 4 digits
            customer = get_customer(self.agent.mobile_number, last_4)
            
            if customer:
                self.agent.customer_id = customer["customer_id"]
                self.agent.customer_name = customer["name"]
                self.agent.last_4 = last_4
                self.verification_attempts = 0
                
                # Get recent transactions
                transactions = get_transactions(customer["customer_id"])
                
                if self.selected_option == "1":
                    # General enquiry flow
                    self.current_stage = "general_enquiry"
                    response = f"""Thank you, {customer['name']}. Your identity has been verified. ✓

How can I assist you today? You can ask about:
- Reward points balance
- Credit limit
- Recent transactions
- Statement details
- Any other credit card related query

Please type your question."""
                    trace["action"] = "verification_success"
                    trace["customer_id"] = customer["customer_id"]
                else:
                    # Fraud transaction flow
                    self.current_stage = "fraud_details"
                    
                    # Show recent transactions
                    trans_list = "\n".join([
                        f"{i+1}. {t['date']} - ${t['amount']:.2f} at {t['merchant']} ({t['status']})"
                        for i, t in enumerate(transactions[:5])
                    ])
                    
                    response = f"""Thank you, {customer['name']}. Your identity has been verified. ✓

Here are your recent transactions:
{trans_list}

Which transaction would you like to report as suspicious?
Please provide the transaction number (1-{len(transactions[:5])}) or describe the transaction."""
                    trace["action"] = "verification_success_fraud"
                    trace["customer_id"] = customer["customer_id"]
                    trace["transactions_shown"] = len(transactions[:5])
                
                return response, trace
            else:
                self.verification_attempts += 1
                if self.verification_attempts >= self.max_verification_attempts:
                    response = "Card verification failed. Please contact customer support or try again later."
                    self.current_stage = "initial"
                    self.verification_attempts = 0
                    self.agent.mobile_number = None
                    trace["action"] = "card_verification_failed_max_attempts"
                    return response, trace
                
                response = f"""Sorry, the last 4 digits don't match our records for this mobile number.

Please try again.

Attempts remaining: {self.max_verification_attempts - self.verification_attempts}"""
                trace["action"] = "card_verification_failed"
                return response, trace
        
        # Stage: General Enquiry
        elif current_stage == "general_enquiry":
            # Use the agent to handle general queries
            self.general_query = user_input
            
            # Simple keyword-based responses (can be enhanced with LLM)
            user_lower = user_input.lower()
            
            if "reward" in user_lower or "point" in user_lower:
                response = f"""Your current reward points balance is: **5,240 points**

You can redeem these points for:
- Shopping vouchers
- Flight miles
- Cashback
- Gift cards

Would you like to know more about redemption options?"""
                trace["action"] = "reward_points_query"
            
            elif "credit limit" in user_lower or "limit" in user_lower:
                response = f"""Your credit card details:
- **Credit Limit**: $10,000
- **Available Credit**: $7,350
- **Used Credit**: $2,650

Your credit utilization is at 26.5%, which is healthy!

Would you like to request a credit limit increase?"""
                trace["action"] = "credit_limit_query"
            
            elif "transaction" in user_lower or "statement" in user_lower:
                transactions = get_transactions(self.agent.customer_id)
                trans_list = "\n".join([
                    f"- {t['date']} - ${t['amount']:.2f} at {t['merchant']} ({t['status']})"
                    for t in transactions[:10]
                ])
                response = f"""Here are your recent transactions:

{trans_list}

Would you like a detailed statement sent to your email?"""
                trace["action"] = "transaction_query"
            
            else:
                response = f"""I understand you're asking about: "{user_input}"

I'm here to help! Could you please be more specific? You can ask about:
- Reward points
- Credit limit
- Recent transactions
- Statement details
- Card benefits
- Payment due dates

Or feel free to rephrase your question."""
                trace["action"] = "general_query_clarification"
            
            return response, trace
        
        # Stage: Fraud Details
        elif current_stage == "fraud_details":
            # Parse transaction selection
            user_lower = user_input.lower()
            
            # Get transactions
            transactions = get_transactions(self.agent.customer_id)
            
            # Try to parse transaction number
            try:
                trans_num = int(user_input.strip()) - 1
                if 0 <= trans_num < len(transactions[:5]):
                    self.pending_transaction = transactions[trans_num]
                    self.current_stage = "fraud_confirmation"
                    
                    trans = self.pending_transaction
                    response = f"""You've selected:
**Transaction Details:**
- Date: {trans['date']}
- Amount: ${trans['amount']:.2f}
- Merchant: {trans['merchant']}
- Status: {trans['status']}

Did you authorize this transaction?
- Type **YES** if you authorized it
- Type **NO** if you did not authorize it"""
                    trace["action"] = "transaction_selected"
                    trace["transaction_id"] = trans.get("transaction_id", "unknown")
                    return response, trace
                else:
                    response = f"Please select a valid transaction number (1-{len(transactions[:5])})."
                    trace["action"] = "invalid_transaction_number"
                    return response, trace
            except ValueError:
                # Try keyword matching
                matching_trans = None
                for trans in transactions[:5]:
                    if user_lower in trans['merchant'].lower() or str(trans['amount']) in user_input:
                        matching_trans = trans
                        break
                
                if matching_trans:
                    self.pending_transaction = matching_trans
                    self.current_stage = "fraud_confirmation"
                    
                    response = f"""You've selected:
**Transaction Details:**
- Date: {matching_trans['date']}
- Amount: ${matching_trans['amount']:.2f}
- Merchant: {matching_trans['merchant']}
- Status: {matching_trans['status']}

Did you authorize this transaction?
- Type **YES** if you authorized it
- Type **NO** if you did not authorize it"""
                    trace["action"] = "transaction_matched"
                    trace["transaction_id"] = matching_trans.get("transaction_id", "unknown")
                    return response, trace
                else:
                    response = "I couldn't identify the transaction. Please provide the transaction number (1-5) from the list above."
                    trace["action"] = "transaction_not_found"
                    return response, trace
        
        # Stage: Fraud Confirmation
        elif current_stage == "fraud_confirmation":
            user_lower = user_input.lower()
            
            if "no" in user_lower:
                # Unauthorized transaction - block card and raise dispute
                self.current_stage = "fraud_action"
                
                trans = self.pending_transaction
                response = f"""I understand this is concerning. For your security, I will:

1. **Block your card** immediately to prevent further unauthorized transactions
2. **Raise a dispute** for the transaction of ${trans['amount']:.2f}

A new card will be issued and sent to your registered address within 5-7 business days.

Should I proceed with these actions?
- Type **YES** to proceed
- Type **NO** to cancel"""
                trace["action"] = "fraud_confirmed"
                trace["transaction_amount"] = trans['amount']
                return response, trace
            
            elif "yes" in user_lower:
                # Authorized transaction - no action needed
                self.current_stage = "completed"
                response = f"""Thank you for confirming. Since you authorized this transaction, no action is needed.

If you have any other concerns, please let me know!

Type **1** or **2** to start a new query."""
                trace["action"] = "transaction_authorized"
                return response, trace
            else:
                response = "Please respond with **YES** or **NO**."
                trace["action"] = "invalid_confirmation"
                return response, trace
        
        # Stage: Fraud Action
        elif current_stage == "fraud_action":
            user_lower = user_input.lower()
            
            if "yes" in user_lower:
                # Execute fraud actions
                trans = self.pending_transaction
                
                # Simulate blocking card
                block_ticket = f"BLK{hash(self.agent.customer_id) % 1000000:06d}"
                
                # Simulate raising dispute
                dispute_ticket = f"DSP{hash(trans.get('transaction_id', 'unknown')) % 1000000:06d}"
                
                self.current_stage = "completed"
                response = f"""✓ Actions completed successfully!

**Card Blocked:**
- Ticket ID: {block_ticket}
- Your card ending in {self.agent.last_4} has been blocked

**Dispute Raised:**
- Ticket ID: {dispute_ticket}
- Amount: ${trans['amount']:.2f}
- Merchant: {trans['merchant']}

**Next Steps:**
- New card will arrive in 5-7 business days
- Dispute will be investigated within 30 days
- You'll receive SMS updates on both tickets

Is there anything else I can help you with?
Type **1** or **2** to start a new query."""
                trace["action"] = "fraud_actions_completed"
                trace["block_ticket"] = block_ticket
                trace["dispute_ticket"] = dispute_ticket
                return response, trace
            
            elif "no" in user_lower:
                self.current_stage = "completed"
                response = f"""Understood. No action has been taken.

If you change your mind or need assistance, please let me know!

Type **1** or **2** to start a new query."""
                trace["action"] = "fraud_actions_cancelled"
                return response, trace
            else:
                response = "Please respond with **YES** or **NO**."
                trace["action"] = "invalid_action_confirmation"
                return response, trace
        
        # Stage: Completed
        elif current_stage == "completed":
            if user_input in ["1", "2"]:
                # Reset and start new conversation
                self.current_stage = "initial"
                self.selected_option = None
                self.pending_transaction = None
                self.general_query = None
                # Don't reset customer verification
                
                return self.process_input(user_input, "initial")
            else:
                response = "Please type **1** for General Enquiry or **2** for Fraud Transaction to start a new query."
                trace["action"] = "awaiting_new_query"
                return response, trace
        
        # Default fallback
        else:
            response = "I'm sorry, something went wrong. Please start over by typing **1** or **2**."
            self.current_stage = "initial"
            trace["action"] = "error_fallback"
            return response, trace
