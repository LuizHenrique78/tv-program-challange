from datetime import datetime

from src.domain.entities.open_tv import OpenTv


class InventoryAvailability(OpenTv):
    date: str | datetime
    available_time: int

    class Config:
        validate_assignment = True
