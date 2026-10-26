# 製程異常分析與可疑因子平台｜資料庫系統實作紀錄

> 課程：資料庫系統  
> 更新日期：2026-10-19  
> 專案：製程異常分析與可疑因子平台  
> 本文件記錄資料庫系統課程之學習、實作、驗收與個人專案規劃。

---

## 專案說明

本專案建立可透過瀏覽器操作的製程異常分析平台，協助工程師查看製程／設備資料、異常預測結果與優先注意的可疑因子。

資料庫系統課程主要負責後端與資料層，包括：

- PostgreSQL 資料庫
- 資料表與關聯設計
- FastAPI 後端 API
- 資料驗證與 CRUD
- 分析結果保存
- View 與跨表查詢
- 身分驗證
- 測試、Logging 與部署

Web 程式設計課則主要負責：

- Web UI
- HTML／CSS／JavaScript
- 使用者操作流程
- 表單與前端互動
- 前端呼叫後端 API

目前專案資料夾大致分為：

    Process_Anomaly_Platform/
    ├─ DB/
    │  └─ api/
    │     ├─ app/
    │     ├─ alembic/
    │     ├─ requirements.txt
    │     └─ run.bat
    └─ WEB/
       └─ site/
          ├─ index.html
          ├─ app.js
          └─ css/

目前開發與展示皆以公開資料或模擬資料進行，不放入真實公司資料、個資或實驗室敏感資訊。

平台輸出的「可疑因子」只提供工程師後續調查方向，不直接代表已確認根因。

---

## W01：FastAPI 專案架構與基礎 API

### 學習目標

1. 建立 Python FastAPI 專案。
2. 理解 FastAPI、瀏覽器與 API 的基本關係。
3. 使用 Swagger UI 測試 API。
4. 使用 Python 虛擬環境管理專案套件。
5. 使用 Git 與 GitHub 管理程式版本。

### 為什麼這樣安排

後續資料庫、CRUD、登入與分析功能都需要建立在可正常運作的後端服務上，因此第一週先建立 FastAPI 專案骨架。

先確認：

    Browser
    ↓
    FastAPI
    ↓
    HTTP Response

能正常運作，再逐步加入 PostgreSQL 與其他功能。

### 操作步驟

1. 建立 `api` 專案目錄。
2. 建立 Python `venv`。
3. 安裝 FastAPI 與 Uvicorn。
4. 建立 `app/main.py`。
5. 建立基本 API。
6. 使用 Swagger UI 測試 API。
7. 建立 `requirements.txt`、`.gitignore` 與 GitHub repository。

目前使用過的基本 API 包含：

    /api/health
    /api/version
    /api/items

其中 `/api/version` 可用來確認目前後端版本，`/api/health` 用來確認服務是否正常，`/api/items` 則用來練習 POST 與資料型別驗證。

### 專案實作安排

FastAPI 作為本專案後端入口。

後續所有資料庫與分析功能都會逐步加入此服務，例如：

    Dataset
    DatasetVersion
    AnalysisRun
    AnalysisMetric
    SuspectedFactor
    AnalysisNote

目前 W01 階段先以基本 API 練習為主，不急著加入正式專案資料表。

### 本週練習

- 建立 FastAPI 專案。
- 建立 `/health`。
- 建立 `/version`。
- 使用 Pydantic 建立 Item Schema。
- 建立 `POST /items`。
- 開啟 Swagger UI。
- 建立 Python 虛擬環境。
- 建立 Git repository。
- 建立 `.gitignore`。
- 使用 Git 管理專案版本。

### 驗收標準

- [x] 已建立 Python venv。
- [x] 已建立 FastAPI 專案。
- [x] FastAPI 可以正常啟動。
- [x] Swagger UI 可以正常開啟。
- [x] `/version` 回傳 `0.1.0`。
- [x] `POST /items` 已建立。
- [x] GitHub repository 已建立。
- [ ] 補做一次錯誤資料型別測試，確認 FastAPI 的錯誤回應。
- [ ] 確認 `.env.example` 已提交且沒有敏感資料。
- [ ] 完成本次最新版本 commit 與 push。

### 學習心得

FastAPI 是後端 HTTP Server，可以依照不同 URL 與 HTTP Method 執行不同 Python function。

例如：

    @app.get("/api/health")

