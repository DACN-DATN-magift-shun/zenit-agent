import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from management_agent.tools.requests.create_transaction_request import CreateTransactionRequest, CreateTransactionResponse
import requests
from src.common.env_constants import EnvConstants

load_dotenv()

class ManagementAgentTransactionTool:
    @staticmethod
    @tool
    def create(request: CreateTransactionRequest) -> CreateTransactionResponse:
        MANAGEMENT_API_BASE_URL = os.getenv(EnvConstants.MANAGEMENT_API_BASE_URL)
        
        try:
            response = requests.post(
                f"{MANAGEMENT_API_BASE_URL}/Transactions",
                json=request.model_dump(),
                headers={
                    "Authorization": f"Bearer {os.getenv(EnvConstants.TEST_ACCESS_TOKEN)}",
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 201:
                return CreateTransactionResponse(success=True, message="Transaction created successfully.")
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return CreateTransactionResponse(success=False, message="Failed to create transaction.")