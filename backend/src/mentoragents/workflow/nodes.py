from src.mentoragents.workflow.state import MentorState 
from src.mentoragents.core.config import settings
from src.mentoragents.workflow.chains import Chains
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig

class Nodes:
    """
    A class that contains the nodes for the workflow.
    """
    def __init__(self):
        self.chains = Chains()
        self.config = RunnableConfig
    
    async def conversation_node(self, state : MentorState) -> MentorState: 
        """
        Node to handle the conversation between the mentor and the user.
        """
        conversation_chain = self.chains.get_mentor_resonse_chain()
        response = await conversation_chain.ainvoke(
            {
                "messages" : state["messages"],
                "mentor_name" : state["mentor_name"],
                "mentor_expertise" : state["mentor_expertise"],
                "mentor_perspective" : state["mentor_perspective"],
                "mentor_talking_style" : state["mentor_talking_style"],
                "summary" : state.get("summary", ""),
            },
            config = self.config
        )
        state["messages"].append(response)
        return state 
      

    async def summarize_conversation_node(self, state : MentorState) -> MentorState: 
        """
        Node to handle the summarization of the conversation between the mentor and the user.
        """
        summary = state.get("summary", "")
        summary_chain = self.chains.get_conversations_summary_chain(summary = summary)
        response = await summary_chain.ainvoke(
            {
                "messages" : state["messages"],
                "mentor_name" : state["mentor_name"],
                "summary" : summary,
            },
            config = self.config
        )

        delete_messages = [
            RemoveMessage(id = m.id)
            for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
        ]

        state["messages"] = delete_messages
        state["summary"] = response.content
        return state 
    
    async def summarize_context_node(self, state : MentorState) -> MentorState: 
        """
        Node to handle the summarization of the context.
        """
        context_chain = self.chains.get_context_summary_chain() 
        response = await context_chain.ainvoke(
            {
                "context" : state["messages"][-1].content,
            }
        )
        state["messages"][-1].content = response.content
        return state 
    
    async def connector_node(self, state : MentorState) -> MentorState: 
        """
        Node to handle the connector.
        """
        return state 