可以理解成：

    Client 發送 GET /api/health
    ↓
    FastAPI 找到對應的 function
    ↓
    執行 Python 程式
    ↓
    回傳 HTTP Response

Python 虛擬環境 `venv` 則是用來隔離不同專案的套件與版本，避免不同專案互相影響。

Swagger UI 可以讓我們不用自己額外寫前端，也能直接測試目前建立的 API，因此很適合在後端開發階段做驗證。

---

## W02：PostgreSQL 安裝與連線

### 學習目標

1. 建立 PostgreSQL 開發環境。
2. 理解 Database、Table、Column、Row。
3. 使用 SQL 新增與查詢資料。
4. 讓 Python 成功連線 PostgreSQL。
5. 使用 FastAPI API 查詢資料庫資料。
6. 初步理解 SQLAlchemy ORM 與 Alembic Migration。

### 為什麼這樣安排

在建立完整 CRUD 或正式專案資料表之前，先確認：

    PostgreSQL 本身正常
    ↓
    Python 可以連線 PostgreSQL
    ↓
    SQLAlchemy 可以操作資料
    ↓
    FastAPI 可以取得資料

這樣之後發生問題時，才能較容易判斷是：

- PostgreSQL 本身的問題
- Python connection 問題
- SQLAlchemy ORM 問題
- FastAPI API 問題

### 操作步驟

1. 安裝並啟動 PostgreSQL。
2. 使用 pgAdmin 管理 PostgreSQL。
3. 建立開發資料庫。
4. 使用 `.env` 保存資料庫連線設定。
5. 建立 `notes` table。
6. 使用 SQL 練習 `INSERT` 與 `SELECT`。
7. 建立 `database.py`。
8. 建立 SQLAlchemy `engine`、`SessionLocal`、`Base` 與 `get_db()`。
9. 建立 `Note` ORM Model。
10. 使用 Alembic 建立與更新資料表。
11. 建立單筆查詢 API。
12. 使用 Swagger 測試 API 是否能讀取 PostgreSQL 資料。

實際操作過的查詢：

    SELECT * FROM notes;

目前已建立三筆測試資料：

    W2 Note 1
    W2 Note 2
    W2 Note 3

並成功查詢。

### 專案實作安排

目前 `notes` 只是課程練習用資料表，不直接作為正式製程資料。

後續專案預計會逐步建立：

    users
    datasets
    dataset_versions
    analysis_runs
    analysis_metrics
    suspected_factors
    analysis_notes

目前先利用 `notes` 練習：

- PostgreSQL
- SQL
- SQLAlchemy ORM
- FastAPI API
- Alembic Migration
- CRUD

等基本概念。

### 本週練習

- 建立 `notes` table。
- 手動新增 3 筆測試資料。
- 使用 `SELECT * FROM notes` 查詢。
- 建立 Python 與 PostgreSQL 連線。
- 建立 `Note` ORM Model。
- 使用 Alembic 建立 Migration。
- 新增 `is_archived` 欄位。
- 建立單筆資料查詢 API。
- 使用 Swagger 查詢指定 note。

### 驗收標準

- [x] PostgreSQL 已建置。
- [x] pgAdmin 可正常使用。
- [x] `notes` table 已建立。
- [x] 已 INSERT 3 筆測試資料。
- [x] `SELECT * FROM notes` 成功。
- [x] Python 可連線 PostgreSQL。
- [x] SQLAlchemy connection 已建立。
- [x] `Note` ORM Model 已建立。
- [x] Alembic Migration 已建立並執行。
- [x] `notes` 已新增 `is_archived` 欄位。
- [x] `/api/note/{note_id}` 已建立。
- [x] Swagger 測試 `/api/note/2` 成功回傳 `200 OK`。
- [x] 能說明 `.env` 不應提交敏感資訊。
- [ ] 補測不存在的 `note_id` 是否正確回傳 `404`。
- [ ] 完成本次最新版本 commit 與 push。

### 學習心得

目前資料流可以理解為：

    Swagger / Browser
    ↓
    FastAPI
    ↓
    get_db()
    ↓
    SQLAlchemy Session
    ↓
    Note ORM
    ↓
    PostgreSQL

`database.py` 中主要元件：

    Engine
    = SQLAlchemy 與 PostgreSQL 的主要連線入口

    SessionLocal
    = 建立 Session 的工廠

    Session
    = 實際進行資料庫操作的工作單位

    Base
    = ORM Model 的共同基底

