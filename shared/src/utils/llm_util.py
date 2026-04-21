import itertools
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from src.common.llm_constants import LLMConstants
from src.common.env_constants import EnvConstants

load_dotenv()

_api_keys = [k.strip() for k in os.getenv(EnvConstants.GOOGLE_AI_API_KEY).split(",") if k.strip()]
_key_cycle = itertools.cycle(_api_keys)

class LLMUtil:
    @staticmethod
    def get_google_genai_chat_model():
        model = ChatGoogleGenerativeAI(
            model=os.getenv(EnvConstants.GOOGLE_CHAT_MODEL_NAME),
            temperature=LLMConstants.GOOGLE_MODEL_TEMPERATURE,
            api_key=next(_key_cycle),
        )
        
        return model

    @staticmethod
    def get_google_genai_embedding_model():
        model = GoogleGenerativeAIEmbeddings(
            model=os.getenv(EnvConstants.GOOGLE_EMBEDDING_MODEL_NAME),
            api_key=next(_key_cycle),
        )
        
        return model