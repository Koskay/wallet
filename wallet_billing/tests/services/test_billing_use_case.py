import uuid
from decimal import Decimal
from unittest.mock import Mock

import pytest

from core.apps.common.enums import OperationType, TransactionStatus
from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.dto.wallets import WalletOperationDTO
from core.apps.wallets.exception.billings import UnsupportedOperationException

from core.apps.wallets.use_cases.billing_use_case import BillingUseCase


@pytest.fixture
def billing_use_case():
    """Фикстура для создания экземпляра BillingUseCase."""
    wallet_service_mock = Mock()
    return BillingUseCase(
        wallet_service=wallet_service_mock
    ), wallet_service_mock


@pytest.fixture
def sample_transaction_dto():
    """Фикстура для создания образца TransactionDTO."""
    return TransactionDTO(
        wallet_id=uuid.uuid4(),
        operation_type=OperationType.DEPOSIT,
        amount=Decimal('300.00'),
        balance_after=Decimal('1300.00'),
        balance_before=Decimal('1000.00'),
        status=TransactionStatus.SUCCESS
    )

@pytest.mark.django_db
class TestBillingUseCase:

    @pytest.mark.parametrize("operation_type, expected_method_name", [
        (OperationType.DEPOSIT, "deposit"),
        (OperationType.WITHDRAWAL, "withdrawal")
    ])
    def test_billing_operations_correct_method_called(self,
            billing_use_case, sample_transaction_dto, operation_type, expected_method_name
    ):
        """
        Тестирует, что для каждого типа операции вызывается соответствующий метод сервиса кошелька.
        Проверяет корректность маршрутизации операций DEPOSIT и WITHDRAWAL.
        """
        billing_use_case, wallet_service = billing_use_case

        operation_dto = WalletOperationDTO(
            wallet_id=sample_transaction_dto.wallet_id,
            operation_type=operation_type,
            amount=sample_transaction_dto.amount
        )

        expected_method = getattr(wallet_service, expected_method_name)
        sample_transaction_dto.operation_type = operation_type
        expected_method.return_value = sample_transaction_dto

        transaction_dto = billing_use_case.process_operation(operation=operation_dto)

        assert transaction_dto == sample_transaction_dto
        expected_method.assert_called_once_with(operation_dto)


    def test_billing_invalid_operation(self, billing_use_case, sample_transaction_dto):
        """
        Тестирует обработку неподдерживаемого типа операции.
        Проверяет, что при передаче некорректного типа операции выбрасывается UnsupportedOperationException.
        """
        billing_use_case, wallet_service = billing_use_case
        billing_use_case.wallet_service.deposit.return_value = sample_transaction_dto
        operation_dto = WalletOperationDTO(
            wallet_id=sample_transaction_dto.wallet_id,
            operation_type="OperationType.WITHDRAWAL",
            amount=sample_transaction_dto.amount
        )

        with pytest.raises(UnsupportedOperationException):
            billing_use_case.process_operation(operation=operation_dto)
            wallet_service.deposit.assert_not_called()
            wallet_service.withdrawal.assert_not_called()