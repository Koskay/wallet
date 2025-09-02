import logging
from dataclasses import dataclass

from core.apps.common.enums import OperationType
from core.apps.wallets.dto.transaction import TransactionDTO
from core.apps.wallets.dto.wallets import WalletOperationDTO
from core.apps.wallets.exception.billings import UnsupportedOperationException
from core.apps.wallets.services.wallets import BaseWalletCommandService


logger = logging.getLogger(__name__)

@dataclass
class BillingUseCase:
    wallet_service: BaseWalletCommandService

    def process_operation(self, operation: WalletOperationDTO) -> TransactionDTO:
        if operation.operation_type == OperationType.DEPOSIT:
            logger.info(f'Вызвана функция пополнения баланса для кошелька {operation.wallet_id}')

            return self.wallet_service.deposit(operation)
        elif operation.operation_type == OperationType.WITHDRAWAL:
            logger.info(f'Вызвана функция списания баланса для кошелька {operation.wallet_id}')

            return self.wallet_service.withdrawal(operation)
        else:
            logger.info(f'Неверный тип операции {operation.operation_type}')
            raise UnsupportedOperationException(operation_type=operation.operation_type)