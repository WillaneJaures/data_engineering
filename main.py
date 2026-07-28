#Pandas permet de manipuler des données sous forme de tableaux appelés DataFrame.
import pandas as pd

#Cette bibliothèque permet d'interagir avec le système d'exploitation.
import os

#Cette bibliothèque permet d'envoyer des requêtes HTTP. Permettant de communiquer avec des sites webs ou api
import requests

#Cette bibliothèque permet de communiquer avec une base de données SQLite.
import sqlite3

#Son rôle est de lire le fichier .env et charger toutes les variables d'env
from dotenv import load_dotenv

#Cette bibliothèque permet de manipuler les données JSON.
import json
from rich import print_json


#lecture du fichier .env
load_dotenv()

#recuperation de la cle 
TOKEN = os.getenv("TOKEN")

ville = "Dakar"

def ingest_data():
    url=f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={TOKEN}"

    #envoie une requete http get au server de openweather et le server repond
    response = requests.get(url)

    #on convertit la reponse en json
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

#execute le code si ce fichier est lance uniquement
if __name__ == "__main__":
    data = ingest_data()
    df = transform_data(data)
    #print(json.dumps(data, indent=4))
    print_json(data=data)
    print("========================================================")
    print(df)

    
    

