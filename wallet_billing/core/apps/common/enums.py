from enum import Enum

class TransactionStatus(str, Enum):
    """Статус транзакции"""
    SUCCESS = "success"
    IN_PROCESSING = "in_processing"
    CANCELED = "canceled"
    FAILED = "failed"

    @property
    def display_name(self) -> str:
        """Получить человекочитаемое название статуса"""
        display_names: dict[str, str] = {
            TransactionStatus.SUCCESS: "Успешно",
            TransactionStatus.IN_PROCESSING: "В обработке",
            TransactionStatus.CANCELED: "Отменена",
            TransactionStatus.FAILED: "Ошибка"
        }
        return display_names.get(self, "Неизвестный статус")

    @classmethod
    def get_display_name_by_value(cls, value: str) -> str:
        """Получить display name по значению"""
        try:
            return cls(value).display_name
        except ValueError:
            return "Неизвестный статус"

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        """Получить choices для Django модели"""
        return [(status.value, status.display_name) for status in cls]


class OperationType(str, Enum):
    """Тип операции транзакции"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

    @property
    def display_name(self) -> str:
        display_names: dict[str, str] = {
            OperationType.DEPOSIT: "Пополнение",
            OperationType.WITHDRAWAL: "Списание",
        }
        return display_names.get(self, "Неизвестная операция")

    @classmethod
    def get_display_name_by_value(cls, value: str) -> str:
        try:
            return cls(value).display_name
        except ValueError:
            return "Неизвестная операция"

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(op.value, op.display_name) for op in cls]