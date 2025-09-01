import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from core.apps.common.enums import TransactionStatus
from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.dto.wallets import WalletOperationDTO
from core.apps.wallets.exception.wallets import WalletNotFoundException, InsufficientFundsException
from core.apps.wallets.models.wallets import Wallet
from core.apps.wallets.services.transactions import BaseTransactionService


@dataclass
class BaseWalletService(ABC):
    transaction_service: BaseTransactionService

    @abstractmethod
    def deposit(self, operation_data: WalletOperationDTO) -> TransactionDTO:
        ...

    @abstractmethod
    def withdrawal(self, operation_data: WalletOperationDTO) -> TransactionDTO:
        ...


class WalletService(BaseWalletService):

    @transaction.atomic
    def deposit(self, operation_data: WalletOperationDTO) -> TransactionDTO:
        wallet_model = self._get_wallet_for_update(operation_data.wallet_id)
        balance_before = wallet_model.balance

        wallet_model.deposit(amount=operation_data.amount)
        wallet_model.save(update_fields=['balance'])

        return self._create_transaction(
            wallet=wallet_model,
            operation_data=operation_data,
            balance_before=balance_before
        )

    @transaction.atomic
    def withdrawal(self, operation_data: WalletOperationDTO) -> TransactionDTO:
        wallet_model = self._get_wallet_for_update(operation_data.wallet_id)
        balance_before = wallet_model.balance

        self.validate_balance(balance=balance_before, amount=operation_data.amount)

        wallet_model.withdrawal(amount=operation_data.amount)
        wallet_model.save(update_fields=['balance'])

        return self._create_transaction(
            wallet=wallet_model,
            operation_data=operation_data,
            balance_before=balance_before
        )

    @staticmethod
    def _get_wallet_for_update(wallet_id: uuid.UUID) -> Wallet:
        try:
            wallet_model = Wallet.objects.select_for_update().get(id=wallet_id)
            return wallet_model
        except Wallet.DoesNotExist:
            raise WalletNotFoundException(wallet_id=wallet_id)

    @staticmethod
    def validate_balance(balance: Decimal, amount: Decimal):
        if balance < amount:
            raise InsufficientFundsException(balance=balance, amount=amount)

    def _create_transaction(
        self,
        wallet: Wallet,
        operation_data: WalletOperationDTO,
        balance_before: Decimal
    ) -> TransactionDTO:
        transaction_dto = TransactionDTO(
            wallet_id=wallet.id,
            operation_type=operation_data.operation_type,
            amount=operation_data.amount,
            balance_after=wallet.balance,
            balance_before=balance_before,
            status=TransactionStatus.SUCCESS
        )
        return self.transaction_service.create_transaction(transaction=transaction_dto)






