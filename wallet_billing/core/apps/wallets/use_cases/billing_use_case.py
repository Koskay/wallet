from dataclasses import dataclass

from core.apps.common.enums import OperationType
from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.dto.wallets import WalletOperationDTO
from core.apps.wallets.exception.billings import UnsupportedOperationException
from core.apps.wallets.services.wallets import BaseWalletService


@dataclass
class BillingUseCase:
    wallet_service: BaseWalletService

    def process_operation(self, operation: WalletOperationDTO) -> TransactionDTO:
        if operation.operation_type == OperationType.DEPOSIT:
            return self.wallet_service.deposit(operation)
        elif operation.operation_type == OperationType.WITHDRAWAL:
            return self.wallet_service.withdrawal(operation)
        else:
            raise UnsupportedOperationException(operation_type=operation.operation_type)