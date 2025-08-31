import uuid
from dataclasses import dataclass
from decimal import Decimal



@dataclass
class TransactionDTO:
    amount: Decimal
    operation_type: str
    status: str
    balance_before: Decimal
    balance_after: Decimal
    wallet_id: uuid.UUID
    id: uuid.UUID = None
