# Credit Card Customer Support Agent - Complete Summary

## Project Overview
AI-powered Credit Card Customer Support Agent built using IBM KIRO Agentic IDE with RAG (Retrieval-Augmented Generation) for policy compliance.

---

## 🎯 Current Implementation

### Single Unified Agent (`unified_agent.py`)
The agent provides **2 main options** at startup:

1. **General Enquiry** - Reward points, Statement, Credit limit, etc.
2. **Fraud Transaction** - Report suspicious transaction

---

## 📊 Flow Diagrams

### Option 1: General Enquiry Flow (Proactive Safety Check)

```
Customer selects "General Enquiry"
        ↓
Customer asks query (e.g., "check reward points")
        ↓
Identity Verification (3 retry attempts)
        ↓
Silent Background Risk Check (RAG-based)
        ↓
Suspicious Activity Detected?
    ↙                    ↘
  YES                     NO
    ↓                      ↓
Proactive Alert      Process Query
    ↓                      ↓
"Was this you?"      Show Results
    ↓                      ↓
Customer Response    Anything else?
  ↙      ↘
YES      NO
  ↓       ↓
Safe   Fraud Flow
  ↓       ↓
Query  Block + Ticket + SLA
```

### Option 2: Fraud Transaction Flow (Direct Report)

```
Customer selects "Fraud Transaction"
        ↓
Identity Verification (3 retry attempts)
        ↓
Ask for transaction amount
        ↓
Search transaction in database
        ↓
Transaction Found?
  ↙              ↘
YES               NO
  ↓                ↓
Show Details    Retry Once
  ↓                ↓
"Did you do this?"  Still not found?
  ↙      ↘          ↓
YES      NO      Escalate
  ↓       ↓
Safe   Fraud Flow
       ↓
   Block + Ticket + SLA
```

---

## 🧪 Test Data

### Customer 1: John Doe (Fraud Scenario)
```
Mobile: 9876543210
Last 4: 1234
Card ID: CARD_1234
Email: john.doe@example.com

Reward Points:
  • Total: 12,500 points
  • Cashback: ₹3,125.00
  • Expiring: 450 points (by March 31, 2026)

Transactions:
  1. ₹1,250.00 at Amazon (Jan 23) - COMPLETED
  2. ₹450.50 at Starbucks (Jan 22) - COMPLETED
  3. ₹8,900.00 at Unknown Merchant XYZ (Jan 21) - PENDING ⚠️ SUSPICIOUS
```

**Test Scenario**: Direct fraud report
- Option: 2 (Fraud Transaction)
- Amount: 8900
- Expected: Agent finds transaction, customer denies, card blocked

---

### Customer 2: Jane Smith (Legitimate Transactions)
```
Mobile: 9998887776
Last 4: 5678
Card ID: CARD_5678
Email: jane.smith@example.com

Reward Points:
  • Total: 8,750 points
  • Cashback: ₹2,187.50
  • Expiring: 200 points (by March 31, 2026)

Transactions:
  1. ₹350.00 at Walmart (Jan 23) - COMPLETED
  2. ₹2,100.00 at Best Buy (Jan 20) - COMPLETED
```

**Test Scenario**: General enquiry, no fraud
- Option: 1 (General Enquiry)
- Query: "What is my statement date?"
- Expected: No suspicious activity, shows statement details

---

### Customer 3: Rajesh Kumar (Proactive Safety Alert)
```
Mobile: 9123456789
Last 4: 9012
Card ID: CARD_9012
Email: rajesh.kumar@example.com

Reward Points:
  • Total: 15,200 points
  • Cashback: ₹3,800.00
  • Expiring: 350 points (by March 31, 2026)

Transactions:
  1. ₹1,200.00 at Target (Feb 4) - COMPLETED
  2. ₹18,900.00 at GlobalTech Solutions Ltd (Feb 5, 2:30 AM) - PENDING ⚠️ HIGH RISK
     • Location: Singapore (International)
     • Time: Late night
     • Merchant: Newly added
     • Fraud Score: 0.75
```

**Test Scenario**: Proactive safety advisory
- Option: 1 (General Enquiry)
- Query: "I want to check my reward points"
- Expected: Agent detects ₹18,900 suspicious transaction, alerts customer calmly
- If customer denies: Card blocked, ticket raised, shows 15,200 reward points

---

## 🔍 Risk Detection Logic

Agent flags transactions as suspicious if **2 or more** risk factors present:

1. **High Fraud Score** (>0.7)
2. **International/Overseas** merchant
3. **Late-night** transaction
4. **Newly added** merchant
5. **High-value pending** (>₹5,000)
6. **Unknown** merchant

---

## 💡 General Query Handling

Agent can answer:

### 1. Reward Points
- Shows total points, cashback value, expiring points
- Retrieves from knowledge base (real data per customer)

### 2. Statement/Bill
- Shows due date, amount due, minimum payment
- Last payment details

