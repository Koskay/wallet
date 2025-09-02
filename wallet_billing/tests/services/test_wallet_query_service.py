import uuid

import pytest

from core.apps.wallets.exception.wallets import WalletNotFoundException
from core.apps.wallets.services.wallets import WalletQueryService
from tests.factories.wallets import WalletFactory, WalletTransactionFactory


@pytest.fixture
def wallet_query_service():
    """Фикстура для создания экземпляра WalletQueryService."""
    return WalletQueryService()


@pytest.mark.django_db
class TestWalletQueryService:
    """Тесты для WalletQueryService."""

    def test_get_wallet_by_id_success(self, wallet_query_service):
        """Тест успешного получения данных кошелька и транзакций по нему."""
        wallet =WalletFactory()
        tr1 = WalletTransactionFactory(wallet=wallet)
        tr2 = WalletTransactionFactory(wallet=wallet)
        wallet_data = wallet_query_service.get_wallet_by_id(wallet.id)
        assert str(wallet_data.id) == wallet.id
        assert wallet_data.balance == wallet.balance
        assert str(wallet_data.last_transaction[0].id) == tr2.id # сортировка по дате
        assert str(wallet_data.last_transaction[1].id) == tr1.id
        assert len(wallet_data.last_transaction) == 2

    def test_get_wallet_by_id_not_found(self, wallet_query_service):
        """Попытка получения данных кошелька которого не существует, вызывает исключение"""
        wallet_id = uuid.uuid4()
        with pytest.raises(WalletNotFoundException):
            wallet_query_service.get_wallet_by_id(wallet_id)
