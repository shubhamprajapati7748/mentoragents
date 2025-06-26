

from functools import lru_cache 
from langgraph.graph import START, END, StateGraph 
from langgraph.prebuilt import tools_condition
from src.mentoragents.workflow.state import MentorState 
from src.mentoragents.workflow.edges import should_summarize_conversation
from src.mentoragents.workflow.nodes import Nodes

class MentorGraph:
    """
    A class that contains the graph for the Mentor Agent.
    """
    def __init__(self):
        """
        Initialize the graph.
        """
        self.graph_builder = StateGraph(MentorState)
        self.nodes = Nodes()
    
    @lru_cache(maxsize=1)
    def build(self) -> StateGraph:
        """Build the graph."""
        self.graph_builder.add_node("conversation_node", self.nodes.conversation_node)
        self.graph_builder.add_node("retrieve_context_node", self.nodes.retrieve_context_node)
        self.graph_builder.add_node("summarize_context_node", self.nodes.summarize_context_node)
        self.graph_builder.add_node("summarize_conversations_node", self.nodes.summarize_conversations_node)
        self.graph_builder.add_node("connector_node", self.nodes.connector_node)  

        # Define the flow
        self.graph_builder.add_edge(START, "conversation_node")
        self.graph_builder.add_conditional_edges(
            "conversation_node",
            tools_condition,
            {
                "tools" : "retrieve_context_node", 
                END : "connector_node",
            }
        )
        self.graph_builder.add_edge("retrieve_context_node", "summarize_context_node")
        self.graph_builder.add_edge("summarize_context_node", "conversation_node")
        self.graph_builder.add_conditional_edges(
            "connector_node",
            should_summarize_conversation,   
            {
                "summarize_conversations_node" : "summarize_conversations_node",
                END : END,
            } 
        )
        self.graph_builder.add_edge("summarize_conversations_node", END)

        return self.graph_builder
    
    def compile(self) : 
        """Compile the graph.""" 
        return self.build().compile()