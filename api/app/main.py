from fastapi import FastAPI, Depends, HTTPException  #HTTPException → 找不到資料時回傳 404
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles  #StaticFiles → 讓 FastAPI 可以提供靜態檔案（圖片、CSS、JS 等等）

from sqlalchemy.orm import Session  #Depends(get_db) → 幫這次 API 取得一個資料庫 Session ; Session → 實際操作資料庫
from app.core.database import get_db
from app.models.note import Note  #Note → 對應 PostgreSQL 的 notes table

# 從 fastapi 匯入 FastAPI
'''把 fastapi 這個第三方套件安裝到 venv 裡。

但是「安裝在電腦裡」不代表你的 main.py 自動就會使用它
從 fastapi 這個套件裡，把名為 FastAPI 的東西載入到目前的程式中，等等要使用它。'''
from pydantic import BaseModel


class Item(BaseModel) : #class 定義類別 #Item 類別名稱 #繼承BaseModel
    name : str
    price : float

class NoteCreate(BaseModel):  #NoteCreate = 新增 Note 時，前端可以送哪些資料
    title: str
    content: str | None = None


class NoteUpdate(BaseModel):  #NoteUpdate = 修改 Note 時，前端可以送哪些資料
    title: str
    content: str | None = None
    is_archived: bool = False


app = FastAPI(
    root_path="/s115321542",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)
#()表示我們要呼叫這個 class，建立一個 FastAPI 應用程式物件（instance）

'''@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Hello World</h1>" '''

#從目前的main.py檔案，往上找三層資料夾，找到 WEB/site 這個資料夾進入
PUBLIC_DIRECTORY = (
    Path(__file__).resolve().parents[3]
    / "WEB"
    / "site"
)

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

@app.get("/api/note/{note_id}")  #Get /note/2
def get_note(note_id: int, db: Session = Depends(get_db)):  #note_id = 2 ; Depends(get_db):取得 Session

    note = db.query(Note).filter(Note.id == note_id).first()  #db.query(Note):查 notes table ; filter(Note.id == 2):找 id=2 ; first():拿第一筆 回傳資料
    #到 notes 資料表裡，找 id 等於使用者傳進來 note_id 的第一筆資料

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at,
        "is_archived": note.is_archived
    }


# 查全部
@app.get("/api/notes")
def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()


# 新增
@app.post("/api/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(
        title=note.title,
        content=note.content
    )

    db.add(new_note)  # 告訴 Session 我要新增這筆
    db.commit()   # 正式寫入 PostgreSQL
    db.refresh(new_note)  # 從 DB 重新取得新增後的資料

    return new_note


# 修改
@app.put("/api/notes/{note_id}")
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db_note.title = note.title
    db_note.content = note.content
    db_note.is_archived = note.is_archived

    db.commit()
    db.refresh(db_note)

    return db_note


# 刪除
@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(db_note)
    db.commit()

    return {"message": "Note deleted"}

#把某個資料夾當作網站的靜態檔案來源，掛在 / 路徑下
app.mount(  #mount"掛載"，把另一個內容來源掛到FastAPI某個路徑下
    "/",  #代表掛在網站根目錄
    StaticFiles(directory=PUBLIC_DIRECTORY, html=True),  #FastAPI/Starlette 提供的靜態檔案服務
    name="web" #幫此mount命名
)
#directory=PUBLIC_DIRECTORY:告訴 FastAPI 去哪找檔案，因為前面有定義所以是去site資料夾找
#html=True:表示用「HTML 網站模式」，當使用者請求 / 時，直接回傳 index.html
