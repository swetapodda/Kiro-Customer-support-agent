# Credit Card Customer Support Agent

AI-powered Credit Card Customer Support Agent with RAG (Retrieval-Augmented Generation) for policy compliance.

## 🚀 Quick Start

```bash
# Run the agent
RUN_AGENT.bat

# Or directly with Python
python src/unified_agent.py
```

## 📁 Project Structure

```
├── src/                  # Source Code
│   ├── unified_agent.py  # Main agent
│   └── tools.py          # Helper functions
│
├── knowledge_base/       # RAG Knowledge Base
│   ├── customers.py      # Customer data
│   ├── transactions.py   # Transaction history
│   ├── policies.py       # Policies & compliance
│   └── rag_retriever.py  # RAG system
│
├── docs/                 # Documentation
│   └── PROJECT_SUMMARY.md  # Complete guide
│
├── requirements.txt      # Dependencies
├── .env                  # API key
└── RUN_AGENT.bat        # Run script
```

## 🎯 Features

### Two Options:
1. **General Enquiry** - Reward points, Statement, Credit limit, etc.
   - Proactive fraud detection during general queries
   - Silent background risk check
   
2. **Fraud Transaction** - Report suspicious transaction
   - Direct fraud reporting
   - Transaction search and validation

## 🧪 Test Data

| Customer | Mobile | Last 4 | Scenario |
|----------|--------|--------|----------|
| John Doe | 9876543210 | 1234 | Has ₹8,900 suspicious transaction |
| Jane Smith | 9998887776 | 5678 | All legitimate transactions |
| Rajesh Kumar | 9123456789 | 9012 | Has ₹18,900 international late-night transaction |

## 📖 Documentation

See `docs/PROJECT_SUMMARY.md` for:
- Complete flow diagrams
- Detailed test scenarios
- Sample conversations
- Compliance rules
- SLA timelines

## 🔧 Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

3. Run:
   ```bash
   RUN_AGENT.bat
   ```

## 🔐 Compliance

- ✅ RBI Guidelines (Customer consent, Zero liability)
- ✅ PCI-DSS (Never ask CVV/PIN/OTP)
- ✅ 3 retry attempts for identity verification

## 🛠️ Technology

- Python 3.12+
- Google Gemini (gemini-flash-latest)
- LangChain + RAG
- IBM KIRO Agentic IDE

---

**Version**: 1.0  
**Last Updated**: February 5, 2026
