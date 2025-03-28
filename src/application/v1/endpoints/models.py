from pydantic import BaseModel
from typing import Optional


class DateRangeRequest(BaseModel):
    program_code: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    date: Optional[str] = None
