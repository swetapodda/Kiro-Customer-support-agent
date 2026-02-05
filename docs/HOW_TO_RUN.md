# How to Run the Agent

## 🚀 Quick Start

### Method 1: Batch File (Windows - Easiest)

**Just double-click**: `RUN_AGENT.bat`

Or from Command Prompt:
```cmd
RUN_AGENT.bat
```

Or from PowerShell:
```powershell
.\RUN_AGENT.bat
```

---

### Method 2: Python Directly

```bash
python main.py
```

Then select:
- **1** for Fraud Demo
- **2** for Clarification Demo
- **3** for Interactive Mode

---

### Method 3: Test First

```bash
python test_agent.py
```

This verifies everything is working before running the agent.

---

## 📋 What Each Method Does

### RUN_AGENT.bat
```
1. Checks if .env file exists
2. Runs python main.py
3. Shows menu to select mode
4. Pauses at end so you can see results
```

### python main.py
```
1. Loads .env file automatically
2. Shows menu to select mode
3. Runs selected demo or interactive mode
```

### python test_agent.py
```
1. Tests all imports
2. Checks API key
3. Tests tools
4. Tests LLM connection
5. Shows ✓ or ✗ for each test
```

---

## 🎯 Step-by-Step Guide

### First Time Setup

1. **Make sure .env file has your API key**
   ```bash
   # Check if .env exists
   dir .env
   
   # View contents (optional)
   type .env
   ```

2. **Test everything works**
   ```bash
   python test_agent.py
   ```
   
   Expected output:
   ```
   ✓ langgraph
   ✓ langchain
   ✓ langchain-google-genai
   ✓ chromadb
   ✓ GEMINI_API_KEY found
   ✓ verify_customer working
   ✓ fetch_recent_transactions working
   ✓ Gemini API connected: Hello
   ```

3. **Run the agent**
   ```bash
   RUN_AGENT.bat
   ```
   
   Or:
   ```bash
   python main.py
   ```

---

## 🎮 Demo Modes

### Option 1: Fraud Scenario (Automated)
```
- Pre-populated with test data
- Shows complete fraud detection workflow
- Card blocking + dispute creation
- ~5-8 seconds execution
```

**Test Credentials**: Already set (John Doe, 9876543210/1234)

---

### Option 2: Clarification Scenario (Automated)
```
- Pre-populated with test data
- Shows low-risk transaction inquiry
- No unnecessary actions
- Professional handling
```

**Test Credentials**: Already set (Jane Smith, 9998887776/5678)

---

### Option 3: Interactive Mode (User Input)
```
- You type responses
- Natural conversation
- Real-time AI classification
- Full control over flow
```

**You provide**:
- Mobile number
- Last 4 digits
- Your concern
- Confirmations

---

## 🔧 Troubleshooting

### Issue: "python is not recognized"

**Solution**: Python not in PATH. Use full path:
```cmd
C:\Users\SwetaPoddar\AppData\Local\Programs\Python\Python312\python.exe main.py
```

Or add Python to PATH.

---

### Issue: ".env file not found"

**Solution**: Create .env file:
```cmd
copy .env.example .env
```

Then edit `.env` and add your API key.

---

### Issue: "API key not valid"

**Solution**: 
1. Get new key from https://makersuite.google.com/app/apikey
2. Edit `.env` file
3. Replace with actual key
4. Run `python test_agent.py` to verify

---

### Issue: "Module not found"

**Solution**: Install dependencies:
```cmd
pip install -r requirements.txt
```

---

## 📁 File Locations

```
project/
├── RUN_AGENT.bat          ← Double-click this!
├── main.py                ← Or run this with Python
├── test_agent.py          ← Test setup first
├── .env                   ← Your API key here
└── requirements.txt       ← Dependencies
```

---

## 💡 Quick Commands Reference

```bash
# Test setup
python test_agent.py

# Run with batch file
RUN_AGENT.bat

# Run with Python
python main.py

# Install dependencies
pip install -r requirements.txt

# Check .env file
type .env

# Create .env from example
copy .env.example .env
```

---

## 🎯 Recommended Workflow

**First Time**:
1. ✅ Create/edit `.env` file with API key
2. ✅ Run `python test_agent.py` to verify
3. ✅ Run `RUN_AGENT.bat` or `python main.py`
4. ✅ Select option 1 for quick demo

**Every Time After**:
1. ✅ Just run `RUN_AGENT.bat` or `python main.py`
2. ✅ Select your preferred mode

---

## 🎬 What You'll See

### When you run RUN_AGENT.bat:

```
============================================================
Credit Card Customer Support Agent
============================================================

.env file found ✓
Starting agent...

Select mode:
1. Demo - Fraud Scenario
2. Demo - Clarification Scenario
3. Interactive Mode

Enter choice (1-3):
```

### After selecting option 1:

```
============================================================
Credit Card Customer Support Agent - Demo
============================================================

Scenario: Unauthorized Transaction Alert

--- Conversation Flow ---

Agent: Hello! I'm your Credit Card Customer Support Agent...

Agent: Thank you, John Doe. Your identity has been verified.

Agent: Here are your recent transactions:
1. 2026-01-23 - $1250.00 at Amazon (completed)
2. 2026-01-22 - $450.50 at Starbucks (completed)
3. 2026-01-21 - $8900.00 at Unknown Merchant XYZ (pending)

Agent: I understand this is concerning...

Agent: Actions taken:
- Card blocked - Ticket: BLK234886
- Dispute raised - Ticket: DSP354369

--- Final State ---
Verified: True
Customer ID: CUST001
Intent: Intent.UNAUTHORIZED_TRANSACTION
Sentiment: Sentiment.CALM
Risk Level: RiskLevel.HIGH
Actions Taken: ['Card blocked...', 'Dispute raised...']
Escalated: False

Press any key to continue...
```

---

## ✅ Summary

**Easiest way**: Just **double-click `RUN_AGENT.bat`**

**Alternative**: Run `python main.py` from terminal

**Test first**: Run `python test_agent.py` to verify setup

That's it! 🚀