`Note` ORM Model 可以理解為：

    Python class Note
    ↕
    PostgreSQL notes table

也就是使用 Python class 對應資料庫 table。

另外：

    default
    = SQLAlchemy／Python 端的預設值

    server_default
    = PostgreSQL Server 端的預設值

兩者作用位置不同。

Alembic 則是用來管理 Database Schema 的版本變更，例如：

    建立 notes table
    ↓
    新增 is_archived 欄位
    ↓
    產生新的 migration

這樣未來資料庫結構的修改就可以被記錄與追蹤，而不只是手動修改資料表。

---

## W03：Run FastAPI as Web App and API

### 學習目標

1. 使用 FastAPI 作為 HTTP Server。
2. 讓同一個 FastAPI 同時提供 Web App 與 API。
3. 將 API 統一整理到 `/api/` 路徑。
4. 使用 StaticFiles 提供 Web 前端檔案。
5. 使用 local IP 驗證服務。
6. 使用學校公開 HTTPS 網址驗證服務。
7. 理解 Browser Cache 對前端測試的影響。

### 為什麼這樣安排

原本 FastAPI 主要用來回傳 API。

W03 進一步將架構整理成：

    Browser
    ↓
    FastAPI :7777
    ├─ Web App
    │  └─ /
    │
    └─ API
       └─ /api/...

讓同一個 FastAPI HTTP Server 可以同時：

- 提供 HTML、CSS、JavaScript
- 接收與回傳 API Request
- 供前端直接呼叫後端 API

### 操作步驟

1. 將 DB 與 WEB 專案分開：

    Process_Anomaly_Platform/
    ├─ DB/
    │  └─ api/
    └─ WEB/
       └─ site/

2. 建立 `run.bat`。

目前內容：

    @echo off
    :: 不顯示每條批次指令

    :: 使用本專案 venv 的 Python 啟動 FastAPI
    :: %~dp0 = run.bat 所在資料夾
    "%~dp0venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload

    :: --host 0.0.0.0：允許 localhost 與 local IP 存取
    :: --port 7777：使用指定 port
    :: --reload：程式修改後自動重新載入

其中：

    %~dp0

代表：

    run.bat 所在的資料夾

因此：

    "%~dp0venv\Scripts\python.exe"

代表直接使用目前專案自己的 Python 虛擬環境，不依賴系統 Python。

3. 將 API 路徑統一整理成：

    /api/health
    /api/version
    /api/items
    /api/note/{note_id}
    /api/notes

4. 在 `main.py` 中設定前端 public directory：

    PUBLIC_DIRECTORY = (
        Path(__file__).resolve().parents[3]
        / "WEB"
        / "site"
    )

此路徑會從：

    DB/api/app/main.py

往上找到專案根目錄，再進入：

    WEB/site

5. 使用 StaticFiles 掛載 Web App：

    app.mount(
        "/",
        StaticFiles(directory=PUBLIC_DIRECTORY, html=True),
        name="web"
    )

可以理解成：

    Browser 開啟 /
    ↓
    FastAPI
    ↓
    StaticFiles
    ↓
    PUBLIC_DIRECTORY
    ↓
    WEB/site/index.html

6. 測試：

    /

可以正常顯示：

    WEB/site/index.html

並測試：

    /api/health

可以正常回傳 API Response。

7. 使用 local IP 測試。

8. 使用學校公開 HTTPS Demo 網址測試。

9. 修改前端內容後，分別使用：

    一般瀏覽器
    無痕模式
    F12 → Network → Disable Cache

測試 Browser Cache 是否影響畫面更新。

### 專案實作安排

FastAPI 現在同時提供：

    FastAPI :7777
    ├─ /              → Web UI
    ├─ /app.js        → JavaScript
    ├─ /css/...       → CSS
    └─ /api/...       → Backend API

Web UI 實際來源：

    WEB/site/
    ├─ index.html
    ├─ app.js
    └─ css/

因此後續 Web 課程所開發的前端頁面，可以由目前的 FastAPI Server 提供。

Public directory 只放準備提供給 Browser 的公開檔案。

不應放入：

    .env
    Database password
    Python backend source
    其他敏感設定檔

老師教材提到限制 StaticFiles 的公開檔案類型。

