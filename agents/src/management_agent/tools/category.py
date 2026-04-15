import os

from dotenv import load_dotenv
from management_agent.tools.helpers.authentication_helper import ManagementAgentAuthenticationHelper
import requests
from langchain_core.tools import tool
from management_agent.common.management_env_constants import ManagementAgentEnvConstants

load_dotenv()

class ManagementAgentCategoryTool:
    @staticmethod
    def get_all(account_id: str):
        """
        Get all categories for the specified account.
        
        Args:
            account_id (str): The account ID to bind with the tool.
        """
        
        @tool("get_all_categories")
        def get_all_categories():
            """
            Get all categories for the specified account.
            """
            
            MANAGEMENT_API_BASE_URL = os.getenv(ManagementAgentEnvConstants.MANAGEMENT_API_BASE_URL)
            basic_auth_token = ManagementAgentAuthenticationHelper.create_basic_auth_token(account_id)
            
            try:
                response = requests.get(
                    f"{MANAGEMENT_API_BASE_URL}/Categories",
                    headers={
                        "Authorization": basic_auth_token,
                        "Content-Type": "application/json"
                    },
                    params={
                        "PageSize": 100,
                        "UseCountTotal": True
                    },
                )
                print(f"Category Response: {response}")
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching categories: {e}")
                return None
            
        return get_all_categories