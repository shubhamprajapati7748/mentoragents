from typing import Literal
from langgraph.graph import END
from mentoragents.workflow.state import MentorState
from mentoragents.core.config import settings

def should_summarize_conversation(
    state: MentorState,
) -> Literal["summarize_conversations_node", "__end__"]:
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversations_node"

    return END
