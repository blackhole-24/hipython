from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "안녕하세요.."}

@app.post("/echo")
def echo(data: dict):
    return {"dict": data}

@app.get("/test1")
def root1():
    return {"name": "둘리"}

@app.get("/test2")
def root2():
    return {"name": ["둘리", "또치", "도우너"]}

@app.get("/test3")
def root3():
    return "<h1>안녕?</h1>"

@app.get("/test4")
def root4():
    return 2000


#경로매개변수, 핸들러
@app.get("/items/{item_id}")
def read_item(item_id: int):
    item_id = item_id*2
    print(str(item_id) + '를 받았습니다.')
    return {"ID":item_id}



