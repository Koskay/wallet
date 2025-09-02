import uuid

import pytest

from core.apps.common.enums import OperationType
from core.apps.wallets.models.wallets import Wallet
from tests.factories.wallets import WalletFactory


@pytest.fixture
def operation_data():
    """Фикстура для создания тестовых данных заказа."""
    return {
        "operation_type": "deposit",
        "amount": "1000"
    }



def get_url(wallet_id: uuid.UUID) -> str:
    """Получение URL для API endpoint'а """

    return f"/api/v1/wallets/{wallet_id}/operation"



@pytest.mark.django_db(transaction=True)
class TestCommandWallet:

    @pytest.mark.parametrize("operation_type", [
        "deposit",
        "withdrawal"
    ])
    def test_wallet_operation(self, client, operation_type):
        """
        Тестирует успешное выполнение операций с кошельком (пополнение и снятие).
        Проверяет корректность ответа API и обновление баланса кошелька.
        """
        wallet = WalletFactory()
        operation_data = {
            "operation_type": operation_type,
            "amount": "1000"
        }
        response = client.post(get_url(wallet.id), operation_data, content_type="application/json")
        response_data = response.json()
        wallet_balance = Wallet.objects.get(id=wallet.id).balance
        assert response.status_code == 201
        assert response_data["data"]["operation_type"] == OperationType.get_display_name_by_value(operation_type)
        assert response_data["data"]["amount"] == "1000"
        assert response_data["data"]["wallet_id"] == str(wallet.id)
        assert response_data["data"]["status"] == "Успешно"
        assert str(wallet_balance) == response_data["data"]["balance"]

    def test_wallet_operation_with_invalid_operation_type(self, client):
        """
        Тестирует обработку некорректного типа операции.
        Проверяет, что API возвращает ошибку 400 и баланс кошелька не изменяется.
        """
        wallet = WalletFactory()
        operation_data = {
            "operation_type": "invalid_operation_type",
            "amount": "1000"
        }
        response = client.post(get_url(wallet.id), operation_data, content_type="application/json")

        assert response.status_code == 400

        wallet_balance = Wallet.objects.get(id=wallet.id).balance
        assert wallet_balance == wallet.balance

    def test_wallet_operation_with_invalid_amount(self, client):
        """
        Тестирует обработку некорректной суммы операции (отрицательное значение).
        Проверяет, что API возвращает ошибку валидации 422 и баланс не изменяется.
        """
        wallet = WalletFactory()
        operation_data = {
            "operation_type": "deposit",
            "amount": "-1000"
        }
        response = client.post(get_url(wallet.id), operation_data, content_type="application/json")

        assert response.status_code == 422

        wallet_balance = Wallet.objects.get(id=wallet.id).balance
        assert wallet_balance == wallet.balance

    def test_wallet_operation_with_wallet_id_not_found(self, client):
        """
        Тестирует обработку операции с несуществующим кошельком.
        Проверяет, что API возвращает ошибку 404 при попытке операции с несуществующим ID кошелька.
        """
        wallet_id = uuid.uuid4()
        operation_data = {
            "operation_type": "deposit",
            "amount": "1000"
        }
        response = client.post(get_url(wallet_id), operation_data, content_type="application/json")

        assert response.status_code == 404