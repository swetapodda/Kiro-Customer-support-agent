# Unified Customer Support Agent Guide

## Overview
This is the **recommended agent** that combines both General Enquiry and Fraud Transaction handling in one unified experience.

## Features

### Two Options at Start
When customer contacts support, they choose:
1. **General Enquiry** - Reward points, statement, credit limit, etc.
2. **Fraud Transaction** - Report suspicious transaction

## Flow Diagrams

### Option 1: General Enquiry Flow
```
Customer selects "General Enquiry"
        ↓
Asks what they need help with
        ↓
Identity Verification (3 retries)
        ↓
Silent Background Risk Check
        ↓
Suspicious Activity Found?
    ↙           ↘
  YES            NO
    ↓             ↓
Proactive Alert  Process Query
    ↓             ↓
"Was this you?"  All Good
    ↓
Customer Response
  ↙      ↘
YES      NO
  ↓       ↓
Safe   Fraud Flow
  ↓       ↓
Query  Block + Ticket
```

### Option 2: Fraud Transaction Flow
```
Customer selects "Fraud Transaction"
        ↓
Identity Verification (3 retries)
        ↓
Ask for transaction amount
        ↓
Search transaction in database
        ↓
Found?
  ↙    ↘
YES     NO
  ↓      ↓
Show   Retry once
  ↓      ↓
Confirm  Still not found?
  ↓      ↓
"Did you do this?"  Escalate
  ↙      ↘
YES      NO
  ↓       ↓
Safe   Fraud Flow
       ↓
   Block + Ticket
```

## Test Scenarios

### Scenario 1: General Enquiry with Proactive Safety Alert

**Customer**: CUST003 (Rajesh Kumar)
- Mobile: `9123456789`
- Last 4: `9012`
- Query: "I want to check my reward points"

**Background**: Has suspicious ₹18,900 international transaction

**Flow**:
1. Customer selects option 1 (General Enquiry)
2. Customer asks about reward points
3. Agent verifies identity
4. Agent silently detects suspicious transaction
5. Agent calmly alerts: "A charge of ₹18,900 at an overseas merchant was made last night. Was this done by you?"
6. Customer says "No"
7. Agent explains protection steps
8. Customer consents
9. Agent blocks card + raises ticket
10. Agent shares ticket ID, SLA, zero liability
11. Agent shares prevention tips

**Test Input**:
```
Option: 1
Query: I want to check my reward points
Mobile: 9123456789
Last 4: 9012
Was this you?: No
Consent: Yes
```

---

### Scenario 2: General Enquiry - No Suspicious Activity

**Customer**: CUST002 (Jane Smith)
- Mobile: `9998887776`
- Last 4: `5678`
- Query: "What is my statement date?"

**Background**: All transactions legitimate

**Flow**:
1. Customer selects option 1 (General Enquiry)
2. Customer asks about statement date
3. Agent verifies identity
4. Agent finds no suspicious activity
5. Agent says "Good news! All transactions appear normal"
6. Agent processes original query
7. Agent asks if anything else needed

**Test Input**:
```
Option: 1
Query: What is my statement date?
Mobile: 9998887776
Last 4: 5678
Anything else?: No
```

---

### Scenario 3: Direct Fraud Report

**Customer**: CUST001 (John Doe)
- Mobile: `9876543210`
- Last 4: `1234`
- Suspicious Transaction: ₹8900 at Unknown Merchant XYZ

**Flow**:
1. Customer selects option 2 (Fraud Transaction)
2. Agent verifies identity
3. Agent asks for transaction amount
4. Customer provides: 8900
5. Agent finds and shows transaction details
6. Agent asks: "Did you perform this transaction?"
7. Customer says "No"
8. Agent explains protection steps
9. Customer consents
10. Agent blocks card + raises ticket
11. Agent shares ticket ID, SLA, prevention tips

**Test Input**:
```
Option: 2
Mobile: 9876543210
Last 4: 1234
Amount: 8900
Did you do this?: No
Consent: Yes
```

---

### Scenario 4: Fraud Report - Transaction Not Found

**Customer**: CUST001 (John Doe)
- Mobile: `9876543210`
- Last 4: `1234`
- Reports: ₹1000 (doesn't exist)

**Flow**:
1. Customer selects option 2 (Fraud Transaction)
2. Agent verifies identity
3. Agent asks for transaction amount
4. Customer provides: 1000
5. Agent can't find transaction
6. Agent asks: "Is there any other transaction that seems suspicious?"
7. Customer says "Yes"
8. Agent asks for amount again
9. Customer provides: 8900
10. Agent finds transaction and proceeds with fraud flow

**Test Input**:
```
Option: 2
Mobile: 9876543210
Last 4: 1234
Amount: 1000
Other transaction?: Yes
Amount: 8900
Did you do this?: No
Consent: Yes
```

## Running the Agent

### Option 1: Using Batch File
```bash
RUN_AGENT.bat
# Select option 1
```

### Option 2: Direct Python
```bash
python unified_agent.py
```

## Sample Conversations

### Example 1: General Enquiry with Fraud Detection

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
   • Block Reference: BLK123456
   • Fraud Ticket: DSP789012
   • Transaction Flagged: ₹18900.00

⏱️ Expected Resolution Timeline:
   • Fraud team review: Within 24 hours
   • Investigation completion: 5-7 business days
   • New card dispatch: 3-5 business days
   • New card delivery: 7-10 business days

🛡️  Customer Liability Protection:
   • Reported within 24h: Zero liability
   • Your case: Zero liability (reported immediately)

Agent: Your fraud ticket reference is DSP789012.
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

### Example 2: Direct Fraud Report

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
   • Card Status: BLOCKED (Card ending 1234)
   • Block Reference: BLK456789
   • Fraud Ticket: DSP123456
   • Transaction Flagged: ₹8900.00

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

## Key Features

### 1. Unified Experience
- Single entry point for all customer needs
- Clear option selection at start
- Seamless flow for both scenarios

### 2. Proactive Safety (Option 1)
- Silent background check during general queries
- Calm, non-alarming alerts
- Customer-first language

### 3. Direct Fraud Handling (Option 2)
- Fast track for fraud reports
- Transaction search and confirmation
- Retry logic if transaction not found

### 4. Compliance
- RBI guidelines: Customer consent mandatory
- PCI-DSS: Never ask CVV/PIN/OTP
- Zero liability protection
- All policies from RAG knowledge base

### 5. Customer Experience
- 3 retry attempts for identity verification
- Clear communication at every step
- Fraud prevention tips shared
- Reference numbers for tracking

## Test Data Summary

| Customer | Mobile | Last 4 | Scenario |
|----------|--------|--------|----------|
| John Doe | 9876543210 | 1234 | Has ₹8900 suspicious transaction |
| Jane Smith | 9998887776 | 5678 | All transactions legitimate |
| Rajesh Kumar | 9123456789 | 9012 | Has ₹18,900 international late-night transaction |

## Benefits

1. **Flexibility**: Handles both general queries and fraud reports
2. **Proactive**: Detects fraud even when customer doesn't report it
3. **Efficient**: Single agent for all scenarios
4. **Compliant**: Follows all RBI and PCI-DSS guidelines
5. **User-Friendly**: Clear options and smooth flow
