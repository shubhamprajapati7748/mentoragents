from mentoragents.workflow.state import MentorState 
from mentoragents.core.config import settings
from mentoragents.workflow.chains import Chains
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from mentoragents.workflow.tools import Tools
from loguru import logger

class Nodes:
    """
    A class that contains the nodes for the workflow.
    """
    def __init__(self):
        self.chains = Chains()
        self.tools = Tools().get_tools()
    
    async def conversation_node(self, state : MentorState, config : RunnableConfig) -> MentorState: 
        """
        Node to handle the conversation between the mentor and the user.
        """
        logger.info(f"Conversation node called")
        summary = state.get("summary", "")
        conversation_chain = self.chains.get_mentor_response_chain()
        response = await conversation_chain.ainvoke(
            {
                "messages" : state["messages"],
                "summary" : summary,
                "mentor_name" : state["mentor_name"],
                "mentor_expertise" : state["mentor_expertise"],
                "mentor_perspective" : state["mentor_perspective"],
                "mentor_style" : state["mentor_style"],
            },
            config
        )
        state["messages"].append(response)
        logger.info(f"Conversation node completed")
        return state 
    

    async def retrieve_context_node(self, state : MentorState) -> MentorState:
        logger.info(f"Retrieve context node called")
        return ToolNode(self.tools)

    async def summarize_conversations_node(self, state : MentorState) -> MentorState: 
        """
        Node to handle the summarization of the conversation between the mentor and the user.
        """
        summary = state.get("summary", "")
        logger.info(f"Summarize conversations node called")
        summary_chain = self.chains.get_conversations_summary_chain(summary = summary)
        response = await summary_chain.ainvoke(
            {
                "messages" : state["messages"],
                "mentor_name" : state["mentor_name"],
                "summary" : summary
            }
        )

        delete_messages = [
            RemoveMessage(id = m.id)
            for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
        ]

        state["messages"] = delete_messages
        state["summary"] = response.content
        logger.info(f"Summarize conversations node completed")
        return state 
    
    async def summarize_context_node(self, state : MentorState) -> MentorState: 
        """
        Node to handle the summarization of the context.
        """
        logger.info(f"Summarize context node called")
        context_chain = self.chains.get_context_summary_chain() 
        response = await context_chain.ainvoke(
            {
                "context" : state["messages"][-1].content,
            }
        )
        state["messages"][-1].content = response.content
        logger.info(f"Summarize context node completed")
        return state 
    
    async def connector_node(self, state : MentorState) -> MentorState: 
        """
        Node to handle the connector.
        """
        return state 