# ResolveIQ



### AI Customer Support That Remembers What Already Happened

ResolveIQ is an AI-powered customer support agent designed to solve one of the biggest problems in traditional support systems: **customers repeatedly receive the same troubleshooting steps even when those steps have already failed.**

ResolveIQ uses **Hindsight memory** to remember customer history, previous issues, troubleshooting attempts, outcomes, preferences, and escalations.

Instead of starting every conversation from zero, ResolveIQ starts with context.

---

## 🚀 What is ResolveIQ?

Traditional customer support often works like this:

> Customer reports an issue → Agent suggests a solution → Solution fails → Customer contacts support again → Agent suggests the same solution.

ResolveIQ changes this workflow.

```text
Customer
   ↓
ResolveIQ Support Agent
   ↓
Recall Previous Customer History
   ↓
Understand Previous Attempts
   ↓
Avoid Failed Solutions
   ↓
Generate Next Best Support Action
   ↓
Store New Outcome
   ↓
Improve Future Conversations
🧠 The Core Idea
Don't Repeat Failed Solutions

Consider a customer experiencing a Wi-Fi problem.

During the first interaction:

Customer:
"My Wi-Fi keeps disconnecting."

Agent:
"Please restart your router."

Customer:
"I already restarted it multiple times."

Result:
Router restart did not solve the issue.

ResolveIQ stores this interaction in Hindsight.

Later, the same customer returns:

Customer:
"My Wi-Fi is still disconnecting."

Instead of recommending the same solution again, ResolveIQ recalls:

Previous issue:
Wi-Fi disconnections

Previous action:
Router restart

Outcome:
Did not solve the issue

The agent can then move to another troubleshooting step.

This makes the support experience context-aware and continuously improving.

✨ Key Features
🧠 Hindsight-Powered Memory

ResolveIQ uses Hindsight as its long-term memory layer.

It remembers:

Customer identity
Previous support conversations
Past tickets
Reported issues
Troubleshooting actions
Failed solutions
Successful solutions
Customer preferences
Escalations
Previous outcomes
👤 Customer Profiles

Each customer has a dedicated profile containing information such as:

Customer ID
Name
Email
Previous tickets
Support history
Known issues
Memory context
Escalation history

This allows the support agent to understand the customer before responding.

🎫 Ticket Management

ResolveIQ provides ticket management for support issues.

Each ticket can contain:

Ticket ID
Customer
Issue
Status
Priority
Created date
Updated date
Support events
Resolution information

Supported ticket states include:

Open
In Progress
Resolved
Escalated
💬 AI Support Desk

The Support Desk is the main interaction point.

A support agent can:

Select a customer
Enter the customer's issue
Retrieve relevant memory
Analyze previous attempts
Generate an AI response
Recommend the next action
Record the outcome
Escalate when required
🔍 Memory Explorer

ResolveIQ makes the memory layer visible instead of hiding it in the background.

The Memory Explorer allows support teams to inspect information stored in Hindsight.

This helps demonstrate how the system:

Interaction
     ↓
Memory
     ↓
Recall
     ↓
Decision
     ↓
New Outcome
     ↓
Updated Memory
🚨 Escalation Management

If an issue cannot be resolved automatically, ResolveIQ can escalate it.

Escalation information can include:

Ticket
Customer
Issue
Reason for escalation
Previous troubleshooting attempts
Relevant memory
AI response
Current status

This gives human support agents useful context instead of forcing them to start the investigation again.

🏗️ Architecture
                    ┌─────────────────────┐
                    │     Streamlit UI    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Support Agent     │
                    │                     │
                    │ Issue Understanding │
                    │ Decision Making      │
                    │ Response Generation  │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌─────────────────┐         ┌─────────────────┐
       │    Hindsight    │         │    Groq LLM     │
       │  Memory Layer   │         │                 │
       │                 │         │ Response        │
       │ Recall          │         │ Generation      │
       │ Retain          │         │                 │
       └────────┬────────┘         └────────┬────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    ┌─────────────────────┐
                    │ Support Resolution  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Store New Outcome   │
                    │ in Hindsight        │
                    └─────────────────────┘
🛠️ Technology Stack
Technology	Purpose
Python	Core application logic
Streamlit	Web application interface
Hindsight	Long-term AI memory
Groq	LLM inference
SQLite	Local application database
REST API	Hindsight integration
Git & GitHub	Version control
📁 Project Structure
resolveiq/
│
├── app/
│   ├── main.py
│   ├── agent.py
│   ├── database.py
│   ├── hindsight_service.py
│   ├── prompts.py
│   └── main_backup.py
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── resolveiq.db
Important Files
app/main.py

Contains the Streamlit application and user interface.

app/agent.py

Contains the support-agent logic responsible for processing customer issues and generating responses.

app/database.py

Handles local SQLite database operations including:

Customers
Tickets
Ticket events
Customer history
Ticket status
app/hindsight_service.py

Handles communication with the Hindsight memory system.

Main operations include:

Retaining memories
Recalling memories
Retrieving customer history
Storing support outcomes
Storing escalations
app/prompts.py

Contains prompts and instructions used by the AI support agent.

🔄 How ResolveIQ Works
Step 1: Customer Reports an Issue

The customer provides their support problem.

Example:

"My internet keeps disconnecting every few minutes."
Step 2: ResolveIQ Identifies the Customer

The system retrieves the customer's profile and previous support history.

Step 3: Hindsight Memory Recall

ResolveIQ queries Hindsight for relevant memories.

For example:

Previous issue:
Internet disconnection

Previous troubleshooting:
Router restart

Previous result:
Issue continued
Step 4: AI Analyzes the Context

The AI considers:

Current issue
Previous issues
Previous actions
Previous outcomes
Customer history
Step 5: Failed Solutions Are Avoided

If a previous troubleshooting action failed, the agent can avoid unnecessarily repeating it.

Step 6: Generate the Next Action

The agent produces a contextual response.

Example:

You have already restarted the router several times,
so let's skip that step.

Next, let's check whether the connection drops across
multiple devices or only one device.
Step 7: Store the New Outcome

The interaction and outcome are stored back into Hindsight.

This creates the learning loop:

Recall → Reason → Respond → Observe → Retain
🧩 Memory Strategy

ResolveIQ treats memory as a core part of the support workflow.

The system can maintain information such as:

Customer Facts
      +
Past Issues
      +
Actions Taken
      +
Action Outcomes
      +
Preferences
      +
Escalations
      ↓
Customer Support Context

This allows future conversations to benefit from previous interactions.

🗄️ Database

ResolveIQ uses SQLite for structured application data.

The database stores entities such as:

Customers
Tickets
Ticket Events

Hindsight is used for long-term conversational and support memory, while SQLite handles structured application data.

🔐 Environment Variables

Create a .env file in the project root.

Example:

HINDSIGHT_API_KEY=your_hindsight_api_key
GROQ_API_KEY=your_groq_api_key

Never commit your .env file to GitHub.

The .gitignore file should contain:

.env
.venv/
__pycache__/
*.pyc
.DS_Store
resolveiq.db
⚙️ Installation
1. Clone the Repository
git clone https://github.com/AbhiramChowdaryBoppana/ResolveIQ.git
cd ResolveIQ
2. Create a Virtual Environment
python3 -m venv .venv

Activate it:

macOS / Linux
source .venv/bin/activate
Windows
.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create:

.env

Add your API credentials:

HINDSIGHT_API_KEY=your_hindsight_api_key
GROQ_API_KEY=your_groq_api_key
▶️ Running the Application

Initialize the database:

python app/database.py

Start the Streamlit application:

python -m streamlit run app/main.py

The application will open in your browser.

🖥️ Application Modules

ResolveIQ contains several main modules.

Dashboard

Provides an overview of:

Customers
Tickets
Open issues
Resolved issues
Escalations
Recent activity
Customers

Manage customer profiles and view their support history.

Tickets

View and manage support tickets.

Support Desk

Interact with the AI support agent.

Memory

Explore customer memories stored through Hindsight.

Escalations

Review issues that require human support intervention.

🎯 Why Memory Matters

Most support systems remember structured information such as:

Customer ID
Ticket ID
Status

ResolveIQ goes further by remembering the experience behind the ticket.

For example:

Problem:
Wi-Fi disconnects frequently

Attempt:
Restarted router

Result:
Failed

Attempt:
Changed DNS settings

Result:
Successful

When the customer returns, the agent has useful historical context.

The goal is simple:

Support should remember what already happened.

🌱 Continuous Learning Loop

ResolveIQ is designed around a continuous feedback loop.

┌──────────────┐
│ Customer     │
│ reports issue│
└──────┬───────┘
       ↓
┌──────────────┐
│ Recall       │
│ Memory       │
└──────┬───────┘
       ↓
┌──────────────┐
│ AI Reasoning │
└──────┬───────┘
       ↓
┌──────────────┐
│ Support      │
│ Action       │
└──────┬───────┘
       ↓
┌──────────────┐
│ Outcome      │
└──────┬───────┘
       ↓
┌──────────────┐
│ Retain       │
│ New Memory   │
└──────┬───────┘
       │
       └──────────────► Future Conversations

Every interaction can contribute useful context for future support.

📊 Example Scenario
First Conversation

Customer

My Wi-Fi is disconnecting.

ResolveIQ

Try restarting your router.

Customer

I already tried that.

ResolveIQ

Understood. I'll record that the router restart
did not resolve the issue and move to another
troubleshooting step.
Later Conversation

Customer

The Wi-Fi is still disconnecting.

ResolveIQ recalls:

Router restart → Failed

Instead of repeating the same instruction, it moves forward with another diagnostic step.

🔮 Future Improvements

Potential future improvements include:

More advanced support workflows
Automatic ticket categorization
Sentiment-aware support
Multi-agent support workflows
Knowledge-base integration
Customer preference learning
Automated escalation routing
Analytics for repeated support failures
Support performance dashboards
Voice-based customer support
Integration with CRM platforms
🔒 Security

ResolveIQ is designed to keep sensitive credentials outside the source code.

API keys should be stored in environment variables.

Never commit:

.env
API keys
Access tokens
Database credentials
Private credentials
📌 Project Goal

ResolveIQ aims to make AI customer support more useful by giving the support agent something traditional chatbots often lack:

memory of what already happened.

Instead of treating every support conversation as a new conversation, ResolveIQ builds context across interactions and uses that context to make future support more informed.

💡 Core Principle
Don't just answer the customer.

Remember the customer.
Remember the problem.
Remember what was tried.
Remember what failed.
Remember what worked.

Then use that memory the next time.
👨‍💻 Developer

Abhiram Chowdary Boppana

AI & Data Science
KL University

GitHub:

https://github.com/AbhiramChowdaryBoppana

⭐ ResolveIQ
Support that remembers what already happened.
