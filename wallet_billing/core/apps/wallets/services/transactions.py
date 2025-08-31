from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.models.transaction import WalletTransaction


@dataclass
class BaseTransactionService(ABC):

    @abstractmethod
    def create_transaction(self, transaction: TransactionDTO) -> TransactionDTO:
        ...


class TransactionService(BaseTransactionService):

    def create_transaction(self, transaction: TransactionDTO) -> TransactionDTO:
        transaction_model = WalletTransaction.from_dto(transaction)
        transaction_model.save()
        return transaction_model.to_dto()