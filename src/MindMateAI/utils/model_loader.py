import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from MindMateAI.utils.common import read_yaml
from MindMateAI.logger import logger
from dotenv import load_dotenv
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = read_yaml(Path("config.yaml"))
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "huggingface", "google"] = "huggingface"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        logger.info("LLM loading...")
        logger.info(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            logger.info("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm=ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider == "huggingface":
            logger.info("Loading LLM from HuggingFace..............")
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HF_TOKEN")
            model_name = self.config["llm"]["huggingface"]["model_name"]
            llm = HuggingFaceEndpoint(
                repo_id=model_name,
                task="text-generation",
                temperature=0.5,
                max_new_tokens=1000,
            )
            llm=ChatHuggingFace(llm=llm)
        elif self.model_provider == "google":
            logger.info("Loading LLM from Google..............")
            os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
            model_name = self.config["llm"]["google"]["model_name"]
            llm=ChatGoogleGenerativeAI(model=model_name)
        
        return llm