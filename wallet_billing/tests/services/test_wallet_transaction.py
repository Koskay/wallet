import uuid
from decimal import Decimal

import pytest

from core.apps.common.enums import OperationType, TransactionStatus
from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.exception.transaction import TransactionCreationException
from core.apps.wallets.services.transactions import TransactionService
from tests.factories.wallets import WalletFactory


@pytest.fixture
def transaction_service():
    """Фикстура для создания экземпляра TransactionService."""
    return TransactionService()


@pytest.fixture
def sample_transaction_dto():
    """Фикстура для создания образца TransactionDTO."""
    wallet = WalletFactory()
    return TransactionDTO(
        wallet_id=wallet.id,
        operation_type=OperationType.DEPOSIT,
        amount=Decimal('100.00'),
        balance_after=Decimal('1100.00'),
        balance_before=Decimal('1000.00'),
        status=TransactionStatus.SUCCESS
    )

@pytest.mark.django_db
class TestTransactionService:
    """Тесты для TransactionService."""

    def test_create_transaction_success(self, transaction_service, sample_transaction_dto):
        """Тест успешного создания транзакции."""

        transaction_dto = transaction_service.create_transaction(sample_transaction_dto)
        assert isinstance(transaction_dto, TransactionDTO)
        assert str(transaction_dto.wallet_id) == sample_transaction_dto.wallet_id
        assert transaction_dto.operation_type == sample_transaction_dto.operation_type
        assert transaction_dto.amount == sample_transaction_dto.amount
        assert transaction_dto.balance_after == sample_transaction_dto.balance_after
        assert transaction_dto.balance_before == sample_transaction_dto.balance_before
        assert transaction_dto.status == sample_transaction_dto.status

    def test_create_transaction_failed_with_negative_amount(self, transaction_service, sample_transaction_dto):
        """Транзакция должная вызывать исключение при попытке создать с отрицательной суммой"""
        sample_transaction_dto.amount = Decimal('-100.00')

        with pytest.raises(TransactionCreationException):
            transaction_service.create_transaction(sample_transaction_dto)


    def test_create_transaction_failed_with_invalid_wallet(self, transaction_service, sample_transaction_dto):
        """Транзакция должная вызывать исключение при попытке создать с несуществующим кошельком"""
        sample_transaction_dto.wallet_id = uuid.uuid4()

        with pytest.raises(TransactionCreationException):
            transaction_service.create_transaction(sample_transaction_dto)
