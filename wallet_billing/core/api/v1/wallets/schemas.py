import datetime
import uuid
from decimal import Decimal

from pydantic import BaseModel, condecimal, field_serializer

from core.apps.common.enums import OperationType, TransactionStatus
from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.dto.wallets import WalletOperationDTO, WalletDTO


class TransactionSchema(BaseModel):
    operation_type: OperationType | str
    amount: condecimal(gt=0, decimal_places=2)

class WalletTransactionInSchema(TransactionSchema):

    def to_dto(self, wallet_id:uuid.UUID) -> WalletOperationDTO:
        return WalletOperationDTO(
            wallet_id=wallet_id,
            operation_type=self.operation_type,
            amount=self.amount
        )

class WalletTransactionOutSchema(TransactionSchema):
    transaction_id: uuid.UUID
    wallet_id: uuid.UUID
    balance: Decimal
    status: TransactionStatus | str
    created_at: datetime.datetime

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.strftime("%d.%m.%Y %H:%M:%S")

    @classmethod
    def from_dto(cls, dto: TransactionDTO) -> 'WalletTransactionOutSchema':
        return cls(
            transaction_id=dto.id,
            wallet_id=dto.wallet_id,
            operation_type=dto.operation_type.get_display_name_by_value(value=dto.operation_type),
            amount=dto.amount,
            balance=dto.balance_after,
            status=dto.status.get_display_name_by_value(value=dto.status),
            created_at=dto.created_at
        )


class WalletDataOutSchema(BaseModel):
    wallet_id: uuid.UUID
    balance: Decimal
    last_transaction_list: list[WalletTransactionOutSchema]

    @classmethod
    def from_dto(cls, dto: WalletDTO) -> 'WalletDataOutSchema':
        return cls(
            wallet_id=dto.id,
            balance=dto.balance,
            last_transaction_list=[WalletTransactionOutSchema.from_dto(transaction) for transaction in dto.last_transaction]
        )





