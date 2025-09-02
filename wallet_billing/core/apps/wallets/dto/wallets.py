import uuid
from dataclasses import dataclass
from decimal import Decimal

from core.apps.common.enums import OperationType
from core.apps.wallets.dto.transaction import TransactionDTO


@dataclass
class WalletDTO:
    id: uuid.UUID
    balance: Decimal
    last_transaction: list[TransactionDTO]
    user_id: int = None
    is_active: bool = None

@dataclass
class WalletOperationDTO:
    wallet_id: uuid.UUID
    operation_type: OperationType
    amount: Decimal