### 3. Credit Limit
- Total limit, used credit, available credit
- Credit utilization percentage

### 4. Card Details
- Card type, expiry date, status
- Annual fee information

### 5. Transaction History
- Recent 5 transactions with details

### 6. Interest Rates
- APR, fees, charges

---

## 🔐 Compliance & Security

### RBI Guidelines
- ✅ Customer consent mandatory for all actions
- ✅ Zero liability for fraud reported within 24 hours
- ✅ Immediate notification required

### PCI-DSS
- ✅ Never ask for full card number
- ✅ Never ask for CVV, PIN, or OTP
- ✅ Only last 4 digits for verification

### Identity Verification
- ✅ 3 retry attempts
- ✅ Session ends after 3 failed attempts
- ✅ Directs to branch/helpline

---

## 📋 Fraud Resolution Process

When customer denies transaction:

1. **Explain Protection Steps**
   - Risk if card stays active
   - Protection measures available

2. **Get Consent** (RBI compliance)
   - "Shall I immediately block the card and raise a fraud verification request?"

3. **Execute Actions**
   - Block card immediately
   - Raise fraud verification ticket

4. **Share Details**
   - Ticket reference number
   - Expected resolution timeline (SLA from knowledge base)
   - Zero liability assurance

5. **Prevention Tips**
   - Never share CVV, PIN, OTP
   - Enable transaction alerts
   - Review transaction history regularly
   - Use secure networks
   - Report suspicious activity immediately
   - Keep contact details updated

---

## ⏱️ SLA Timelines (from Knowledge Base)

- **Card Block**: Immediate (within 2 minutes)
- **SMS Notification**: Within 5 minutes
- **Email Notification**: Within 30 minutes
- **Fraud Team Review**: Within 24 hours
- **Investigation Completion**: 5-7 business days
- **Provisional Credit**: Within 10 business days (if eligible)
- **New Card Dispatch**: 3-5 business days
- **New Card Delivery**: 7-10 business days
- **Final Resolution**: 30-45 days maximum

---

## 📁 Project Structure

```
Kiro-Customer-support-agent/
│
├── src/                     # Source Code
│   ├── unified_agent.py     # Main agent (only file needed to run)
│   └── tools.py             # Helper functions (verify, block, dispute)
│
├── knowledge_base/          # RAG Knowledge Base
│   ├── __init__.py
│   ├── customers.py         # Customer data with reward points
│   ├── transactions.py      # Transaction history
│   ├── policies.py          # All policies (fraud, compliance, SLA)
│   ├── rag_retriever.py     # RAG system
│   ├── README.md
│   └── *.md                 # Policy documents
│
├── docs/                    # Documentation
│   ├── PROJECT_SUMMARY.md   # This file
│   ├── UNIFIED_AGENT_GUIDE.md
│   ├── ARCHITECTURE.md
│   ├── HOW_TO_RUN.md
│   └── README.md
│
├── requirements.txt         # Python dependencies
├── .env                     # API key configuration
└── RUN_AGENT.bat           # Windows batch file to run agent
```

---

## 🚀 How to Run

### Method 1: Batch File (Recommended)
```bash
RUN_AGENT.bat
```

### Method 2: Direct Python
```bash
python src/unified_agent.py
```

### Prerequisites
1. Python 3.12+
2. `.env` file with `GOOGLE_API_KEY`
3. Install dependencies: `pip install -r requirements.txt`

---

## 🎬 Sample Conversations

### Scenario 1: Proactive Safety Alert

