from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta

import logging
import os
import requests
import sqlite3
import pandas as pd

from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

API_KEY = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_etl",
    default_args=default_args,
    description="ETL Weather Pipeline",
    schedule="@daily",
    start_date=datetime(2026, 7, 25),
    catchup=False,
) as dag:

    @task
    def extract():
        cities = [
            "Dakar",
            "Libreville",
            "Abidjan",
            "Lagos",
            "Accra"
        ]

        weather_data = []

        for city in cities:
            try:
                url = (
                    f"https://api.openweathermap.org/data/2.5/weather"
                    f"?q={city}&appid={API_KEY}"
                )

                response = requests.get(url)
                response.raise_for_status()

                weather_data.append(response.json())

                logging.info(f"Données récupérées pour {city}")

            except requests.exceptions.RequestException as e:
                logging.error(f"Erreur pour {city}: {e}")

        return weather_data

    @task
    def transform(data):

        weather = []

        for city_data in data:

            city_weather = {
                "city": city_data["name"],
                "humidity": city_data["main"]["humidity"],
                "temperature": city_data["main"]["temp"],
                "pressure": city_data["main"]["pressure"],
                "wind_speed": city_data["wind"]["speed"],
            }

            weather.append(city_weather)

        #df = pd.DataFrame(weather)

        logging.info("Transformation terminée")

        return weather

    @task
    def load(weather):

        df = pd.DataFrame(weather)

        db_path = "weather_data.db"

        try:

            conn = sqlite3.connect(db_path)

            logging.info(f"Connexion à {db_path}")

            df.to_sql(
                "weather",
                conn,
                if_exists="replace",
                index=False
            )

            conn.commit()
            conn.close()

            logging.info("Chargement terminé dans SQLite")

        except sqlite3.Error as e:
            logging.error(f"Erreur SQLite : {e}")

    extracted_data = extract()

    transformed_data = transform(extracted_data)

    load(transformed_data)