import uuid

import pytest

from tests.factories.wallets import WalletFactory, WalletTransactionFactory


def get_url(wallet_id: uuid.UUID) -> str:
    """Получение URL для API endpoint'а """

    return f"/api/v1/wallets/{wallet_id}"



@pytest.mark.django_db(transaction=False)
class TestQueryWallet:

    def test_get_wallet_success(self, client):
        """
        Тестирует успешное получения данных о кошельке.
        Проверяет корректность ответа API.
        """
        wallet = WalletFactory()
        tr1 = WalletTransactionFactory(wallet=wallet)
        tr2 = WalletTransactionFactory(wallet=wallet)
        response = client.get(get_url(wallet.id), content_type="application/json")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["data"]["wallet_id"] == str(wallet.id)
        assert response_data["data"]["balance"] == str(wallet.balance)
        assert len(response_data["data"]["last_transaction_list"]) == 2
        assert response_data["data"]["last_transaction_list"][0]["transaction_id"] == str(tr2.id)


    def test_get_wallet_with_wallet_id_not_found(self, client):
        wallet_id = uuid.uuid4()

        response = client.get(get_url(wallet_id), content_type="application/json")

        assert response.status_code == 404