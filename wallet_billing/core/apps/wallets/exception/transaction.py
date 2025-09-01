import uuid
from dataclasses import dataclass
from decimal import Decimal

from core.apps.common.exception.base import ServiceException

@dataclass
class TransactionCreationException(ServiceException):
    wallet_id: uuid.UUID = None
    operation_type: str = None
    amount: Decimal = None

    @property
    def message(self):
        return (f"Ошибка создания транзакции для кошелька {self.wallet_id} "
                f"на операцию {self.operation_type} и суммой {self.amount}")

    @property
    def status_code(self):
        return 500
