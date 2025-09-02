import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from core.apps.common.enums import TransactionStatus
from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.dto.wallets import WalletOperationDTO, WalletDTO
from core.apps.wallets.exception.wallets import WalletNotFoundException, InsufficientFundsException
from core.apps.wallets.models.wallets import Wallet
from core.apps.wallets.services.transactions import BaseTransactionService


logger = logging.getLogger(__name__)

@dataclass
class BaseWalletCommandService(ABC):
    """Абстрактный базовый сервис для выполнения операций с кошельком."""
    transaction_service: BaseTransactionService

    @abstractmethod
    def deposit(self, operation_data: WalletOperationDTO) -> TransactionDTO:
        """Выполняет пополнение кошелька."""
        ...

    @abstractmethod
    def withdrawal(self, operation_data: WalletOperationDTO) -> TransactionDTO:
        """Выполняет снятие средств с кошелька."""
        ...


class BaseWalletQueryService(ABC):
    """Абстрактный базовый сервис для получения данных кошелька."""

    @abstractmethod
    def get_wallet_by_id(self, wallet_id: uuid.UUID) -> WalletDTO:
        """Получает кошелек по его идентификатору."""
        ...


class WalletQueryService(BaseWalletQueryService):
    """Сервис для получения данных кошелька из базы данных."""

    def get_wallet_by_id(self, wallet_id: uuid.UUID) -> WalletDTO:
        """
        Получает кошелек по его идентификатору с предзагрузкой транзакций.
        
        Args:
            wallet_id: Уникальный идентификатор кошелька
            
        Returns:
            WalletDTO: DTO объект кошелька
            
        Raises:
            WalletNotFoundException: Если кошелек с указанным ID не найден
        """
        try:
            wallet_model = Wallet.objects.prefetch_related('transactions').get(id=wallet_id)
            return wallet_model.to_dto()
        except Wallet.DoesNotExist:
            logger.error(f'Кошелек с id {wallet_id} не найден')
            raise WalletNotFoundException(wallet_id=wallet_id)

class WalletCommandService(BaseWalletCommandService):
    """Сервис для выполнения операций изменения состояния кошелька."""

    @transaction.atomic
    def deposit(self, operation_data: WalletOperationDTO) -> TransactionDTO:
        """
        Выполняет пополнение кошелька и создает соответствующую транзакцию.
        
        Args:
            operation_data: Данные операции пополнения
            
        Returns:
            TransactionDTO: DTO созданной транзакции
        """
        wallet_model = self._get_wallet_for_update(operation_data.wallet_id)
        balance_before = wallet_model.balance

        wallet_model.deposit(amount=operation_data.amount)
        wallet_model.save(update_fields=['balance'])

        logger.info(f'Кошелек с id {operation_data.wallet_id} успешно пополнен на сумму: {operation_data.amount}')

        return self._create_transaction(
            wallet=wallet_model,
            operation_data=operation_data,
            balance_before=balance_before
        )

    @transaction.atomic
    def withdrawal(self, operation_data: WalletOperationDTO) -> TransactionDTO:
        """
        Выполняет снятие средств с кошелька с проверкой достаточности баланса.
        
        Args:
            operation_data: Данные операции снятия
            
        Returns:
            TransactionDTO: DTO созданной транзакции
            
        Raises:
            InsufficientFundsException: Если недостаточно средств на балансе
        """
        wallet_model = self._get_wallet_for_update(operation_data.wallet_id)
        balance_before = wallet_model.balance

        self.validate_balance(balance=balance_before, amount=operation_data.amount)

        wallet_model.withdrawal(amount=operation_data.amount)
        wallet_model.save(update_fields=['balance'])

        logger.info(f'С кошелька с id {operation_data.wallet_id} успешно списана сумма: {operation_data.amount}')

        return self._create_transaction(
            wallet=wallet_model,
            operation_data=operation_data,
            balance_before=balance_before
        )

    @staticmethod
    def _get_wallet_for_update(wallet_id: uuid.UUID) -> Wallet:
        """
        Получает кошелек с блокировкой для обновления.
        
        Args:
            wallet_id: Уникальный идентификатор кошелька
            
        Returns:
            Wallet: Модель кошелька
            
        Raises:
            WalletNotFoundException: Если кошелек не найден
        """
        try:
            wallet_model = Wallet.objects.select_for_update().get(id=wallet_id)
            return wallet_model
        except Wallet.DoesNotExist:
            logger.error(f'Кошелек с id {wallet_id} не найден')
            raise WalletNotFoundException(wallet_id=wallet_id)

    @staticmethod
    def validate_balance(balance: Decimal, amount: Decimal):
        """
        Проверяет достаточность баланса для снятия средств.
        
        Args:
            balance: Текущий баланс кошелька
            amount: Сумма для снятия
            
        Raises:
            InsufficientFundsException: Если баланс недостаточен
        """
        if balance < amount:
            logger.error(f'Ошибка списания с баланса {balance} на сумму: {amount}, не хватает средств')
            raise InsufficientFundsException(balance=balance, amount=amount)

    def _create_transaction(
        self,
        wallet: Wallet,
        operation_data: WalletOperationDTO,
        balance_before: Decimal
    ) -> TransactionDTO:
        """
        Создает транзакцию для выполненной операции.
        
        Args:
            wallet: Модель кошелька
            operation_data: Данные операции
            balance_before: Баланс до операции
            
        Returns:
            TransactionDTO: DTO созданной транзакции
        """
        transaction_dto = TransactionDTO(
            wallet_id=wallet.id,
            operation_type=operation_data.operation_type,
            amount=operation_data.amount,
            balance_after=wallet.balance,
            balance_before=balance_before,
            status=TransactionStatus.SUCCESS
        )
        return self.transaction_service.create_transaction(transaction=transaction_dto)