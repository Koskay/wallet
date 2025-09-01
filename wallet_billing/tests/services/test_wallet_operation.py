import uuid
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from core.apps.common.enums import OperationType, TransactionStatus
from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.dto.wallets import WalletOperationDTO
from core.apps.wallets.exception.wallets import WalletNotFoundException, InsufficientFundsException
from core.apps.wallets.models.wallets import Wallet
from core.apps.wallets.services.transactions import TransactionService
from core.apps.wallets.services.wallets import WalletService
from tests.factories.wallets import WalletFactory


@pytest.fixture
def transaction_service():
    """Фикстура для создания экземпляра TransactionService."""
    return TransactionService()


@pytest.fixture
def wallet_service(transaction_service):
    """Фикстура для создания экземпляра WalletService."""
    return WalletService(transaction_service=transaction_service)


class WalletTestDataFactory:
    """Фабрика для создания тестовых данных кошельков."""
    
    STANDARD_AMOUNT = Decimal('100.00')
    LARGE_AMOUNT = Decimal('10000000.00')
    MAX_LIMIT_AMOUNT = Decimal('100000000000.00')
    
    @staticmethod
    def create_deposit_operation(wallet_id, amount=None):
        """Создает DTO для операции депозита."""
        return WalletOperationDTO(
            wallet_id=wallet_id,
            operation_type=OperationType.DEPOSIT,
            amount=amount or WalletTestDataFactory.STANDARD_AMOUNT
        )
    
    @staticmethod
    def create_withdrawal_operation(wallet_id, amount=None):
        """Создает DTO для операции снятия."""
        return WalletOperationDTO(
            wallet_id=wallet_id,
            operation_type=OperationType.WITHDRAWAL,
            amount=amount or WalletTestDataFactory.STANDARD_AMOUNT
        )


@pytest.mark.django_db(transaction=True)
class TestWalletServiceDeposits:
    """Тесты для операций пополнения кошелька."""

    def test_successful_deposit_updates_balance_and_creates_transaction(self, wallet_service):
        """Успешное пополнение должно обновить баланс и создать транзакцию."""

        wallet = WalletFactory()
        balance_before = wallet.balance
        amount = WalletTestDataFactory.STANDARD_AMOUNT
        balance_after = balance_before + amount
        operation = WalletTestDataFactory.create_deposit_operation(wallet.id, amount)

        transaction = wallet_service.deposit(operation)

        self._assert_successful_deposit(
            transaction=transaction,
            wallet_id=wallet.id,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after
        )

    def test_deposit_with_nonexistent_wallet_raises_exception(self, wallet_service):
        """Пополнение несуществующего кошелька должно вызывать исключение."""

        nonexistent_wallet_id = uuid.uuid4()
        operation = WalletTestDataFactory.create_deposit_operation(nonexistent_wallet_id)

        with pytest.raises(WalletNotFoundException):
            wallet_service.deposit(operation)

    def test_deposit_exceeding_max_balance_raises_validation_error(self, wallet_service):
        """Пополнение, превышающее максимальный баланс, должно вызывать ошибку валидации."""

        wallet = WalletFactory()
        operation = WalletTestDataFactory.create_deposit_operation(
            wallet.id, 
            WalletTestDataFactory.MAX_LIMIT_AMOUNT
        )

        with pytest.raises(ValidationError):
            wallet_service.deposit(operation)

    def _assert_successful_deposit(self, transaction, wallet_id, amount, balance_before, balance_after):
        """Проверяет успешность операции пополнения."""
        # Проверка возвращенной транзакции
        assert isinstance(transaction, TransactionDTO)
        assert str(transaction.wallet_id) == wallet_id
        assert transaction.operation_type == OperationType.DEPOSIT.value
        assert transaction.amount == amount
        assert transaction.balance_before == balance_before
        assert transaction.balance_after == balance_after
        assert transaction.status == TransactionStatus.SUCCESS
        
        # Проверка обновления баланса в БД
        updated_wallet = Wallet.objects.get(id=wallet_id)
        assert updated_wallet.balance == balance_after


@pytest.mark.django_db(transaction=True)
class TestWalletServiceWithdrawals:
    """Тесты для операций снятия средств с кошелька."""

    def test_successful_withdrawal_updates_balance_and_creates_transaction(self, wallet_service):
        """Успешное снятие должно обновить баланс и создать транзакцию."""

        wallet = WalletFactory()
        balance_before = wallet.balance
        amount = WalletTestDataFactory.STANDARD_AMOUNT
        balance_after = balance_before - amount
        operation = WalletTestDataFactory.create_withdrawal_operation(wallet.id, amount)

        transaction = wallet_service.withdrawal(operation)

        self._assert_successful_withdrawal(
            transaction=transaction,
            wallet_id=wallet.id,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after
        )

    def test_withdrawal_with_insufficient_funds_raises_exception(self, wallet_service):
        """Снятие суммы, превышающей баланс, должно вызывать исключение."""

        wallet = WalletFactory()
        balance_before = wallet.balance
        excessive_amount = WalletTestDataFactory.LARGE_AMOUNT
        operation = WalletTestDataFactory.create_withdrawal_operation(wallet.id, excessive_amount)

        with pytest.raises(InsufficientFundsException):
            wallet_service.withdrawal(operation)
        
        # Проверяем, что баланс не изменился
        wallet_balance_after = Wallet.objects.get(id=wallet.id).balance
        assert wallet_balance_after == balance_before

    def _assert_successful_withdrawal(self, transaction, wallet_id, amount, balance_before, balance_after):
        """Проверяет успешность операции снятия."""
        # Проверка возвращенной транзакции
        assert isinstance(transaction, TransactionDTO)
        assert str(transaction.wallet_id) == wallet_id
        assert transaction.operation_type == OperationType.WITHDRAWAL.value
        assert transaction.amount == amount
        assert transaction.balance_before == balance_before
        assert transaction.balance_after == balance_after
        assert transaction.status == TransactionStatus.SUCCESS
        
        # Проверка обновления баланса в БД
        updated_wallet = Wallet.objects.get(id=wallet_id)
        assert updated_wallet.balance == balance_after