目前專案實際仍使用 `app.js`，因此暫時不額外建立只允許 `.html` 與 `.css` 的副檔名限制，避免 JavaScript 無法載入。

目前先確保 Public Directory 與 Backend、設定檔及敏感資料分離。

### 本週練習

- 建立 `run.bat`。
- 使用專案 venv Python 啟動 Uvicorn。
- 使用 `0.0.0.0:7777` 啟動 FastAPI。
- 使用 local IP 存取網站。
- 將 Web UI 設為網站 root。
- API 統一放到 `/api/`。
- 使用 StaticFiles 提供 HTML／CSS／JavaScript。
- 使用 Browser 測試 Web 與 API。
- 測試 Browser Cache。
- 使用學校公開 HTTPS Demo 網址存取。

### 驗收標準

- [x] `run.bat` 已建立。
- [x] FastAPI 可使用 port `7777`。
- [x] 使用 `0.0.0.0` 啟動服務。
- [x] local IP 可正常存取。
- [x] `/` 可正常顯示 `WEB/site/index.html`。
- [x] `/api/health` 可正常回傳資料。
- [x] Web App 與 API 可同時運作。
- [x] API 已統一使用 `/api/`。
- [x] StaticFiles 已成功提供 Web 前端資源。
- [x] Browser Cache 已實際測試。
- [x] 無痕模式可正常取得最新版頁面。
- [x] 學校公開 HTTPS 網址已成功存取。
- [ ] 若老師之後要求額外限制 StaticFiles 可公開副檔名，再依課堂要求調整；目前已將公開前端資料夾與後端、敏感設定分離。
- [ ] 完成本次最新版本 commit 與 push。

### 學習心得

W03 讓我理解 FastAPI 不只可以提供 API，也可以作為 Web Server 提供靜態前端檔案。

原本：

    Browser
    ↓
    FastAPI API

現在則變成：

    Browser
    ↓
    FastAPI
    ├─ Web App
    └─ API

`app.mount()`：

    app.mount(
        "/",
        StaticFiles(directory=PUBLIC_DIRECTORY, html=True),
        name="web"
    )

代表將某個資料夾掛載到 FastAPI 的某個 URL 路徑。

其中：

    "/"

表示網站根目錄。

    StaticFiles

表示提供已存在的靜態檔案，例如：

    HTML
    CSS
    JavaScript
    圖片

    directory=PUBLIC_DIRECTORY

表示 FastAPI 要去哪一個資料夾尋找前端檔案。

    html=True

表示以 HTML 網站模式提供檔案，開啟 `/` 時可以直接取得 `index.html`。

    name="web"

則是替這個 mount 取一個名稱，供 FastAPI 內部識別。

另外：

    127.0.0.1

只能由目前這台電腦自己存取。

    0.0.0.0

則代表 Server 監聽所有可用網路介面，因此除了 localhost，也可以透過 local IP 存取。

這次也理解 Browser Cache 可能造成前端檔案已修改，但瀏覽器仍顯示舊版本的情況。

遇到此問題時可以使用：

    無痕模式
    或
    F12 → Network → Disable Cache

協助排查。

---

## W01～W03 目前進度摘要

目前已完成：

    W01
    FastAPI 基礎架構
    ↓
    W02
    FastAPI + PostgreSQL
    ↓
    W03
    Web App + FastAPI API

目前系統基本架構已形成：

    Browser
    ↓
    FastAPI :7777
    ├─ WEB/site
    │  ├─ HTML
    │  ├─ CSS
    │  └─ JavaScript
    │
    └─ /api/
       ↓
    SQLAlchemy
       ↓
    PostgreSQL

下一階段將進入 W04 CRUD API 完整實作，確認：

    Create
    Read
    Update
    Delete

皆可透過 Swagger 正常操作 PostgreSQL 資料。

W01～W03 文件整理完成後，再統一進行：

    git status
    ↓
    確認變更
    ↓
    git add
    ↓
    git commit
    ↓
    git push

---

---

## W04：CRUD API 完整實作 {#CRUD}

### 學習目標

本週將 API 層與資料庫層串接，完成 RESTful CRUD，建立從 HTTP Request 到 PostgreSQL 的完整資料操作流程。

本週先使用 `Note` 完成 CRUD，再以 `User` 練習相同架構，確認能將 CRUD 架構套用至不同的 ORM Model。

### RESTful API

