import json
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from functions.get_board_id import get_board_id

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"message": "success connection"}


@app.get("/board/{id}")
async def get_board(id: int):
    with open("data.json", "r") as file:
        data_json = json.loads(file.read())

    return get_board_id(id, data_json["boards"])


@app.get("/boards")
async def get_boards():
    with open("data.json", "r") as file:
        data_json = json.loads(file.read())

    boards = []

    for board in data_json["boards"]:
        boards.append(
            {
                "title": board["title"],
                "id": board["id"],
                "image_url": board["image_url"],
            }
        )

    return boards


class DataModel(BaseModel):
    data: Any
    id: int


@app.patch("/board")
async def edit_board(data: DataModel):
    with open("data.json", "r") as file:
        data_json = json.loads(file.read())
        for index, board in enumerate(data_json["boards"]):
            if int(board["id"]) == data.id:
                data_json["boards"][index]["lists"] = data.data
                break

    with open("data.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(data_json, ensure_ascii=False))

    return {"message": "OK"}


class BoardModel(BaseModel):
    title: str
    image_url: str


@app.post("/board")
async def add_board(board: BoardModel):
    with open("data.json", "r") as file:
        data_json = json.loads(file.read())

    data_json["boards"].append(
        {
            "title": board.title,
            "id": data_json["boardCount"],
            "image_url": board.image_url,
            "lists": [],
        }
    )

    data_json["boardCount"] += 1

    with open("data.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(data_json, ensure_ascii=False))


@app.delete("/board")
async def delete_board(id: int):
    with open("data.json", "r") as file:
        data_json = json.loads(file.read())

    data_json.remove(get_board_id(id, data_json))

    with open("data.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(data_json, ensure_ascii=False))
