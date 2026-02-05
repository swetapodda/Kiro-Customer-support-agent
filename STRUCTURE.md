# Project Structure

```
Kiro-Customer-support-agent/
│
├── 📂 src/                          # SOURCE CODE
│   ├── unified_agent.py             # Main agent (run this)
│   └── tools.py                     # Helper functions
│
├── 📂 knowledge_base/               # KNOWLEDGE BASE (RAG)
│   ├── __init__.py
│   ├── customers.py                 # Customer data + reward points
│   ├── transactions.py              # Transaction history
│   ├── policies.py                  # All policies (fraud, compliance, SLA)
│   ├── rag_retriever.py             # RAG system
│   ├── README.md
│   └── *.md                         # Policy documents (7 files)
│
├── 📂 docs/                         # DOCUMENTATION
│   ├── PROJECT_SUMMARY.md           # ⭐ Complete guide with test data
│   ├── UNIFIED_AGENT_GUIDE.md       # Agent usage guide
│   ├── ARCHITECTURE.md              # System architecture
│   ├── HOW_TO_RUN.md               # Setup instructions
│   └── README.md                    # General readme
│
├── 📄 README.md                     # Quick start guide
├── 📄 requirements.txt              # Python dependencies
├── 📄 .env                          # API key configuration
├── 📄 RUN_AGENT.bat                # ⭐ Run this to start
└── 📄 .gitignore                    # Git ignore rules
```

## 🎯 Key Files

### To Run:
- **RUN_AGENT.bat** - Double-click to start
- **src/unified_agent.py** - Main agent code

### To Understand:
- **README.md** - Quick overview
- **docs/PROJECT_SUMMARY.md** - Complete guide with test data and flows

### To Modify:
- **src/unified_agent.py** - Agent logic
- **knowledge_base/customers.py** - Customer data
- **knowledge_base/transactions.py** - Transaction data
- **knowledge_base/policies.py** - Policies and rules

## 📊 Separation

✅ **Code** → `src/` folder  
✅ **Knowledge** → `knowledge_base/` folder  
✅ **Documentation** → `docs/` folder  
✅ **Configuration** → Root level (`.env`, `requirements.txt`)