RESTful API 是一種以「資源（Resource）」為中心設計 HTTP API 的方式。

以 Note 為例：

```text
/api/notes/
```

代表 Note 集合，而：

```text
/api/notes/{note_id}
```

代表指定的一筆 Note。

透過不同 HTTP Method 表示不同操作：

| HTTP Method | CRUD | 功能 |
| --- | --- | --- |
| POST | Create | 新增資料 |
| GET | Read | 查詢資料 |
| PUT | Update | 修改資料 |
| DELETE | Delete | 刪除資料 |

### Schema 與 ORM Model

新增：

```text
app/schemas/note.py
```

使用 Pydantic Schema 區分 API 的輸入與輸出資料格式：

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
```

其中：

```text
NoteCreate
→ Client 傳給 API 的資料格式

NoteResponse
→ API 回傳給 Client 的資料格式

Note
→ SQLAlchemy ORM Model，負責 Python 與 PostgreSQL 之間的資料對應
```

### Note Router

新增：

```text
app/api/notes.py
```

設定：

```python
router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)
```

並完成：

```text
POST   /api/notes/
GET    /api/notes/
GET    /api/notes/{note_id}
PUT    /api/notes/{note_id}
DELETE /api/notes/{note_id}
```

在 `main.py` 中註冊：

```python
from app.api import notes

app.include_router(notes.router, prefix="/api")
```

因此：

```text
main.py       /api
notes router  /notes

→ /api/notes/
```

### Note CRUD

#### Create

```text
POST /api/notes/
```

執行流程：

```text
Request
↓
NoteCreate
↓
SQLAlchemy Note
↓
db.add()
↓
db.commit()
↓
db.refresh()
↓
PostgreSQL
↓
NoteResponse
```

#### Read All

```text
GET /api/notes/
```

使用：

```python
db.query(Note).all()
```

取得所有 Note。

#### Read One

```text
GET /api/notes/{note_id}
```

依照 `note_id` 查詢指定 Note。

若資料不存在：

```python
raise HTTPException(
    status_code=404,
    detail="Note not found"
)
```

#### Update

```text
PUT /api/notes/{note_id}
```

先找出原本資料，再更新欄位：

```python
for key, value in note_data.model_dump().items():
    setattr(note, key, value)
```

最後：

```python
db.commit()
db.refresh(note)
```

#### Delete

```text
DELETE /api/notes/{note_id}
```

使用：

```python
db.delete(note)
db.commit()
```

刪除指定資料。

### User CRUD 練習

完成 Note CRUD 後，再將相同架構套用到 `User`。

原有 User Model 欄位：

```text
id
email
hashed_password
created_at
```

新增：

```text
app/schemas/user.py
app/api/users.py
```

在 `main.py` 註冊：

```python
from app.api import notes, users

app.include_router(notes.router, prefix="/api")
app.include_router(users.router, prefix="/api")
```

完成：

```text
POST   /api/users/
GET    /api/users/
GET    /api/users/{user_id}
PUT    /api/users/{user_id}
DELETE /api/users/{user_id}
```

### 本週練習

1. 建立 `NoteCreate` 與 `NoteResponse` Schema。
2. 建立 Note Router。
3. 完成 Note 的 Create、Read、Update、Delete。
4. 將 Note Router 註冊至 `main.py`。
5. 使用 Swagger 測試完整 CRUD。
6. 找不到指定 Note 時回傳 `404 Not Found`。
7. 將相同 CRUD 架構套用到 User Model。

### 驗收標準

- [x] `POST /api/notes/` 可新增 Note
- [x] `GET /api/notes/` 可查詢全部 Note
- [x] `GET /api/notes/{note_id}` 可查詢單筆 Note
- [x] `PUT /api/notes/{note_id}` 可修改 Note
- [x] `DELETE /api/notes/{note_id}` 可刪除 Note
- [x] 查詢不存在的 Note 回傳 `404 Not Found`
- [x] User CRUD 完整實作
- [x] User 刪除後再次查詢回傳 `404 Not Found`
- [x] Swagger UI 可正常測試所有 API

### 心得

本週第一次完整串接：

```text
HTTP Request
↓
FastAPI Router
↓
Pydantic Schema
↓
SQLAlchemy ORM
↓
PostgreSQL
```

理解 `Model`、`Schema` 與 `Router` 的不同角色：

```text
Model
→ 定義資料庫資料與 Python Object 的對應

