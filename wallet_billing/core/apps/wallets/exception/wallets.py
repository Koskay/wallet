import uuid
from dataclasses import dataclass
from decimal import Decimal

from core.apps.common.exception.base import ServiceException


@dataclass
class WalletNotFoundException(ServiceException):
    wallet_id: uuid.UUID

    @property
    def message(self):
        return f"Кошелек с {self.wallet_id} не найден"

    @property
    def status_code(self):
        return 404


@dataclass(eq=False)
class InsufficientFundsException(ServiceException):
    balance: Decimal
    amount: Decimal

    @property
    def message(self):
        return f"Недостаточно средств. Баланс: {self.balance}, Требуется: {self.amount}"

    @property
    def status_code(self):
        return 400