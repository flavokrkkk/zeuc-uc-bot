from enum import Enum


class PurchaseStatuses(Enum):
    IN_PROGRESS = "Ожидает"
    COMPLETED = "Выполнен"
    CANCELED = "Отменен"


class BonusStatuses(Enum):
    GET = "Получен"
    USE = "Использован"