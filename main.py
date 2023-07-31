from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

students={
    1:{
        'name':'john',
        'age':17,
        'year':'year 12'
    }
}

class Student(BaseModel):
    name:str
    age:int
    year:str



@app.get("/")
def home():
    return {"message":"hello!"}
