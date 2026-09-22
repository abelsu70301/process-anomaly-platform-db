from fastapi import FastAPI
# 從 fastapi 匯入 FastAPI
'''把 fastapi 這個第三方套件安裝到 venv 裡。

但是「安裝在電腦裡」不代表你的 main.py 自動就會使用它
從 fastapi 這個套件裡，把名為 FastAPI 的東西載入到目前的程式中，等等我要使用它。'''
from pydantic import BaseModel


class Item(BaseModel) : #class 定義類別 #Item 類別名稱 #繼承BaseModel
    name : str
    price : float

app = FastAPI()
#()表示我們要呼叫這個 class，建立一個 FastAPI 應用程式物件（instance）

@app.get("/health")
#GET 是 HTTP 的一種 Method（方法），主要用來「取得資料」
#@app 是FastAPI的decorator
#/health是路徑
#@把下面那個 Python 函式登記成某個 API 路徑要執行的處理函式

#GET /health
#「詢問這個後端服務目前是否正常運作。」
#health 在這裡不是「人的健康」，而是 系統健康狀態

def health_check():
#define，定義函式 後方加函式名稱，()內放參數，目前沒有，: 後表示接下來是函式內容
    return {"status" : "ok"}
#return 是「把結果回傳出去」
#{:}字典：status 這個欄位目前的值是 ok
#執行健康檢查後，回傳「status = ok」

#兩行要一起看：有人用 GET 呼叫 /health → 執行 health_check()
    

@app.get("/version")
def get_version():
    return {"version" : "1.0"}

@app.post("/items")
def create_item(item : Item) : 
    #左邊 item 是參數名稱，右邊 Item 是剛剛定義的類別名稱
    #這個函式會接收一個叫做 item 的資料，而且這筆資料必須符合 Item 的規格
    return item #把剛剛收到並驗證過的 Item 回傳給 Client





