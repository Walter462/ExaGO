"""
Graph state definition
"""
import operator
from typing import Literal, Dict, Any, TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import AnyMessage, BaseMessage


class State(TypedDict):
	""" 
	Data structure to be filled and changed by LangGraph nodes.
	"""
	messages: Annotated[list[AnyMessage], operator.add]
	llm_calls: int