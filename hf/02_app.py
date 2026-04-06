from fastapi import FastAPI

app = FastAPI()

@app.get("/") #root url > http://ip:8000/
def root():
    return {"message": "Hello, FastAPI!"}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}^^"}