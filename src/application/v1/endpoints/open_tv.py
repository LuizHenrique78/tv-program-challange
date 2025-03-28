from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from src.application.v1.endpoints.models import DateRangeRequest
from src.domain.entities.open_tv import TVData
from src.domain.services.tv_data_service import TvDataService

router = APIRouter()

tv_service = TvDataService()

weekday_map = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}


@router.get("/program", response_model=List[TVData])
def get_program_data(program_code: str, date: str):
    tv_data_list = tv_service.get_all_data()
    weekday = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
    result = [
        item for item in tv_data_list
        if item.program_code == program_code and item.weekday == weekday
    ]

    if not result:
        raise HTTPException(status_code=404, detail="No data found for this program and date")

    return result


@router.get("/period", response_model=List[TVData])
def get_period_data(program_code: str, start_date: str, end_date: str):
    tv_data_list = tv_service.get_all_data()

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    result = [
        item for item in tv_data_list
        if item.program_code == program_code and
           start_date_obj >= datetime.strptime(item.exhibition_date, "%Y-%m-%d") <= end_date_obj
    ]

    if not result:
        raise HTTPException(status_code=404, detail="No data found for the specified period")

    return result
