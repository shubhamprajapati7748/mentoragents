from typing import Literal
from langgraph.graph import END
from src.mentoragents.workflow.state import MentorState
from src.mentoragents.core.config import settings

def should_summarize_conversation(
    state: MentorState,
) -> Literal["summarize_conversation_node", "__end__"]:
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"

    return END
