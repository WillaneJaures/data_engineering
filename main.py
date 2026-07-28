import pandas as pd
import os
import requests
import sqlite3
from dotenv import load_dotenv
import json
from rich import print_json

load_dotenv()


TOKEN = os.getenv("TOKEN")

ville = "Dakar"

def ingest_data():
    url=f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={TOKEN}"
    response = requests.get(url)
    data = response.json()
    return data

def transform_data(data):
    dic = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "country": data["sys"]["country"],
        "weather_description": data["weather"][0]["description"]
    }
    df = pd.DataFrame([dic])
    return df

if __name__ == "__main__":
    data = ingest_data()
    df = transform_data(data)
    #print(json.dumps(data, indent=4))
    print_json(data=data)
    print("========================================================")
    print(df)

    
    

