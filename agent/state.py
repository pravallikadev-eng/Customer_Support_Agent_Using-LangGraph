from typing import TypedDict, List, Dict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    user_id: str
    thread_id: str
    messages: Annotated[List[Dict], add_messages]
    user_history: List[Dict]
    needs_human: bool
