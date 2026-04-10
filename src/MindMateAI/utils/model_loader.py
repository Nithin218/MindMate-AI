import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from MindMateAI.utils.common import read_yaml
from MindMateAI.logger import logger
from pathlib import Path
from langchain_groq import ChatGroq

load_dotenv()


class ConfigLoader:
    def __init__(self):
        print("Loaded config.....")
        config_path = Path(__file__).resolve().parents[3] / "config" / "config.yaml"
        self.config = read_yaml(config_path)
        if not self.config:
            raise ValueError("Configuration file is empty or not found.")

    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):
    model_provider: Literal["groq", "groq_light"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """
        groq       -> cbt_agent, writer_agent        (llama-3.3-70b-versatile)
        groq_light -> emotion_analysis_agent,
                      ethical_guardian_agent          (llama-3.1-8b-instant)
        """
        logger.info(f"Loading model: {self.model_provider}")
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")

        model_name = self.config["llm"][self.model_provider]["model_name"]
        llm = ChatGroq(model=model_name, api_key=groq_api_key)
        logger.info(f"Loaded {model_name} from Groq.")
        return llm