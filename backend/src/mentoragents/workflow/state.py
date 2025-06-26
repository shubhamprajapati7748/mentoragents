from langgraph.graph import MessagesState

class MentorState(MessagesState):
    """
    A class that contains the state for the Mentor State for the Mentor Agent.
    """
    name : str 
    expertise : str
    perspective : str 
    style : str 
    context : str 
    summary : str  


def state_to_str(state : MentorState) -> str: 
    """Convert the MentorState to String"""
    return f"""
    MentorState(
        name = {state.name},
        expertise = {state.expertise},
        perspective = {state.perspective},
        style = {state.style},
        context = {state.context},
        summary = {state.summary}
    )
    """