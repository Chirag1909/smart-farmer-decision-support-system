from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv("../../processed_data/best_crop_mandi_ranking.csv")


@app.get("/")
def home():
    return {"message":"API Running"}


# get states
@app.get("/states")
def states():

    return sorted(df["state"].unique())


# crop recommendation
@app.get("/recommend/{state}")
def recommend(state:str):

    data = df[df["state"].str.lower()==state.lower()].head(5)

    results=[]

    for _,row in data.iterrows():

        revenue=row["expected_revenue"]
        cost=revenue*0.55
        profit=revenue-cost

        results.append({

            "crop":row["crop"],
            "yield":row["predicted_yield"],
            "price":row["modal_price"],
            "revenue":revenue,
            "profit":profit,
            "district":row["district"],
            "mandi":row["market"]

        })

    return results


# weather API
@app.get("/weather/{city}")
def weather(city:str):

    API_KEY="9809ac00cd0f719f6bb4f02ca140c36a"

    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    data=requests.get(url).json()

    return {

        "temperature":data["main"]["temp"],
        "humidity":data["main"]["humidity"],
        "condition":data["weather"][0]["main"]

    }