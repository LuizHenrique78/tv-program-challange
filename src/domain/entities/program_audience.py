from datetime import datetime

from src.domain.entities.open_tv import OpenTv


class ProgramAudience(OpenTv):
    exhibition_date: str | datetime
    program_start_time: str | datetime
    average_audience: float

    class Config:
        validate_assignment = True