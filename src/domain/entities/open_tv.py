from datetime import datetime

from pydantic import BaseModel, Field


class OpenTv(BaseModel):
    signal: str
    program_code: str

    class Config:
        validate_assignment = True


class TVData(BaseModel):
    signal: str
    program_code: str
    weekday: str
    available_time: int
    predicted_audience: float | None = Field(default=0)
    exhibition_date: datetime | str

    class Config:
        validate_assignment = True

    def model_dump_tv_data(self):
        if isinstance(self.exhibition_date, datetime):
            self.exhibition_date = self.exhibition_date.isoformat()

        return self.model_dump()
