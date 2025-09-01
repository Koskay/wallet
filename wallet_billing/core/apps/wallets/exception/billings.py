from dataclasses import dataclass

from core.apps.common.exception.base import ServiceException


@dataclass
class UnsupportedOperationException(ServiceException):
    operation_type: str = None

    @property
    def message(self):
        return f"Операция {self.operation_type} не поддерживается"

    @property
    def status_code(self):
        return 400