```
Agent: Hello! Welcome to Credit Card Customer Support.
Agent: How can I help you today?

Please select an option:
1. General Enquiry (Reward points, Statement, Credit limit, etc.)
2. Fraud Transaction (Report suspicious transaction)

You (Enter 1 or 2): 1

Agent: Sure! What would you like to know about?

You: I want to check my reward points

Agent: I'd be happy to help you with that.
Agent: Let me pull up your account details.

Agent: For security purposes, I need to verify your identity.
Agent: Please provide your registered mobile number and last 4 digits of your card.

You (Mobile Number): 9123456789
You (Last 4 Digits): 9012

Agent: Thank you, Rajesh Kumar. Identity verified.

Agent: One moment please... (Accessing your account)

Agent: Before we continue, I'd like to quickly confirm a recent transaction
       for your safety.

Agent: A charge of ₹18900.00 at an overseas merchant was made Late night.
Agent: Merchant: GlobalTech Solutions Ltd
Agent: Date: 2026-02-05 02:30 AM

Agent: Was this transaction done by you?

You (Yes/No): No

Agent: Thank you for letting me know. I understand your concern.

Agent: For your protection, I recommend we take immediate action.
Agent: Here's what I suggest:

       • Block your card to prevent further unauthorized charges
       • Raise a fraud verification request
       • Our fraud team will investigate within 24 hours
       • You'll have zero liability as per RBI guidelines

Agent: As per RBI guidelines: Mandatory for all actions

Agent: Shall I immediately block the card and raise a fraud verification request?
You (Yes/No): Yes

Agent: Thank you for your consent. Processing immediately...

✅ Actions Completed Successfully!

📋 Summary:
   • Card Status: BLOCKED (Card ending 9012)
   • Block Reference: BLK456789
   • Fraud Ticket: DSP123456
   • Transaction Flagged: ₹18900.00

⏱️ Expected Resolution Timeline:
   • Fraud team review: Within 24 hours
   • Investigation completion: 5-7 business days
   • New card dispatch: 3-5 business days
   • New card delivery: 7-10 business days

🛡️  Customer Liability Protection:
   • Reported within 24h: Zero liability
   • Your case: Zero liability (reported immediately)

Agent: Your fraud ticket reference is DSP123456.
Agent: You will receive SMS and email confirmations within 5 minutes.
Agent: Our fraud team will contact you within 24 hours if needed.

🛡️  Fraud Prevention Tips:
   1. Never share your CVV, PIN, or OTP with anyone
   2. Enable SMS/email alerts for all transactions
   3. Regularly review your transaction history
   4. Use secure networks for online transactions
   5. Report suspicious activity immediately
   6. Keep your contact details updated with the bank

Agent: Thank you for your cooperation. Stay safe!
```

---

### Scenario 2: Direct Fraud Report

```
Agent: Hello! Welcome to Credit Card Customer Support.
Agent: How can I help you today?

Please select an option:
1. General Enquiry (Reward points, Statement, Credit limit, etc.)
2. Fraud Transaction (Report suspicious transaction)

You (Enter 1 or 2): 2

Agent: I understand you received a suspicious transaction SMS.
Agent: Let me help you with that.

Agent: For security purposes, I need to verify your identity.
Agent: Please provide your registered mobile number and last 4 digits of your card.

You (Mobile Number): 9876543210
You (Last 4 Digits): 1234

Agent: Thank you, John Doe. Identity verified.

Agent: Can you please tell me about the transaction you're concerned about?
Agent: Please provide the transaction amount.

You (Amount in ₹): 8900

Agent: I found a transaction for ₹8900.00
Agent: Merchant: Unknown Merchant XYZ
Agent: Date: 2026-01-21
Agent: Status: PENDING

Agent: Did you perform this transaction?
You (Yes/No): No

[... Fraud resolution process continues as above ...]
```

---

### Scenario 3: General Enquiry - No Fraud

```
You (Enter 1 or 2): 1

Agent: Sure! What would you like to know about?

You: What is my statement date?

[... Identity verification ...]

Agent: One moment please... (Accessing your account)

✅ Agent: Good news! All your recent transactions appear normal.
Agent: Now, regarding your query about 'What is my statement date?'...

Agent: Here are your statement details:

       • Statement Date: February 5, 2026
       • Due Date: March 15, 2026
       • Total Amount Due: ₹15,234.00
       • Minimum Amount Due: ₹761.70
       • Last Payment: ₹5,000.00 on January 10, 2026

Agent: Is there anything else I can help you with today?
You (Yes/No): No

Agent: Thank you for contacting us. Have a great day!
```

---

## 🔑 Key Features

1. **Unified Experience** - Single agent for all scenarios
2. **Proactive Safety** - Detects fraud during general queries
3. **RAG-Powered** - All policies from knowledge base
4. **Compliant** - RBI + PCI-DSS guidelines
5. **User-Friendly** - Clear options, 3 retry attempts
6. **Real Data** - Actual reward points, transactions from KB
7. **Comprehensive** - Handles 6+ types of general queries

---

## 📊 Success Metrics

- ✅ Identity verification works correctly
- ✅ Fraud detection triggers on 2+ risk factors
- ✅ Customer consent obtained before actions
- ✅ Card blocked immediately
- ✅ Ticket raised with reference number
- ✅ SLA timelines shared from knowledge base
- ✅ Zero liability assurance provided
- ✅ Prevention tips shared
- ✅ General queries answered accurately

---

## 🛠️ Technology Stack

- **Language**: Python 3.12
- **LLM**: Google Gemini (gemini-flash-latest)
- **Framework**: LangChain + RAG
- **IDE**: IBM KIRO Agentic IDE
- **Knowledge Base**: Local Python modules
- **Compliance**: RBI + PCI-DSS

---

## 📝 Notes

- Agent uses **mock data** for demonstration
- In production, connect to real databases
- All policies retrieved from RAG knowledge base
- No hallucination - all responses based on KB
- Customer consent mandatory per RBI guidelines
- Never asks for CVV, PIN, or OTP (PCI-DSS)

---

**Last Updated**: February 5, 2026
**Version**: 1.0 (Unified Agent)
**Status**: Production Ready
