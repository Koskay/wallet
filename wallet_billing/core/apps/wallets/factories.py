from functools import lru_cache

from core.apps.wallets.services.transactions import TransactionService
from core.apps.wallets.services.wallets import WalletService
from core.apps.wallets.use_cases.billing_use_case import BillingUseCase


@lru_cache(1)
def get_billing_use_case():
    return BillingUseCase(
        wallet_service=WalletService(
            transaction_service=TransactionService()
        ),
    )