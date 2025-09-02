from functools import lru_cache

from core.apps.wallets.services.transactions import TransactionService
from core.apps.wallets.services.wallets import WalletCommandService, WalletQueryService
from core.apps.wallets.use_cases.billing_use_case import BillingUseCase


@lru_cache(1)
def get_billing_use_case():
    return BillingUseCase(
        wallet_service=WalletCommandService(
            transaction_service=TransactionService()
        ),
    )

@lru_cache(1)
def get_wallet_query_service():
    return WalletQueryService()