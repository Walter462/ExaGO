"""
Agent workflow thinking graph.
"""

from langgraph.graph import END, START, StateGraph
from agent.state import State
from agent.nodes import tool_node
from agent.nodes import llm_call
from agent.nodes import should_continue
import logging
from agent import logger


# Build and compile agent
agent_builder = StateGraph(State)
# Add nodes
agent_builder.add_node("LLM", llm_call)
agent_builder.add_node("SQL tools", tool_node)
# Add edges to connect nodes
agent_builder.add_edge(START, "LLM")
agent_builder.add_conditional_edges(
    "LLM",
    should_continue,
    ["SQL tools", END]
)
agent_builder.add_edge("SQL tools", "LLM")

# Compile the agent
agent = agent_builder.compile()
# Activate logging messages at certain level
logger = logger.default_server_logging(level=logging.DEBUG)

# Agent mermaid digram
logger.debug(f"""Current agent architecture mermaid diagram (copy/paste to a mermaid fenced block in a markdown document):
              \n{agent.get_graph().draw_mermaid()}""")
