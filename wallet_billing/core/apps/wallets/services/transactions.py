from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.exception.transaction import TransactionCreationException
from core.apps.wallets.models.transaction import WalletTransaction


@dataclass
class BaseTransactionService(ABC):

    @abstractmethod
    def create_transaction(self, transaction: TransactionDTO) -> TransactionDTO:
        ...


class TransactionService(BaseTransactionService):

    def create_transaction(self, transaction: TransactionDTO) -> TransactionDTO:
        transaction_model = WalletTransaction.from_dto(transaction)
        try:
            transaction_model.full_clean()
            transaction_model.save()
        except (IntegrityError, ValidationError):
            raise TransactionCreationException(wallet_id=transaction_model.wallet_id,
                                               operation_type=transaction_model.operation_type,
                                               amount=transaction_model.amount)
        return transaction_model.to_dto()