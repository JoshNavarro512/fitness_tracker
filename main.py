
import requests
from datetime import datetime
import os
import os
from dotenv import load_dotenv  

load_dotenv()

GENDER = "male"
WEIGHT_KG = 99.79
HEIGHT_CM = 187.96
AGE = 33



APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv('API_KEY')
print(APP_ID)
print(API_KEY)

NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEET_ENDPOINT =  os.getenv('SHEET_ENDPOINT')

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}


response = requests.post(NUTRITIONIX_ENDPOINT, json=parameters, headers=headers)
response.raise_for_status()

data = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in data["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    #Bearer Token Authentication
    bearer_headers = {
    "Authorization": f"Bearer {os.getenv('Token')}"
    }
    sheet_response = requests.post(
        SHEET_ENDPOINT, 
        json=sheet_inputs, 
        headers=bearer_headers
    )