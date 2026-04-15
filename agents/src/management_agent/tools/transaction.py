from datetime import datetime
import os
from typing import List, Optional
import uuid

from dotenv import load_dotenv
from langchain_core.tools import tool
from management_agent.api.data.management_qdrant import ManagementAgentQdrant
from management_agent.api.requests.qdrant_upsert_request import ManagementAgentQdrantUpsertRequest, TransactionPayload
from management_agent.common.management_env_constants import ManagementAgentEnvConstants
from management_agent.states.main_state import ManagementAgentMainState
from management_agent.tools.helpers.authentication_helper import ManagementAgentAuthenticationHelper
from qdrant_client import QdrantClient
import requests
from src.common.env_constants import EnvConstants

load_dotenv()

class ManagementAgentTransactionTool:
    @staticmethod
    def create(account_id: str, query: str = ""):
        """Create a tool with bind account_id
        
        Args:
            account_id: The account ID to bind with the tool
            query: The text query for Qdrant search
        """
        
        @tool
        def create_transaction(
            title: str,
            amount: int,
            transaction_date: str,  # đổi thành str để tránh parse lỗi
            category_id: str,       # đổi thành str
            category_name: str,    
            wallet_id: str,         # đổi thành str
            wallet_name: str,       
            note: Optional[str] = "",
        ) -> str:
            """Create a financial transaction.
            
            Args:
                title: Title of the transaction
                amount: Amount in VND (integer)
                transaction_date: Date in ISO format (e.g. 2026-04-07T00:00:00)
                category_id: UUID of the category
                category_name: Name of the category (for vector upsert in Qdrant, not required for API call)
                wallet_id: UUID of the wallet
                wallet_name: Name of the wallet (for vector upsert in Qdrant, not required for API call)
                note: Optional note
            """
            MANAGEMENT_API_BASE_URL = os.getenv(ManagementAgentEnvConstants.MANAGEMENT_API_BASE_URL)
            basic_auth_token = ManagementAgentAuthenticationHelper.create_basic_auth_token(account_id)
            
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
                        "Authorization": basic_auth_token,
                        "Content-Type": "application/json"
                    },
                    timeout=30  # thêm timeout
                )
                
                print(f"API status code: {response.status_code}")
                print(f"API response: {response.text}")
                
                if response.status_code == 201:
                    qdrant_client = QdrantClient(url=os.getenv(EnvConstants.QDRANT_CLIENT_URL))
                    qdrant = ManagementAgentQdrant(qdrant_client)
                    
                    qdrant.upsert(
                        ManagementAgentQdrantUpsertRequest(
                            collection="transactions",
                            query=query,
                            payload=TransactionPayload(
                                account_id=account_id,
                                title=title,
                                category=category_name,
                                wallet=wallet_name
                            )
                        )
                    )
                    
                    return "Transaction created successfully."
                return f"Failed: {response.status_code} - {response.text}"
            except Exception as e:
                print(f"Error calling API: {type(e).__name__}: {e}")
                return f"Error: {e}"
            
        return create_transaction
    
    @staticmethod
    @tool
    def get_missing_fields(missing_fields: List[str]):
        """Get missing fields after done content extraction.
        
        Args:
            missing_fields: List of missing fields after content extraction (e.g. ["amount", "transaction_date"])
        """
        
        return missing_fields