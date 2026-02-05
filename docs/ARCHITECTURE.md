# Agent Architecture

## Overview

This Credit Card Customer Support Agent uses **LangGraph** for state machine orchestration and **Google Gemini API** for LLM inference. The architecture follows a node-based workflow pattern.

## State Machine Flow

```
START
  ↓
Greeting
  ↓
Identity Verification ←─┐ (retry on failure)
  ↓                     │
  ├─ verified? ─────────┘
  ├─ escalate? → Escalation → Closure → END
  ↓
Intent Classification
  ↓
Sentiment Analysis
  ↓
  ├─ needs transactions? → Transaction Retrieval
  ↓                              ↓
Risk Assessment ←────────────────┘
  ↓
Action Recommendation
  ↓
  ├─ high risk? → Escalation
  ↓
Closure
  ↓
END
```

## Node Descriptions

### 1. Greeting Node
- Welcomes customer
- Introduces agent capabilities
- Sets friendly tone

### 2. Identity Verification Node
- Collects mobile number and last 4 digits
- Validates against customer database
- Allows 1 retry, then escalates
- **Tool**: `verify_customer(mobile, last4)`

### 3. Intent Classification Node
- Uses Gemini LLM to classify customer intent
- Categories:
  - Unauthorized transaction
  - Fraud suspicion
  - Card blocking request
  - Transaction clarification
  - General inquiry
- **LLM**: Gemini 1.5 Flash with zero-shot classification

### 4. Sentiment Analysis Node
- Analyzes emotional state from customer messages
- Categories: calm, worried, anxious, angry
- Influences empathy level and escalation priority
- **LLM**: Gemini 1.5 Flash with sentiment prompt

### 5. Transaction Retrieval Node
- Fetches recent transactions for verified customers
- Masks sensitive data (full card number)
- Displays date, amount, merchant, status
- **Tool**: `fetch_recent_transactions(customer_id)`

### 6. Risk Assessment Node
- Evaluates risk based on:
  - Intent type (fraud = HIGH)
  - Sentiment (anxious/angry = escalate)
  - Transaction patterns
- Outputs: LOW, MEDIUM, HIGH

### 7. Action Recommendation Node
- HIGH risk: Block card + raise dispute
- MEDIUM risk: Offer card blocking
- LOW risk: Provide information only
- **Tools**: 
  - `block_card(card_id)`
  - `raise_dispute_ticket(customer_id, transaction)`

### 8. Escalation Node
- Triggers when:
  - High emotional distress detected
  - Multiple unauthorized transactions
  - Customer explicitly requests human
  - Verification fails twice
- **Tool**: `escalate_to_human_agent(context)`

### 9. Closure Node
- Summarizes actions taken
- Provides ticket/reference numbers
- Explains next steps
- Offers additional help

## State Schema

```python
AgentState = {
    "messages": List[str],              # Agent responses
    "verified": bool,                   # Identity verified?
    "customer_id": Optional[str],       # Customer identifier
    "mobile_number": Optional[str],     # For verification
    "last_4_digits": Optional[str],     # For verification
    "intent": Optional[Intent],         # Classified intent
    "sentiment": Optional[Sentiment],   # Detected sentiment
    "risk_level": RiskLevel,            # LOW/MEDIUM/HIGH
    "transactions": List[dict],         # Recent transactions
    "actions_taken": List[str],         # Actions performed
    "escalated": bool,                  # Escalated to human?
    "conversation_history": List[dict], # Full conversation
    "retry_count": int                  # Verification retries
}
```

## Tools

All tools are mock implementations for demo purposes. In production:

1. **verify_customer**: Connect to customer identity service (OAuth, KYC)
2. **fetch_recent_transactions**: Query transaction database (PostgreSQL, DynamoDB)
3. **block_card**: Call card management API
4. **raise_dispute_ticket**: Create ticket in CRM system
5. **escalate_to_human_agent**: Route to live agent queue

## Security & Compliance

- ✅ No full card numbers exposed
- ✅ Identity verification before data access
- ✅ All sensitive data masked
- ✅ Audit trail via conversation_history
- ✅ PCI-DSS aligned (mock implementation)
- ✅ RBI guidelines compliant

## Technology Stack

| Component | Technology |
|-----------|-----------|
| LLM | Google Gemini 1.5 Flash (free tier) |
| Framework | LangGraph + LangChain |
| Vector DB | ChromaDB (local) |
| State Management | LangGraph StateGraph |
| Language | Python 3.8+ |

## Conditional Routing

The agent uses conditional edges for dynamic flow:

```python
should_continue_verification(state):
    if verified → intent_classification
    if escalated → escalation
    else → identity_verification (retry)

should_show_transactions(state):
    if intent in [fraud, clarification] → transaction_retrieval
    else → risk_assessment

should_escalate(state):
    if escalated → closure
    if high_risk → escalation
    else → closure
```

## Error Handling

- Verification failures: Max 2 retries → escalate
- LLM failures: Fallback to rule-based classification
- Tool failures: Log error, inform customer, escalate
- Timeout: Auto-escalate after 5 minutes

## Future Enhancements

1. **Vector DB Integration**: Store conversation embeddings in ChromaDB for similarity search
2. **Multi-turn Memory**: Use LangChain memory for context retention
3. **Voice Integration**: Add speech-to-text for phone calls
4. **Analytics Dashboard**: Track escalation rates, resolution times
5. **A/B Testing**: Test different empathy levels and response styles
