import uvicorn
from fastapi import FastAPI

from src.application.v1.endpoints import open_tv
app = FastAPI(
    title="Globo Eng Dados Challange",
    description="FastApi to handle tv programs date medians",
    version="1.0.0"
)

app.include_router(open_tv.router, prefix="/api/v1", tags=["Webhooks"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)