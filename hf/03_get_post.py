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




# 쿼리 매개변수 > ? 뒤에 온다
# http://127.0.0.1:8000/items/3?discount=true
@app.get("/products/{item_id}")   # ← 경로를 다르게 변경
def get_item(item_id: int, discount: bool = False):
    item_msg = f"{discount} 할인여부"
    return item_msg



# http://127.0.0.1:8000/items/3/orders/2
@app.get("/items/{item_id}/orders/{order_id}")
def get_item_orders(item_id: int, order_id: int):
    print("get_item_orders")
    return {"item_id": item_id, "order_id": order_id}



# /stocks/005930/history?days=60&market=kospi
@app.get("/stocks/{ticker}/history")
def get_stock_history(ticker: str, days: int = 30, market: str    = "kospi"):
    print("get_stock_history > 종목 이력을 조회합니다.")
    return {"ticker": "", "days": 60, "history": "구현 예정입니다."}       



from pydantic import BaseModel
class News(BaseModel):
    title: str
    content: str
    views: int = 0


@app.post("/news")
def anal_news(data: News):
    return {"news": data}



class StockRequest(BaseModel):
    ticker: str
    days: int = 30
    market: str = "kospi"

@app.post("/stocks/history")
def get_stock_history(data: StockRequest):
    print("get_stock_history > 종목 이력을 조회합니다.")
    return {"ticker": data.ticker, "days": data.days, "history": "구현 예정입니다."}









# uvicorn 03_get_post:app --reload --port 8001
# http://127.0.0.1:8001/hello





