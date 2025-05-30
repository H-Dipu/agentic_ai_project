# ✅ Agentic AI Setup Guide (Windows)

This guide will help you install and run an Agentic AI system using LangChain, OpenAI, and Wikipedia as a tool.

---

📁 STEP 1: Create Project Folder and Virtual Environment

Open Command Prompt or PowerShell and run:

    mkdir agentic_ai_project
    cd agentic_ai_project
    python -m venv venv
    venv\Scripts\activate

---

📦 STEP 2: Install Required Packages

    pip install langchain langchain-community langchain-openai openai wikipedia python-dotenv

---

🗝️ STEP 3: Create `.env` File to Store API Key

1. Inside the `agentic_ai_project` folder, create a file named:

       .env

2. Add the following line (replace with your own OpenAI API key):

       OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

---

🧠 STEP 4: Create `agent.py` Script

Create a new file called:

    agent.py

Paste the following code inside:

------------------------------------------------------

import os
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OPENAI_API_KEY in .env file")

from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

# Wikipedia tool setup
wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = [
    Tool(
        name="Wikipedia",
        func=wiki_tool.run,
        description="Useful for looking up general knowledge."
    )
]

# GPT model setup
llm = ChatOpenAI(temperature=0, openai_api_key=api_key)

# Zero-shot agent (no memory)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Ask initial question
goal = "What are the top AI coding assistants and what makes them unique?"
response = agent.invoke(goal)
print("\n🔍 Zero-Shot Agent's Answer:\n", response)

# Add memory (optional follow-up conversation)
memory = ConversationBufferMemory(memory_key="chat_history")

agent_with_memory = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# Follow-up questions
agent_with_memory.invoke("Tell me about GitHub Copilot")
agent_with_memory.invoke("What else do you know about coding assistants?")

------------------------------------------------------

---

▶️ STEP 5: Run Your Agent

In the terminal, from inside the project folder:

    python agent.py

You should see output from the agent fetching info from Wikipedia using GPT.

---

📌 Tips

- To exit the virtual environment: `deactivate`
- To run again later:
    cd agentic_ai_project  
    venv\Scripts\activate  
    python agent.py

---

🛠️ Troubleshooting

- **Quota error 429**: Your OpenAI API key has no remaining quota. Visit https://platform.openai.com/account/billing to add a payment method.
- **Deprecation warnings**: This script uses the latest stable imports; older methods are deprecated by LangChain v0.2+

---

🧠 Built With:
- LangChain
- LangChain-Community
- LangChain-OpenAI
- Wikipedia API
- dotenv for key management

---

🎉 You're now ready to build and extend your own Agentic AI system!
