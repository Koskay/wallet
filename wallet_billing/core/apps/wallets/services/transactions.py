import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.exception.transaction import TransactionCreationException
from core.apps.wallets.models.transaction import WalletTransaction


logger = logging.getLogger(__name__)

@dataclass
class BaseTransactionService(ABC):
    """Абстрактный базовый сервис для работы с транзакциями."""

    @abstractmethod
    def create_transaction(self, transaction: TransactionDTO) -> TransactionDTO:
        """Создает новую транзакцию."""
        ...


class TransactionService(BaseTransactionService):
    """Сервис для создания и управления транзакциями кошелька."""

    def create_transaction(self, transaction: TransactionDTO) -> TransactionDTO:
        """
        Создает новую транзакцию в базе данных с валидацией.
        
        Args:
            transaction: DTO объект транзакции для создания
            
        Returns:
            TransactionDTO: DTO созданной транзакции
            
        Raises:
            TransactionCreationException: Если произошла ошибка при создании транзакции
                (нарушение целостности данных или ошибка валидации)
        """
        transaction_model = WalletTransaction.from_dto(transaction)
        try:
            transaction_model.full_clean()
            transaction_model.save()

            logger.info(f'Успешное создания транзакции для кошелька {transaction_model.wallet_id}')
        except (IntegrityError, ValidationError):
            logger.error(f'Ошибка создания транзакции для кошелька {transaction_model.wallet_id} не пройдена валидация')
            raise TransactionCreationException(wallet_id=transaction_model.wallet_id,
                                               operation_type=transaction_model.operation_type,
                                               amount=transaction_model.amount)
        return transaction_model.to_dto()