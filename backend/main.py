from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db

app = FastAPI(title="IoT Backend")


@app.get("/")
async def root():
    return {"message": "IoT Backend is running"}


@app.get("/health/db")
async def database_health(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(text("SELECT 2"))

    return {
        "database": "connected",
        "result": result.scalar_one(),
    }
