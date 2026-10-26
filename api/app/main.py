#因為 Note CRUD 已經移到 app/api/notes.py，資料庫 Session、404、Note Model 都會在那邊使用
from fastapi import FastAPI   
from pathlib import Path
from fastapi.staticfiles import StaticFiles  #StaticFiles → 讓 FastAPI 可以提供靜態檔案（圖片、CSS、JS 等等）
from app.api import notes, users, subclass  #把 notes.py 裡的 API 路徑都掛到這個 FastAPI 應用程式裡
from pydantic import BaseModel


class Item(BaseModel) : #class 定義類別 #Item 類別名稱 #繼承BaseModel
    name : str
    price : float

#()表示我們要呼叫這個 class，建立一個 FastAPI 應用程式物件（instance）
app = FastAPI(
    root_path="/s115321542",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

#從目前的main.py檔案，往上找三層資料夾，找到 WEB/site 這個資料夾進入
PUBLIC_DIRECTORY = (
    Path(__file__).resolve().parents[3]
    / "WEB"
    / "site"
)

app.include_router(notes.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(subclass.router, prefix="/api")

@app.get("/api/health")
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
    

@app.get("/api/version")
def get_version():
    return {"version" : "0.1.0"}

@app.post("/api/items")
def create_item(item : Item) : 
    #左邊 item 是參數名稱，右邊 Item 是剛剛定義的類別名稱
    #這個函式會接收一個叫做 item 的資料，而且這筆資料必須符合 Item 的規格
    return item #把剛剛收到並驗證過的 Item 回傳給 Client


#把某個資料夾當作網站的靜態檔案來源，掛在 / 路徑下
app.mount(  #mount"掛載"，把另一個內容來源掛到FastAPI某個路徑下
    "/",  #代表掛在網站根目錄
    StaticFiles(directory=PUBLIC_DIRECTORY, html=True),  #FastAPI/Starlette 提供的靜態檔案服務
    name="web" #幫此mount命名
)
#directory=PUBLIC_DIRECTORY:告訴 FastAPI 去哪找檔案，因為前面有定義所以是去site資料夾找
#html=True:表示用「HTML 網站模式」，當使用者請求 / 時，直接回傳 index.html
