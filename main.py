from fastapi import FastAPI
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Разрешить все домены
    allow_credentials=True,
    allow_methods=["*"],        # Разрешить все HTTP-методы (GET, POST, PUT, DELETE, ...)
    allow_headers=["*"],        # Разрешить любые заголовки
)

@app.get('/')
async def home():
    return {
        "message": "Hello World"
    }

@app.get('/todo')
async def get_todo_data():
    with open("data.json", "r") as file:
        data_json = json.loads(file.read())

    return data_json

class DataModel(BaseModel):
    data: Any

@app.patch('/todo')
async def edit_todo_data(data: DataModel):
    url = os.getenv('GITHUB_GISTS_URL')
    token = os.getenv('GITHUB_KEY')

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }

    body = {
        "description": "change file data.json",
        "files": {
            "data.json": {
                "content": json.dumps(data.data)
            }
        }
    }

    response = requests.patch(url, headers=headers, data=json.dumps(body))

    with open("data.json", "w", encoding='utf-8') as file:
        file.write(json.dumps(data.data, ensure_ascii=False))


    return {"message": response.status_code}
