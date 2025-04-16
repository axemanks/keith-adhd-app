import os
from typing import List, Tuple, Union

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from quart import Blueprint, Response, jsonify, request

# Import the actual tool implementations
from app.backend.services.tools import (
    get_memory,
    mark_task_done,
    schedule_goal,
    store_memory,
    web_search,
)

bp = Blueprint('assistant', __name__, url_prefix='/api/assistant')

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))

# Initialize conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Define tools with actual implementations
tools: List[Tool] = [
    Tool(
        name="schedule_goal",
        func=schedule_goal,
        description="Break down a goal into steps and schedule them",
    ),
    Tool(name="mark_task_done", func=mark_task_done, description="Mark a task or step as complete"),
    Tool(
        name="store_memory", func=store_memory, description="Store a memory in the long-term memory"
    ),
    Tool(name="get_memory", func=get_memory, description="Retrieve a memory from long-term memory"),
    Tool(
        name="web_search", func=web_search, description="Search the web for real-time information"
    ),
]

# Create the agent prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an ADHD Productivity Assistant. Your goal is to help users manage their tasks,
    stay focused, and maintain productivity. You can:
    1. Break down goals into manageable steps
    2. Schedule tasks and set reminders
    3. Store and retrieve important information
    4. Search the web for relevant information

    Always be supportive, clear, and concise in your responses.""",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create the agent
agent = create_openai_functions_agent(llm, tools, prompt)
# Use type ignore for the agent type incompatibility since it's a LangChain version mismatch
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)  # type: ignore


@bp.route('/message', methods=['POST'])
async def handle_message() -> Union[Response, Tuple[Response, int]]:
    try:
        data = await request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400

        user_message = data['message']

        # Process the message with the agent
        response = await agent_executor.ainvoke({"input": user_message})

        return jsonify({'response': response['output'], 'status': 'success'})

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500
