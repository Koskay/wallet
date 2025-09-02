import datetime
import uuid
from dataclasses import dataclass
from decimal import Decimal

from core.apps.common.enums import OperationType, TransactionStatus


@dataclass
class TransactionDTO:
    amount: Decimal
    operation_type: OperationType
    status: TransactionStatus
    balance_before: Decimal
    balance_after: Decimal
    wallet_id: uuid.UUID
    id: uuid.UUID = None
    created_at: datetime.datetime = None





