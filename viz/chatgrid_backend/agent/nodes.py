"""
Graph nodes
"""

# LangChain imports
from langchain.chat_models import init_chat_model
from langchain.messages import  HumanMessage, AIMessage, SystemMessage, ToolMessage

from langgraph.graph import END, START, StateGraph
from typing import Literal, Dict, Any, TypedDict, Annotated, Sequence, Optional

from agent.state import State
from agent.tools import test_database_connection
from agent.tools import list_databases
from agent.tools import get_database_tables
from agent.tools import get_postgres_schema
from agent.prompts import SYSTEM_PROMPT


# SQL tools
tools = [test_database_connection, list_databases, get_database_tables, get_postgres_schema]
tools_by_name = {tool.name: tool for tool in tools}

def tool_node(state: State):
    """Performs the tool call"""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


# LLM node
# tools = [add, multiply, divide, get_postgres_schema, get_user_tables_schema]
model = init_chat_model(model="gpt-5-nano",
                        temperature = 0)
model_with_tools = model.bind_tools(tools)

def llm_call(state: State) -> State:
    """LLM decides whether to call a tool or not"""
    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content=SYSTEM_PROMPT
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }

# Define end logic (conditional edge)
def should_continue(state: State) -> Literal["addition", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "SQL tools"

    # Otherwise, stop (reply to the user)
    return END