Schema
→ 定義 API 接收與回傳的資料格式

Router
→ 定義 API Path、HTTP Method 與 CRUD 邏輯
```

也實際理解：

```text
db.add()
→ 將新物件加入 Session

db.commit()
→ 將交易真正寫入資料庫

db.refresh()
→ 從資料庫重新取得最新資料

db.query()
→ 查詢資料

HTTPException(404)
→ 處理指定資源不存在的情況
```

完成 Note CRUD 後，再將相同架構套用至 User CRUD，確認 CRUD 的結構可以套用到不同資料 Entity。

目前 Note 與 User 主要仍是課程架構練習；後續正式專題會再將相同概念套用至製程異常分析平台所需要的 Dataset、Analysis Batch、Prediction Result 等資料。

---

---

## W05：關聯式設計：View {#DbView}

### 學習目標

本週從單一資料表 CRUD 進一步進入多資料表關聯，理解 Class、Inheritance、Object、CO 的資料關係，並使用 PostgreSQL Function 與 View 封裝常用資料操作與查詢。

本週將完成：

Class / Inheritance / Object / CO
↓
insertClass()
↓
vd_subclass / vd_objectlist / vd_object
↓
FastAPI API

### Class、Inheritance、Object、CO

建立：

class
inheritance
object
co

其中：

Class
→ 分類或功能目錄

Inheritance
→ Class 與 Class 的父子關係

Object
→ 實際功能或內容物件

CO
→ Class 與 Object 的關係

Inheritance 使用：

pcid
→ parent class id

ccid
→ child class id

兩者都是 Foreign Key：

inheritance.pcid
→ class.cid

inheritance.ccid
→ class.cid

CO 則使用：

cid
→ class.cid

oid
→ object.oid

並以：

(cid, oid)

作為 Composite Primary Key。

因為：

一個 Class 可以包含多個 Object
一個 Object 也可以屬於多個 Class

所以單獨的 cid 或 oid 都不能唯一辨識一筆關係。

### Identity

將：

class.cid
object.oid

設定為：

GENERATED BY DEFAULT AS IDENTITY

代表新增資料時，可以由 PostgreSQL 自動產生流水號。

其中：

PRIMARY KEY
→ 確保值唯一

IDENTITY
→ 自動產生編號

兩者功能不同，但可以同時使用。

### insertClass() Function

建立：

insertClass(pcid, pname, cname)

三個參數分別代表：

pcid
→ parent class id

pname
→ parent class name

cname
→ child class name

其中：

$1 = pcid
$2 = pname
$3 = cname

Function 內使用：

v_ccid
→ 暫存 child class 的 cid

parent_idpath
→ 暫存 parent class 的 idpath

執行流程：

確認 parent cid 存在
↓
確認 parent cid 與 pname 相符
↓
查詢是否已有同名 child
↓
沒有則新增 child
↓
取得 child cid
↓
建立 inheritance 關係
↓
取得 parent idpath
↓
更新 child 的 idpath / namepath
↓
回傳 child cid

目前使用專案情境建立：

首頁
└─ 製程異常分析平台
   ├─ 資料管理
   ├─ 分析設定
   ├─ 分析結果
   ├─ 歷史紀錄
   └─ 系統設定

### Database View

本週建立三個 View：

vd_subclass
vd_objectlist
vd_object

View 可以理解為：

JOIN / SELECT Query
↓
包成一個可以重複查詢的虛擬表

與 JOIN 的差別：

JOIN
→ 定義資料如何跨表組合

View
→ 將常用 Query 保存成可重複查詢的資料介面

### vd_subclass

建立：

vd_subclass

使用：

class(parent)
+
inheritance
+
class(child)

整理 parent 與 child Class 的關係。

目前可使用：

SELECT *
FROM vd_subclass
WHERE pcid = 1;

取得：

資料管理
分析設定
分析結果
歷史紀錄
系統設定

新增 API：

GET /api/subclass/pcid/{id}

例如：

GET /api/subclass/pcid/1

### Object 與 CO

目前在：

資料管理(cid=2)

底下建立三個 Object：

oid=1
→ 上傳資料集

oid=2
→ 資料品質檢查

oid=3
→ 版本管理

再透過 CO 建立：

cid | oid
2   | 1
2   | 2
2   | 3

代表：

資料管理
├─ 上傳資料集
├─ 資料品質檢查
└─ 版本管理

### vd_objectlist

建立：

vd_objectlist

用途為：

已知 cid
→ 查詢該 Class 底下有哪些 Object

新增 API：

GET /api/subclass/objectlist/cid/{id}

### vd_object

建立：

vd_object

目前依專案需求保留：

oid
title
class
des

用途為：

已知 oid
→ 查詢單一 Object 詳細內容

新增 API：

GET /api/subclass/object/{id}

### Subclass Router

新增：

app/api/subclass.py

並在 main.py 註冊：

from app.api import notes, users, subclass

app.include_router(subclass.router, prefix="/api")

因此：

main.py
/api

subclass router
/subclass

→ /api/subclass/...

資料查詢流程：

Request
↓
FastAPI Router
↓
Depends(get_db)
↓
SQLAlchemy Session
↓
db.execute()
↓
PostgreSQL View
↓
result.mappings()
↓
JSON Response

其中：

Depends(get_db)
→ 取得資料庫操作 Session

db.execute(...)
→ 真正執行 SQL

mappings().all()
→ 取得多筆資料

mappings().first()
→ 取得單筆資料

### API 最小授權原則

FastAPI 使用 dev_user 連線 PostgreSQL。

View 僅提供 API 需要的讀取權限：

GRANT SELECT ON vd_subclass TO dev_user;
GRANT SELECT ON vd_objectlist TO dev_user;
GRANT SELECT ON vd_object TO dev_user;

代表：

可以 SELECT
但沒有額外取得 INSERT / UPDATE / DELETE 權限

避免給 API 不需要的資料庫權限。

### 本週練習

1. 建立 academic.sql。
2. 建立 Class、Inheritance、Object、CO。
3. 建立 insertClass() Function。
4. 建立製程異常分析平台 Class 階層。
5. 建立 vd_subclass。
6. 建立 Object 與 CO 測試資料。
7. 建立 vd_objectlist。
8. 建立 vd_object。
9. 建立 Subclass Router。
10. 建立 /api/subclass/pcid/{id}。
11. 建立 /api/subclass/objectlist/cid/{id}。
12. 建立 /api/subclass/object/{id}。
13. 使用 Swagger 測試 API。
14. 設定 View 的 API 最小 SELECT 權限。

### 驗收標準

- [x] class table 已建立
- [x] inheritance table 已建立
- [x] object table 已建立
- [x] co table 已建立
- [x] insertClass() 已建立並成功執行
- [x] 製程異常分析平台 Class 階層已建立
- [x] vd_subclass 可正常查詢
- [x] vd_objectlist 可正常查詢
- [x] vd_object 可正常查詢
- [x] dev_user 已取得 View 的 SELECT 權限
- [x] /api/subclass/pcid/{id} 可正常回傳資料
- [x] /api/subclass/objectlist/cid/{id} 已建立
- [x] /api/subclass/object/{id} 已建立
- [x] Swagger UI 可正常測試 View API
- [ ] 完成本次最新版本 commit 與 push

### 心得

本週從 W04 的單一資料表 CRUD，進一步理解多資料表之間的關係。

Inheritance 與 CO 都屬於關係表，但用途不同：

Inheritance
→ Class ↔ Class

CO
→ Class ↔ Object

也理解 Composite Primary Key 的用途：

(cid, oid)

不是要求 cid 或 oid 各自唯一，而是要求這一組 Class-Object 關係不能重複。

本週也理解 Function 與 View 的用途：

Function
→ 將多個資料操作步驟包成一個可重複執行的流程

View
→ 將常用跨表查詢包成可重複查詢的虛擬表

FastAPI 端則進一步理解：

get_db()
→ 取得資料庫 Session

db.execute()
→ 執行 SQL

result.mappings()
→ 將查詢結果轉成可回傳的 mapping 資料

在 API 測試時曾遇到 500 Internal Server Error，最後透過 Uvicorn traceback 發現：

result.mapping()

應改為：

result.mappings()

也因此更理解 Swagger 顯示的 HTTP Error 與後端 traceback 是不同層次的資訊，除錯時不能只看 Swagger。

最後透過 GRANT SELECT 理解 API 最小授權原則：API 只取得真正需要的資料庫權限，不因方便而直接使用過大的資料庫權限。