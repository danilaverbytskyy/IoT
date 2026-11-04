import os
from datetime import datetime
from zoneinfo import ZoneInfo

import psycopg2
import requests

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator


API_URL = "https://api.open-meteo.com/v1/forecast"

LATITUDE = 45.0453
LONGITUDE = 38.9818


def extract_transform_load():
    # 1. Extract: получаем данные из API
    response = requests.get(
        API_URL,
        params={
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "wind_speed_10m,"
                "weather_code"
            ),
            "timezone": "Europe/Moscow",
        },
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    current = data["current"]

    # Время наблюдения из ответа API
    observed_at = datetime.fromisoformat(
        current["time"]
    ).replace(tzinfo=ZoneInfo("Europe/Moscow"))

    # 2. Load: подключаемся к TimescaleDB/PostgreSQL
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=10,
    )

    try:
        with conn:
            with conn.cursor() as cur:
                # Создаём таблицу при первом запуске
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS weather_observations (
                        observed_at TIMESTAMPTZ PRIMARY KEY,
                        latitude DOUBLE PRECISION NOT NULL,
                        longitude DOUBLE PRECISION NOT NULL,
                        temperature DOUBLE PRECISION,
                        humidity INTEGER,
                        wind_speed DOUBLE PRECISION,
                        weather_code INTEGER
                    )
                """)

                # Сохраняем данные; повторная запись того же
                # времени обновит существующую строку
                cur.execute("""
                    INSERT INTO weather_observations (
                        observed_at,
                        latitude,
                        longitude,
                        temperature,
                        humidity,
                        wind_speed,
                        weather_code
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (observed_at)
                    DO UPDATE SET
                        temperature = EXCLUDED.temperature,
                        humidity = EXCLUDED.humidity,
                        wind_speed = EXCLUDED.wind_speed,
                        weather_code = EXCLUDED.weather_code
                """, (
                    observed_at,
                    LATITUDE,
                    LONGITUDE,
                    current.get("temperature_2m"),
                    current.get("relative_humidity_2m"),
                    current.get("wind_speed_10m"),
                    current.get("weather_code"),
                ))
    finally:
        conn.close()


with DAG(
    dag_id="open_meteo_weather_etl",
    description="Загрузка погоды Open-Meteo в PostgreSQL",
    start_date=pendulum.datetime(
        2026, 10, 28, tz="Europe/Moscow"
    ),
    schedule="@hourly",
    catchup=False,
    tags=["iot", "weather", "etl"],
) as dag:

    load_weather = PythonOperator(
        task_id="extract_transform_load",
        python_callable=extract_transform_load,
    )
