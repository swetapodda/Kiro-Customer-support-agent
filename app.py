"""Streamlit UI for Credit Card Customer Support Agent"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph_runner import AgentRunner

# Page configuration
st.set_page_config(
    page_title="Credit Card Support Agent",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better chat UI
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .agent-message {
        background-color: #f5f5f5;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_runner" not in st.session_state:
    st.session_state.agent_runner = AgentRunner()
if "conversation_stage" not in st.session_state:
    st.session_state.conversation_stage = "initial"
if "customer_verified" not in st.session_state:
    st.session_state.customer_verified = False
if "execution_trace" not in st.session_state:
    st.session_state.execution_trace = []

# Sidebar
with st.sidebar:
    st.title("💳 Credit Card Support")
    st.markdown("---")
    
    # Show execution trace toggle
    show_trace = st.checkbox("Show Execution Trace", value=False)
    
    st.markdown("---")
    
    # Customer info (if verified)
    if st.session_state.customer_verified:
        st.subheader("Customer Info")
        agent_state = st.session_state.agent_runner.get_state()
        if agent_state:
            st.write(f"**Name:** {agent_state.get('customer_name', 'N/A')}")
            st.write(f"**Customer ID:** {agent_state.get('customer_id', 'N/A')}")
            st.write(f"**Card:** XXXX XXXX XXXX {agent_state.get('last_4', 'N/A')}")
    
    st.markdown("---")
    
    # Clear conversation button
    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent_runner = AgentRunner()
        st.session_state.conversation_stage = "initial"
        st.session_state.customer_verified = False
        st.session_state.execution_trace = []
        st.rerun()
    
    st.markdown("---")
    st.caption("Powered by AI Agent")

# Main chat interface
st.title("Credit Card Customer Support Agent")
st.markdown("Welcome! I'm here to help you with your credit card queries and concerns.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show execution trace in sidebar if enabled
if show_trace and st.session_state.execution_trace:
    with st.sidebar:
        st.markdown("---")
        st.subheader("🔍 Execution Trace")
        for trace in st.session_state.execution_trace[-5:]:  # Show last 5 traces
            with st.expander(f"{trace['timestamp']} - {trace['action']}", expanded=False):
                st.json(trace['details'])

# Initial greeting
if not st.session_state.messages:
    initial_message = """Hello! Welcome to Credit Card Customer Support.

How can I help you today?

Please select an option:
1. General Enquiry (Reward points, Statement, Credit limit, etc.)
2. Fraud Transaction (Report suspicious transaction)

Type **1** or **2** to continue."""
    
    st.session_state.messages.append({"role": "assistant", "content": initial_message})
    with st.chat_message("assistant"):
        st.markdown(initial_message)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process user input through agent runner
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response, trace = st.session_state.agent_runner.process_input(
                prompt,
                st.session_state.conversation_stage
            )
            
            # Update conversation stage
            st.session_state.conversation_stage = st.session_state.agent_runner.current_stage
            
            # Update customer verification status
            if st.session_state.agent_runner.agent.customer_id:
                st.session_state.customer_verified = True
            
            # Add trace to execution trace
            if trace:
                st.session_state.execution_trace.append({
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "action": trace.get("action", "Unknown"),
                    "details": trace
                })
            
            # Display response
            st.markdown(response)
            
            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.caption("💡 Tip: Be specific with your queries for better assistance. All conversations are secure and confidential.")
