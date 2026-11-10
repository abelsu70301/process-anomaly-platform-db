#因為 Note CRUD 已經移到 app/api/notes.py，資料庫 Session、404、Note Model 都會在那邊使用
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path
from fastapi.staticfiles import StaticFiles  #StaticFiles → 讓 FastAPI 可以提供靜態檔案（圖片、CSS、JS 等等）
from app.api import notes, users, subclass, auth, root  #把 notes.py 裡的 API 路徑都掛到這個 FastAPI 應用程式裡
from pydantic import BaseModel
import uuid  #讓每一個 Request 都有自己的唯一編號
import time
from app.logging_db import save_log, save_session

class Item(BaseModel) : #class 定義類別 #Item 類別名稱 #繼承BaseModel
    name : str
    price : float

#()表示我們要呼叫這個 class，建立一個 FastAPI 應用程式物件（instance）
app = FastAPI(
    root_path="/s115321542",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

def error_response(request: Request, status: int, code: str, message: str):
    request.state.error_code = code
    request.state.error_message = message
    #Exception Handler 發現錯誤 - 把錯誤代碼和訊息先存在這次 request 裡

    return JSONResponse(
        status_code=status,
        content={
            "success": False,
            "error": {
                "code": code,
                "message": message
            }
        }
    )

#任何API request 都先經過這個 middleware
@app.middleware("http")  #request進來 - 產生uuid - 存到request.state.request_id - 執行真正API - 把Request ID 放進 Response Header - 回傳
async def request_id_middleware(request: Request, call_next):
    start = time.perf_counter()

    request.state.request_id = uuid.uuid4()

    session_id = request.cookies.get("api_session")  #看瀏覽器有沒有帶 api_session cookie

    client_ip = request.client.host if request.client else None

    if session_id is None:  #若沒有，產生新的 UUID
        session_id = str(uuid.uuid4())  #若有，沿用原本的值

    request.state.session_id = session_id
    request.state.member_id = None
    request.state.error_code = None
    request.state.error_message = None

    try:
        response = await call_next(request)

    except Exception:
        response = error_response(
            request, 500, "INTERNAL_ERROR", "伺服器內部錯誤"
        )

    if "api_session" not in request.cookies:  #如果這次 Request 原本沒有 api_session
        response.set_cookie(key="api_session", value=session_id, httponly= True, samesite="lax")
        #httponly= True: 代表 JavaScript 不能直接讀這個 Cookie，安全性比較好  #samesite="lax": 限制跨網站情境下 Cookie 的傳送方式
    duration = (time.perf_counter() - start) * 1000

    log_data = {  #把原本 Terminal 上看到的資訊包成一個 dictionary
        "session_id": session_id,
        "request_id": request.state.request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": duration,
        "error_code": request.state.error_code,
        "message": request.state.error_message

    }

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{duration:.2f} ms "
        f"request_id={request.state.request_id}"
    )

    tasks = BackgroundTasks()  #API → 把 save_log 放進 BackgroundTasks
    tasks.add_task(save_session, session_id, client_ip, request.state.member_id)
    tasks.add_task(save_log, log_data)

    response.background = tasks

    response.headers["X-Request-ID"] = str(
        request.state.request_id
    )

    return response

@app.exception_handler(StarletteHTTPException)  #FastAPI 只要遇到 HTTP 類型的錯誤，就交給 http_error() 處理
async def http_error(request: Request, exc: StarletteHTTPException):
    return error_response(request, exc.status_code, f"HTTP_{exc.status_code}", str(exc.detail))  #exc.status_code, Ex:404  #exc.detail, Ex:Not found
    #error_response() 把它整理成我們統一的 JSON 格式
#從目前的main.py檔案，往上找三層資料夾，找到 WEB/site 這個資料夾進入
PUBLIC_DIRECTORY = (
    Path(__file__).resolve().parents[3]
    / "WEB"
    / "site"
)

@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    return error_response(request, 422, "VALIDATION_ERROR", "請求參數驗證失敗")  #422: FastAPI 驗證輸入資料失敗 → RequestValidationError

@app.exception_handler(Exception)
async def unexpected_error(request: Request, exc: Exception):
    return error_response(request, 500, "INTERNAL_ERROR", "伺服器內部錯誤")


app.include_router(notes.router, prefix="/api")  #notes 裡所有 API 註冊到 FastAPI，並且在網址前面統一加上 /api
app.include_router(users.router, prefix="/api")
app.include_router(subclass.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(root.router, prefix="/api")

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
