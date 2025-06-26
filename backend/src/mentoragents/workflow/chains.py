from src.mentoragents.workflow.models import Models
from src.mentoragents.workflow.prompt import MENTOR_CHARACTER_PROMPT, SUMMARY_PROMPT, CONTEXT_SUMMARY_PROMPT, EXTEND_SUMMARY_PROMPT
from src.mentoragents.workflow.tools import Tools
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.mentoragents.core.config import settings

class Chains:
    """
    A class that contains the chains.
    """
    def __init__(self):
        """
        Initialize the chains.
        """
        self.base_model = Models(settings.GROQ_LLM_MODEL).get_groq_model()
        self.summary_model = Models(settings.GROQ_LLM_MODEL_CONTEXT_SUMMARY).get_groq_model()
        self.tools = Tools().get_tools()    

    def get_mentor_resonse_chain(self):
        """
        Get the chain for the mentor response.
        """
        system_prompt = MENTOR_CHARACTER_PROMPT
        model = self.base_model.bind_tools(self.tools)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ],
            template_format = "jinja2"
        )
        return prompt | model 
    
    def get_conversations_summary_chain(self, summary: str = ''): 
        """
        Get the chain for the conversations summary.
        """
        summary_message = EXTEND_SUMMARY_PROMPT if summary else SUMMARY_PROMPT
        prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variation_name="messages"),
                ("human", summary_message.prompt)
            ],
            template_format = "jinja2"
        )
        return prompt | self.base_model 

    def get_context_summary_chain(self):
        """
        Get the chain for the context summary.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("human", CONTEXT_SUMMARY_PROMPT.prompt),
            ],
            template_format = "jinja2"
        )
        return prompt | self.summary_model 