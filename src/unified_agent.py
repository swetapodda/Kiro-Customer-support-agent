"""Unified Credit Card Customer Support Agent - General Enquiry + Fraud Transaction"""

import os
import sys
import random
from dotenv import load_dotenv

# Add parent directory to path to import knowledge_base
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge_base import rag, get_customer, get_transactions
from src.tools import block_card, raise_dispute_ticket

# Load environment variables
load_dotenv()

class UnifiedCustomerSupportAgent:
    """
    Unified Credit Card Customer Support AI Agent
    Options: 1. General Enquiry (with proactive safety check)
             2. Fraud Transaction (direct fraud handling)
    """
    
    def __init__(self):
        self.rag = rag
        self.customer_id = None
        self.customer_name = None
        self.last_4 = None
        self.suspicious_transactions = []
    
    def run(self):
        """Run unified agent with 2 options"""
        print("=" * 70)
        print("Credit Card Customer Support Agent")
        print("=" * 70)
        print()
        
        # Step 1: Ask customer to choose option
        print("Agent: Hello! Welcome to Credit Card Customer Support.")
        print("Agent: How can I help you today?\n")
        print("Please select an option:")
        print("1. General Enquiry (Reward points, Statement, Credit limit, etc.)")
        print("2. Fraud Transaction (Report suspicious transaction)\n")
        
        choice = input("You (Enter 1 or 2): ").strip()
        print()
        
        if choice == "1":
            self.handle_general_enquiry()
        elif choice == "2":
            self.handle_fraud_transaction()
        else:
            print("Agent: Invalid option. Please restart and select 1 or 2.")
    
    def handle_general_enquiry(self):
        """Handle general enquiry with proactive safety check"""
        print("Agent: Sure! What would you like to know about?\n")
        
        general_query = input("You: ").strip()
        print()
        
        print("Agent: I'd be happy to help you with that.")
        print("Agent: Let me pull up your account details.\n")
        
        # Verify identity
        if not self.verify_identity_with_retry():
            return
        
        # Silent background risk check
        print("Agent: One moment please... (Accessing your account)\n")
        
        transactions = get_transactions(self.customer_id)
        self.suspicious_transactions = self.detect_unusual_activity(transactions)
        
        # Proactive alert if suspicious activity found
        if self.suspicious_transactions:
            high_risk_txn = self.suspicious_transactions[0]
            
            print("Agent: Before we continue, I'd like to quickly confirm a recent transaction")
            print("       for your safety.\n")
            
            # Calm, specific, non-alarming language
            location_info = ""
            if "international" in high_risk_txn.get('location', '').lower():
                location_info = " at an overseas merchant"
            
            time_info = ""
            if high_risk_txn.get('transaction_time'):
                time_info = f" {high_risk_txn['transaction_time']}"
            
            print(f"Agent: A charge of ₹{high_risk_txn['amount']:.2f}{location_info} was made{time_info}.")
            print(f"Agent: Merchant: {high_risk_txn['merchant']}")
            print(f"Agent: Date: {high_risk_txn['date']}")
            print()
            print("Agent: Was this transaction done by you?\n")
            
            response = input("You (Yes/No): ").strip().lower()
            print()
            
            if response in ['yes', 'y']:
                print("Agent: Thank you for confirming. Your transaction is legitimate.")
                print(f"Agent: Now, regarding your query about '{general_query}'...\n")
                
                # Process the general query
                self.process_general_query(general_query)
                
                self.ask_anything_else()
            else:
                # Customer denies - fraud case
                self.process_fraud_with_consent(high_risk_txn)
        else:
            # No suspicious activity
            print("✅ Agent: Good news! All your recent transactions appear normal.")
            print(f"Agent: Now, regarding your query about '{general_query}'...\n")
            
            # Process the general query
            self.process_general_query(general_query)
            
            self.ask_anything_else()
    
    def handle_fraud_transaction(self):
        """Handle direct fraud transaction report"""
        print("Agent: I understand you received a suspicious transaction SMS.")
        print("Agent: Let me help you with that.\n")
        
        # Verify identity
        if not self.verify_identity_with_retry():
            return
        
        # Ask customer about the suspicious transaction
        print("Agent: Can you please tell me about the transaction you're concerned about?")
        print("Agent: Please provide the transaction amount.\n")
        
        transaction_amount = input("You (Amount in ₹): ").strip()
        print()
        
        # Fetch recent transactions
        transactions = get_transactions(self.customer_id)
        if not transactions:
            print("Agent: No recent transactions found.")
            return
        
        # Find matching transaction
        matched_txn = None
        for txn in transactions:
            if str(txn['amount']) == transaction_amount or str(int(float(transaction_amount))) == str(int(txn['amount'])):
                matched_txn = txn
                break
        
        if not matched_txn:
            print(f"Agent: I couldn't find a transaction for ₹{transaction_amount}.")
            print("Agent: Is there any other transaction that seems suspicious to you?\n")
            
            retry_response = input("You (Yes/No): ").strip().lower()
            print()
            
            if retry_response in ['yes', 'y']:
                print("Agent: Please provide the amount of the suspicious transaction.\n")
                transaction_amount = input("You (Amount in ₹): ").strip()
                print()
                
                for txn in transactions:
                    if str(txn['amount']) == transaction_amount or str(int(float(transaction_amount))) == str(int(txn['amount'])):
                        matched_txn = txn
                        break
                
                if not matched_txn:
                    print(f"Agent: I still couldn't find a transaction for ₹{transaction_amount}.")
                    print("Agent: Let me connect you with a specialist for further assistance.")
                    print("Agent: Your reference number is: REF" + str(random.randint(100000, 999999)))
                    return
            else:
                print("Agent: Thank you for contacting us. If you notice any suspicious activity,")
                print("Agent: please don't hesitate to reach out immediately.")
                print("Agent: Have a great day!")
                return
        
        # Confirm transaction details
        print(f"Agent: I found a transaction for ₹{matched_txn['amount']:.2f}")
        print(f"Agent: Merchant: {matched_txn['merchant']}")
        print(f"Agent: Date: {matched_txn['date']}")
        print(f"Agent: Status: {matched_txn['status'].upper()}\n")
        
        print("Agent: Did you perform this transaction?")
        response = input("You (Yes/No): ").strip().lower()
        print()
        
        if response in ['yes', 'y']:
            print("Agent: Thank you for confirming. Your transaction is legitimate.")
            print("Agent: Is there anything else I can help you with?")
            
            continue_response = input("You (Yes/No): ").strip().lower()
            print()
            
            if continue_response in ['no', 'n']:
                print("Agent: Thank you for contacting us. Have a great day!")
            else:
                print("Agent: I'm here to help! Please describe your concern.")
                additional_query = input("You: ").strip()
                print()
                print("Agent: Thank you for sharing. Let me connect you with a specialist who can assist you better.")
                print("Agent: Your reference number is: REF" + str(random.randint(100000, 999999)))
                print("Agent: Have a great day!")
        else:
            # Customer denies - fraud case
            self.process_fraud_with_consent(matched_txn)
    
    def verify_identity_with_retry(self) -> bool:
        """Verify identity with 3 retry attempts"""
        print("Agent: For security purposes, I need to verify your identity.")
        print("Agent: Please provide your registered mobile number and last 4 digits of your card.\n")
        
        max_attempts = 3
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            
            if attempt > 1:
                print(f"\nAgent: Attempt {attempt} of {max_attempts}. Please try again.\n")
            
            mobile = input("You (Mobile Number): ").strip()
            last4 = input("You (Last 4 Digits): ").strip()
            print()
            
            customer = get_customer(mobile, last4)
            
            if customer:
                self.customer_id = customer["customer_id"]
                self.customer_name = customer["name"]
                self.last_4 = last4
                self.state = {
                    "mobile": mobile,
                    "last_4": last4,
                    "customer_id": customer["customer_id"],
                    "customer_name": customer["name"]
                }
                print(f"Agent: Thank you, {self.customer_name}. Identity verified.\n")
                return True
            else:
                remaining = max_attempts - attempt
                if remaining > 0:
                    print(f"Agent: ❌ I couldn't verify your identity.")
                    print(f"Agent: You have {remaining} attempt(s) remaining.")
                else:
                    print("Agent: ❌ I couldn't verify your identity after 3 attempts.")
                    print("Agent: For security reasons, I must end this session.")
                    print("Agent: Please contact our branch or call our helpline for assistance.")
                    return False
        
        return False
    
    def detect_unusual_activity(self, transactions: list) -> list:
        """Silent risk check - detect unusual transactions"""
        suspicious = []
        
        for txn in transactions:
            risk_factors = []
            
            if txn.get('fraud_score', 0) > 0.7:
                risk_factors.append("high_fraud_score")
            
            if 'international' in txn.get('location', '').lower():
                risk_factors.append("international")
            
            if txn.get('transaction_time') and 'late' in txn.get('transaction_time', '').lower():
                risk_factors.append("late_night")
            
            if txn.get('merchant_status') == 'Newly added':
                risk_factors.append("new_merchant")
            
            if txn.get('status') == 'pending' and txn.get('amount', 0) > 5000:
                risk_factors.append("high_value_pending")
            
            if 'unknown' in txn.get('merchant', '').lower():
                risk_factors.append("unknown_merchant")
            
            if len(risk_factors) >= 2:
                suspicious.append(txn)
        
        return suspicious
    
    def process_fraud_with_consent(self, transaction: dict):
        """Process fraud case with customer consent"""
        print("Agent: Thank you for letting me know. I understand your concern.\n")
        
        # Explain protection steps
        print("Agent: For your protection, I recommend we take immediate action.")
        print("Agent: Here's what I suggest:\n")
        print("       • Block your card to prevent further unauthorized charges")
        print("       • Raise a fraud verification request")
        print("       • Our fraud team will investigate within 24 hours")
        print("       • You'll have zero liability as per RBI guidelines\n")
        
        # Get consent
        compliance = self.rag.get_compliance_rules()
        print(f"Agent: As per RBI guidelines: {compliance['rbi_guidelines']['customer_consent']}\n")
        print("Agent: Shall I immediately block the card and raise a fraud verification request?")
        
        consent = input("You (Yes/No): ").strip().lower()
        print()
        
        if consent not in ['yes', 'y', 'i consent', 'consent']:
            print("Agent: I understand. However, I strongly recommend taking action soon.")
            print("Agent: Your card remains at risk until blocked.")
            print("Agent: Please call us back immediately if you change your mind.")
            return
        
        # Block card and raise ticket
        print("Agent: Thank you for your consent. Processing immediately...\n")
        
        block_result = block_card(f"CARD_{self.customer_id}")
        dispute_result = raise_dispute_ticket(
            self.customer_id,
            {"amount": transaction['amount'], "transaction_id": transaction.get('transaction_id', 'N/A')}
        )
        
        sla = self.rag.get_fraud_sla()
        
        # Share results
        print("✅ Actions Completed Successfully!\n")
        print("📋 Summary:")
        print(f"   • Card Status: BLOCKED (Card ending {self.last_4})")
        print(f"   • Block Reference: {block_result['ticket_number']}")
        print(f"   • Fraud Ticket: {dispute_result['ticket_number']}")
        print(f"   • Transaction Flagged: ₹{transaction['amount']:.2f}\n")
        
        print("⏱️ Expected Resolution Timeline:")
        print(f"   • Fraud team review: {sla['fraud_team_review']}")
        print(f"   • Investigation completion: {sla['investigation_completion']}")
        print(f"   • New card dispatch: {sla['new_card_dispatch']}")
        print(f"   • New card delivery: {sla['new_card_delivery']}\n")
        
        print("🛡️  Customer Liability Protection:")
        from knowledge_base.policies import FRAUD_POLICIES
        liability = FRAUD_POLICIES['customer_liability']
        print(f"   • Reported within 24h: {liability['reported_within_24h']}")
        print(f"   • Your case: Zero liability (reported immediately)\n")
        
        print(f"Agent: Your fraud ticket reference is {dispute_result['ticket_number']}.")
        print("Agent: You will receive SMS and email confirmations within 5 minutes.")
        print("Agent: Our fraud team will contact you within 24 hours if needed.\n")
        
        # Share prevention tips
        self.share_prevention_tips()
    
    def ask_anything_else(self):
        """Ask if customer needs anything else"""
        print("Agent: Is there anything else I can help you with today?")
        continue_response = input("You (Yes/No): ").strip().lower()
        print()
        
        if continue_response in ['no', 'n']:
            print("Agent: Thank you for contacting us. Have a great day!")
        else:
            print("Agent: Please let me know what you need.")
            additional_query = input("You: ").strip()
            print()
            
            # Process the additional query
            self.process_general_query(additional_query)
            
            print("Agent: Is there anything else?")
            final_response = input("You (Yes/No): ").strip().lower()
            print()
            
            if final_response in ['no', 'n']:
                print("Agent: Thank you for contacting us. Have a great day!")
            else:
                print("Agent: For further assistance, please contact our helpline.")
                print("Agent: Your reference number is: REF" + str(random.randint(100000, 999999)))
                print("Agent: Have a great day!")
    
    def process_general_query(self, query: str):
        """Process general customer queries with mock responses"""
        query_lower = query.lower()
        
        # Reward points query
        if any(word in query_lower for word in ['reward', 'points', 'cashback']):
            # Get actual reward points from customer data
            customer = get_customer(self.state.get("mobile"), self.state.get("last_4"))
            if customer and "reward_points" in customer:
                rewards = customer["reward_points"]
                print(f"Agent: Here are your reward points details:\n")
                print(f"       • Total Reward Points: {rewards['total_points']:,}")
                print(f"       • Cashback Value: ₹{rewards['cashback_value']:.2f}")
                print(f"       • Points Expiring Soon: {rewards['points_expiring_soon']} (by {rewards['expiry_date']})")
                print(f"       • Redemption Options: {', '.join(rewards['redemption_options'])}\n")
            else:
                # Fallback if no reward data
                points = random.randint(5000, 15000)
                cashback = points * 0.25
                print(f"Agent: Here are your reward points details:\n")
                print(f"       • Total Reward Points: {points:,}")
                print(f"       • Cashback Value: ₹{cashback:.2f}")
                print(f"       • Points Expiring Soon: {random.randint(100, 500)} (by March 31, 2026)")
                print(f"       • Redemption Options: Shopping vouchers, Travel bookings, Bill payments\n")
        
        # Statement query
        elif any(word in query_lower for word in ['statement', 'bill', 'due date', 'payment']):
            due_date = "March 15, 2026"
            amount_due = random.randint(5000, 25000)
            min_due = amount_due * 0.05
            print(f"Agent: Here are your statement details:\n")
            print(f"       • Statement Date: February 5, 2026")
            print(f"       • Due Date: {due_date}")
            print(f"       • Total Amount Due: ₹{amount_due:,.2f}")
            print(f"       • Minimum Amount Due: ₹{min_due:.2f}")
            print(f"       • Last Payment: ₹{random.randint(3000, 8000):,.2f} on January 10, 2026\n")
        
        # Credit limit query
        elif any(word in query_lower for word in ['credit limit', 'limit', 'available credit']):
            total_limit = random.randint(100000, 500000)
            used = random.randint(20000, 80000)
            available = total_limit - used
            utilization = (used / total_limit) * 100
            print(f"Agent: Here are your credit limit details:\n")
            print(f"       • Total Credit Limit: ₹{total_limit:,}")
            print(f"       • Used Credit: ₹{used:,}")
            print(f"       • Available Credit: ₹{available:,}")
            print(f"       • Credit Utilization: {utilization:.1f}%")
            print(f"       • Recommendation: {'Good! Keep utilization below 30%' if utilization < 30 else 'Consider paying down balance'}\n")
        
        # Card details query
        elif any(word in query_lower for word in ['card details', 'card type', 'expiry', 'validity']):
            print(f"Agent: Here are your card details:\n")
            print(f"       • Card Type: Platinum Credit Card")
            print(f"       • Card Number: XXXX XXXX XXXX {self.last_4}")
            print(f"       • Expiry Date: 12/2028")
            print(f"       • Card Status: Active")
            print(f"       • Annual Fee: ₹2,500 (Waived for this year)\n")
        
        # Transaction history query
        elif any(word in query_lower for word in ['transaction', 'history', 'recent']):
            transactions = get_transactions(self.customer_id)
            print(f"Agent: Here are your recent transactions:\n")
            for idx, txn in enumerate(transactions[:5], 1):
                print(f"       {idx}. ₹{txn['amount']:.2f} at {txn['merchant']} on {txn['date']} - {txn['status'].upper()}")
            print()
        
        # Interest rate query
        elif any(word in query_lower for word in ['interest', 'rate', 'apr', 'charges']):
            print(f"Agent: Here are your interest rate details:\n")
            print(f"       • Purchase APR: 3.5% per month (42% annually)")
            print(f"       • Cash Advance APR: 3.75% per month")
            print(f"       • Late Payment Fee: ₹500")
            print(f"       • Over Limit Fee: ₹500")
            print(f"       • Foreign Transaction Fee: 3.5% of transaction amount\n")
        
        # Generic query
        else:
            print(f"Agent: I understand you're asking about '{query}'.")
            print(f"Agent: Let me provide you with the relevant information.\n")
            print(f"       For detailed assistance with this query, I recommend:")
            print(f"       • Visiting our website: www.bank.com")
            print(f"       • Calling our 24/7 helpline: 1800-XXX-XXXX")
            print(f"       • Visiting your nearest branch\n")
            print(f"Agent: I can also connect you with a specialist for detailed guidance.")
            print(f"Agent: Your reference number is: REF" + str(random.randint(100000, 999999)) + "\n")
    
    def share_prevention_tips(self):
        """Share fraud prevention tips"""
        print("🛡️  Fraud Prevention Tips:")
        print("   1. Never share your CVV, PIN, or OTP with anyone")
        print("   2. Enable SMS/email alerts for all transactions")
        print("   3. Regularly review your transaction history")
        print("   4. Use secure networks for online transactions")
        print("   5. Report suspicious activity immediately")
        print("   6. Keep your contact details updated with the bank\n")
        
        print("Agent: Thank you for your cooperation. Stay safe!")

if __name__ == "__main__":
    agent = UnifiedCustomerSupportAgent()
    agent.run()
