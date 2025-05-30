from dotenv import load_dotenv
import os

from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

from langchain_community.chat_models import ChatOpenAI  # ✅ UPDATED
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory


# Load environment variable
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Wikipedia tool setup
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = [
    Tool(
        name="Wikipedia",
        func=wiki.run,
        description="Useful for looking up general knowledge."
    )
]

# GPT model setup
llm = ChatOpenAI(temperature=0, openai_api_key=api_key)

# Agent without memory (Zero-shot)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run a query
goal = "What are the top AI coding assistants and what makes them unique?"
response = agent.run(goal)
print("\nZero-shot Agent Response:\n", response)

# Agent with memory (follow-up capable)
memory = ConversationBufferMemory(memory_key="chat_history")

agent_with_memory = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# Follow-up examples
agent_with_memory.run("Tell me about GitHub Copilot")
agent_with_memory.run("What else do you know about coding assistants?")
