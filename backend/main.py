from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import Todo
from database import (
    create_todo,
    fetch_all_todos,
    fetch_one_todo,
    remove_todo,
    update_todo,
)

app = FastAPI()


origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True, 
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.get("/")
def read_root():
    return {"Ping": "Pong"}


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response


@app.get("/api/todo{title}", response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response: 
        return response 
    else: 
        raise HTTPException(404, f"There is no TODO item called {title}")


@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response: 
        return response 
    else: 
        raise HTTPException(400, "Can not create given TODO item")


@app.put("/api/todo{title}", response_model=Todo)
async def put_todo(title: str, desc: str):
    response = await update_todo(title, desc) 
    if response: 
        return response
    else:
        raise HTTPException(404, f"There is no TODO item called {title}")


@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response: 
        return f"Succesfully deleted {title} item"
    else: 
        raise HTTPException(404, f"There is no TODO item called {title}")

