from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel


class CreateTransactionRequest(BaseModel):
    title: str 
    amount: int
    transaction_date: datetime
    category_id: uuid.UUID
    wallet_id: uuid.UUID
    note: Optional[str] = ""
    
class CreateTransactionResponse(BaseModel):
    id: uuid.UUID
    title: str
    amount: int
    transaction_date: datetime
    category_id: uuid.UUID
    wallet_id: uuid.UUID
    note: Optional[str] = ""
    
    