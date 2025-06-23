from langchain_huggingface import HuggingFaceEmbeddings 
from loguru import logger 

class Embeddings: 
    """
    A class that embeds text into a vector space.
    """
    def __init__(self, model_name :str, device :str = "cpu"):
        """
        Initializes the Embeddings with a given model name and device.
        """
        self.model_name = model_name 
        self.device = device 

    def get_hf_model(self) -> HuggingFaceEmbeddings:
        """
        Returns a HuggingFaceEmbeddings object that embeds text into a vector space.
        """
        logger.info(f"Initializing HuggingFaceEmbeddings with model name: {self.model_name} and device: {self.device}")
        return HuggingFaceEmbeddings(
            model_name = self.model_name,
            model_kwargs = {"device": self.device},
            encode_kwargs = {"normalize_embeddings": True},
            trust_remote_code = True
        )