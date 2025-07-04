from langgraph.graph import MessagesState

class MentorState(MessagesState):
    """
    A class that contains the state for the Mentor State for the Mentor Agent.
    """
    mentor_name : str 
    mentor_expertise : str
    mentor_perspective : str 
    mentor_style : str 
    mentor_context : str 
    summary : str  


def state_to_str(state: MentorState) -> str:
    if "summary" in state and bool(state["summary"]):
        conversation = state["summary"]
    elif "messages" in state and bool(state["messages"]):
        conversation = state["messages"]
    else:
        conversation = ""

    return f"""
        MentorState(mentor_context={state["mentor_context"]}, 
        mentor_name={state["mentor_name"]}, 
        mentor_expertise={state["mentor_expertise"]}, 
        mentor_perspective={state["mentor_perspective"]}, 
        mentor_style={state["mentor_style"]}, 
        conversation={conversation})
        """