import base64
import os

from dotenv import load_dotenv
from src.common.env_constants import EnvConstants

load_dotenv()

class ManagementAgentAuthenticationHelper:
    @staticmethod
    def create_basic_auth_token(account_id: str) -> str:      
        username = os.getenv(EnvConstants.AUTH_USERNAME)
        password = os.getenv(EnvConstants.AUTH_PASSWORD)
        
        credentials = f"{username}:{password}:{account_id}"
        token = base64.b64encode(credentials.encode()).decode()
        
        return f"Basic {token}"