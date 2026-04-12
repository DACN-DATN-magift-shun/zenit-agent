from datetime import datetime
import os
from typing import List, Optional
import uuid

from dotenv import load_dotenv
from langchain_core.tools import tool
from management_agent.common.management_env_constants import ManagementAgentEnvConstants
from management_agent.states.main_state import ManagementAgentMainState
import requests
from src.common.env_constants import EnvConstants

load_dotenv()

class ManagementAgentTransactionTool:
    @staticmethod
    @tool
    def create(
        title: str,
        amount: int,
        transaction_date: str,  # đổi thành str để tránh parse lỗi
        category_id: str,       # đổi thành str
        wallet_id: str,         # đổi thành str
        note: Optional[str] = ""
    ) -> str:
        """Create a financial transaction.
        
        Args:
            title: Title of the transaction
            amount: Amount in VND (integer)
            transaction_date: Date in ISO format (e.g. 2026-04-07T00:00:00)
            category_id: UUID of the category
            wallet_id: UUID of the wallet
            note: Optional note
        """
        MANAGEMENT_API_BASE_URL = os.getenv(ManagementAgentEnvConstants.MANAGEMENT_API_BASE_URL)
        
        try:
            payload = {
                "title": title,
                "amount": amount,
                "transactionDate": transaction_date if transaction_date.endswith("Z") else transaction_date + "Z",  # đảm bảo có timezone
                "categoryId": category_id,
                "walletId": wallet_id,
                "note": note
            }
            
            print(f"Creating transaction with payload: {payload}")
            
            response = requests.post(
                f"{MANAGEMENT_API_BASE_URL}/Transactions",
                json=payload,
                headers={
                    "Authorization": f"Bearer {os.getenv(EnvConstants.TEST_ACCESS_TOKEN)}",
                    "Content-Type": "application/json"
                },
                timeout=30  # thêm timeout
            )
            
            print(f"API status code: {response.status_code}")
            print(f"API response: {response.text}")
            
            if response.status_code == 201:
                return "Transaction created successfully."
            return f"Failed: {response.status_code} - {response.text}"
        except Exception as e:
            print(f"Error calling API: {type(e).__name__}: {e}")
            return f"Error: {e}"
    
    @staticmethod
    @tool
    def set_missing_fields(state: ManagementAgentMainState, missing_fields: List[str]):
        """Set missing fields after done content extraction.
        
        Args:
            state: Current state of the agent
            missing_fields: List of missing fields after content extraction (e.g. ["amount", "transaction_date"])
        """
        
        state["missing_fields"] = missing_fields