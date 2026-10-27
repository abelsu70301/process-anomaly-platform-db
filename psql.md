# 製程異常分析與可疑因子平台｜資料庫系統實作紀錄

> 課程：資料庫系統  
> 專案：製程異常分析與可疑因子平台  
> 本文件記錄資料庫系統課程之學習、實作、驗收與專案應用。

---

## 專案說明

本專案建立可透過瀏覽器操作的製程異常分析平台，協助工程師查看製程／設備資料、異常預測結果與優先注意的可疑因子。

資料庫系統課程主要負責：

- PostgreSQL 資料庫
- 資料表與關聯設計
- FastAPI 後端 API
- 資料驗證與 CRUD
- View 與跨表查詢
- 身分驗證
- EER Model
- 分析結果保存
- 歷史資料查詢

Web 程式設計課則主要負責：

- Web UI
- HTML／CSS／JavaScript
- 使用者操作流程
- 表單與前端互動
- 前端呼叫後端 API

目前開發與展示皆使用公開或模擬資料，不使用真實公司資料、個資或其他敏感資訊。

平台輸出的「可疑因子」只提供工程師後續調查方向，不直接代表已確認的異常根因。

---

# W01：FastAPI 專案架構與基礎 API

## 學習目標

1. 建立 Python FastAPI 專案。
2. 理解 FastAPI、Browser 與 API 的基本關係。
3. 使用 Swagger UI 測試 API。
4. 使用 Python venv 管理專案環境。
5. 使用 Git 與 GitHub 管理版本。

## 基本架構

```text
Browser
↓
FastAPI
↓
HTTP Response
```

建立的基本 API：

```text
GET  /api/health
GET  /api/version
POST /api/items
```

## 本週實作

- 建立 Python venv。
- 安裝 FastAPI 與 Uvicorn。
- 建立 `app/main.py`。
- 建立基本 GET / POST API。
- 使用 Pydantic 驗證資料。
- 使用 Swagger UI 測試 API。
- 建立 `requirements.txt`。
- 建立 `.gitignore`。
- 建立 Git repository。

## 驗收

- [x] Python venv 可正常使用
- [x] FastAPI 可正常啟動
- [x] Swagger UI 可正常開啟
- [x] `/api/health` 可正常回應
- [x] `/api/version` 可正常回應
- [x] POST API 可接收資料
- [x] Git repository 已建立

## 心得

FastAPI 可以依 URL 與 HTTP Method 找到對應的 Python Function：

```text
Client Request
↓
FastAPI Route
↓
Python Function
↓
HTTP Response
```

Swagger UI 則可以在尚未完成前端時，直接測試後端 API。

---

# W02：PostgreSQL、SQLAlchemy 與 Alembic

## 學習目標

1. 建立 PostgreSQL 開發環境。
2. 理解 Database、Table、Column、Row。
3. 練習 SQL INSERT / SELECT。
4. 使用 Python 連線 PostgreSQL。
5. 使用 SQLAlchemy ORM。
6. 使用 Alembic 管理 Database Schema。

## PostgreSQL 與 FastAPI

資料流程：

```text
FastAPI
↓
get_db()
↓
SQLAlchemy Session
↓
ORM Model
↓
PostgreSQL
```

建立：

```text
notes
users
```

並使用 Alembic 新增：

```text
notes.is_archived
```

## SQLAlchemy 主要元件

```text
Engine
→ SQLAlchemy 與 PostgreSQL 的連線入口

SessionLocal
→ 建立 Session 的工廠

Session
→ 實際執行資料庫操作

Base
→ ORM Model 的共同基底
```

ORM Model 可以理解為：

```text
Python Class
↕
PostgreSQL Table
```

## Alembic

Alembic 用來記錄資料庫結構的變化：

```text
建立 Table
↓
修改 Column
↓
產生 Migration
↓
upgrade
```

因此資料庫結構的修改可以被追蹤與重現。

## 本週實作

- 建立 PostgreSQL。
- 建立開發 Database。
- 建立 `notes` Table。
- 建立 SQLAlchemy Engine / Session。
- 建立 Note ORM Model。
- 使用 Alembic Migration。
- 新增 `is_archived`。
- 使用 API 查詢 PostgreSQL 資料。

## 驗收

- [x] PostgreSQL 可正常使用
- [x] Python 可連線 PostgreSQL
- [x] Note ORM Model 已建立
- [x] Migration 可正常執行
- [x] `is_archived` 已新增
- [x] FastAPI 可讀取 PostgreSQL 資料

---

# W03：FastAPI 同時提供 Web App 與 API

## 學習目標

1. 使用 FastAPI 作為 HTTP Server。
2. 同時提供 Web App 與 API。
3. API 統一使用 `/api/`。
4. 使用 StaticFiles 提供 Web 前端。

## 架構

```text
Browser
↓
FastAPI :7777
├─ /
│  └─ Web App
│
└─ /api/
   └─ Backend API
```

Web 前端位於：

```text
WEB/site/
├─ index.html
├─ app.js
└─ css/
```

FastAPI 使用：

```python
app.mount(
    "/",
    StaticFiles(directory=PUBLIC_DIRECTORY, html=True),
    name="web"
)
```

提供靜態前端。

## `run.bat`

使用專案自己的 venv Python：

```bat
"%~dp0venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload
```

其中：

```text
0.0.0.0
→ 監聽所有網路介面

7777
→ FastAPI 使用的 Port

--reload
→ 程式修改後自動重新載入
```

## 本週實作

- 建立 `run.bat`
- FastAPI 使用 Port 7777
- API 統一為 `/api/...`
- Web App 掛載至 `/`
- StaticFiles 提供 HTML / CSS / JavaScript
- Local IP 測試
- Browser Cache 測試

## 驗收

- [x] `/` 可顯示 Web App
- [x] `/api/health` 可正常回應
- [x] Web 與 API 可同時運作
- [x] StaticFiles 可正常讀取前端資源

---

# W04：RESTful CRUD API

## 學習目標

將 API 層與資料庫層串接，完成完整 CRUD：

```text
Create
Read
Update
Delete
```

## RESTful API

以 Note 為例：

| HTTP Method | CRUD | 功能 |
|---|---|---|
| POST | Create | 新增 |
| GET | Read | 查詢 |
| PUT | Update | 修改 |
| DELETE | Delete | 刪除 |

建立：

```text
POST   /api/notes/
GET    /api/notes/
GET    /api/notes/{note_id}
PUT    /api/notes/{note_id}
DELETE /api/notes/{note_id}
```

以及：

```text
POST   /api/users/
GET    /api/users/
GET    /api/users/{user_id}
PUT    /api/users/{user_id}
DELETE /api/users/{user_id}
```

## Router / Schema / Model

```text
Router
→ API Path、HTTP Method、資料操作流程

Schema
→ API Input / Output 格式

Model
→ SQLAlchemy ORM 與 PostgreSQL Table 對應
```

資料流程：

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

常用 SQLAlchemy 操作：

```text
db.add()
→ 將物件加入 Session

db.commit()
→ 寫入 Database

db.refresh()
→ 重新取得最新資料

db.query()
→ 查詢資料

db.delete()
→ 刪除資料
```

## 本週實作

- Note CRUD
- User CRUD
- Pydantic Schema
- Router 分層
- ORM Model
- 404 Error Handling
- Swagger UI 測試

## 驗收

- [x] Note Create
- [x] Note Read All
- [x] Note Read One
- [x] Note Update
- [x] Note Delete
- [x] User CRUD
- [x] 不存在資料回傳 404
- [x] Swagger 可正常操作

---

# W05：關聯式設計、Function 與 View

## 學習目標

從單一資料表 CRUD 進一步進入多資料表關聯。

本週建立：

```text
Class
Inheritance
Object
CO
↓
Function
↓
View
↓
FastAPI API
```

## Class / Inheritance / Object / CO

```text
Class
→ 分類或功能目錄

Inheritance
→ Class 與 Class 的父子關係

Object
→ 實際功能或內容

CO
→ Class 與 Object 的關係
```

Inheritance：

```text
pcid
→ parent class id

ccid
→ child class id
```

CO：

```text
cid
→ class id

oid
→ object id
```

以：

```text
(cid, oid)
```

作為 Composite Primary Key。

## `insertClass()` Function

建立：

```text
insertClass(pcid, pname, cname)
```

主要流程：

```text
確認 Parent
↓
確認 Child 是否存在
↓
必要時建立 Child
↓
建立 Inheritance
↓
更新 Path
↓
回傳 Child cid
```

目前專案測試分類：

```text
首頁
└─ 製程異常分析平台
   ├─ 資料管理
   ├─ 分析設定
   ├─ 分析結果
   ├─ 歷史紀錄
   └─ 系統設定
```

## View

建立：

```text
vd_subclass
vd_objectlist
vd_object
```

### `vd_subclass`

用途：

```text
parent class id
↓
查詢 child class
```

API：

```text
GET /api/subclass/pcid/{id}
```

### `vd_objectlist`

用途：

```text
class id
↓
查詢該 Class 底下的 Object
```

API：

```text
GET /api/subclass/objectlist/cid/{id}
```

### `vd_object`

用途：

```text
object id
↓
查詢單一 Object
```

API：

```text
GET /api/subclass/object/{id}
```

## FastAPI 與 View

```text
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
```

## 最小授權

FastAPI 使用 `dev_user`。

View 僅給予：

```sql
GRANT SELECT ON vd_subclass TO dev_user;
GRANT SELECT ON vd_objectlist TO dev_user;
GRANT SELECT ON vd_object TO dev_user;
```

避免提供不需要的 INSERT / UPDATE / DELETE 權限。

## 驗收

- [x] Class 已建立
- [x] Inheritance 已建立
- [x] Object 已建立
- [x] CO 已建立
- [x] `insertClass()` 已建立
- [x] 三個 View 可正常查詢
- [x] View API 可正常使用
- [x] `dev_user` 已設定最小 SELECT 權限

## 心得

Function：

```text
將多步驟資料操作封裝成可重複執行流程
```

View：

```text
將常用 SELECT / JOIN 封裝成可重複查詢的虛擬表
```

---

# W06：Authentication、JWT 與受保護 API

## 學習目標

1. 理解 Authentication 與 Authorization。
2. 建立本地 Member。
3. 使用 JWT 表示登入身分。
4. 使用 Cookie 傳遞 JWT。
5. 建立 Current Member 驗證。
6. 保護需要登入的 API。
7. 理解 OAuth2 / OIDC 與本地 JWT 的關係。

---

## Authentication 與 Authorization

Authentication：

```text
你是誰？
```

例如：

```text
目前登入者
→ Member 1
```

Authorization：

```text
你可以做什麼？
```

例如：

```text
只有已登入 Member
→ 可以使用某些 API
```

目前 W06 先完成：

```text
Authentication
+
是否已登入的 API 保護
```

---

## OAuth2、OIDC 與 JWT

Google 登入的完整概念：

```text
Browser
↓
Google Login
↓
OIDC
↓
取得 sub / email / name
↓
建立或更新本地 Member
↓
建立本系統 JWT
↓
Cookie
↓
後續 API
```

其中：

```text
OAuth2
→ Authorization Framework

OIDC
→ 在 OAuth2 上加入 Identity

JWT
→ 本系統用來保存登入身分資訊的 Token
```

目前 Google OIDC 尚未實作完成，因此本週先使用測試 Member 驗證後半段流程：

```text
Member
↓
JWT
↓
Cookie
↓
Protected API
```

---

## Member Table

建立：

```text
member
```

主要欄位：

```text
mid
google_sub
email
name
is_active
created_at
last_login
```

### 欄位用途

```text
mid
→ 本系統 Member ID

google_sub
→ Google Account 穩定識別值

email
→ Email

name
→ 顯示名稱

is_active
→ 帳號是否可使用

created_at
→ 建立時間

last_login
→ 最近登入時間
```

`google_sub` 使用 UNIQUE，避免同一 Google Account 被建立成多個 Member。

---

## Member ORM Model

建立：

```text
app/models/member.py
```

用途：

```text
Python Member Object
↕
PostgreSQL member Table
```

---

## Repository

建立：

```text
app/repositories/member.py
```

目前主要 Function：

```text
upsert_member()
get_active_member_by_id()
```

### `upsert_member()`

流程：

```text
依 google_sub 查詢
↓
不存在
→ INSERT Member

已存在
→ UPDATE
   email
   name
   last_login
```

實際測試：

```text
第一次
google_sub = test-google-sub
→ 建立 mid = 1
```

再次使用相同 `google_sub`：

```text
email / name 更新
mid 仍然 = 1
```

確認沒有新增第二個 Member。

---

## Member Database 權限

FastAPI 使用 `dev_user`。

本週授權：

```sql
GRANT SELECT, INSERT, UPDATE
ON TABLE member
TO dev_user;

GRANT USAGE, SELECT
ON SEQUENCE member_mid_seq
TO dev_user;
```

目前不需要刪除 Member，因此不提供 DELETE。

符合：

```text
Least Privilege
→ 只提供功能真正需要的權限
```

---

## JWT

建立：

```text
app/core/security.py
```

主要 Function：

```text
create_access_token()
decode_access_token()
```

目前使用：

```text
HS256
```

Token 主要內容：

```text
sub
→ Member ID

iat
→ Issued At

exp
→ Expiration Time
```

目前：

```text
ACCESS_TOKEN_EXPIRE_SECONDS = 3600
```

也就是：

```text
1 小時
```

### 建立 Token

```text
member.mid
↓
create_access_token()
↓
JWT
```

### 驗證 Token

```text
JWT
↓
decode_access_token()
↓
驗證 Signature
↓
驗證 Expiration
↓
讀取 sub
↓
Member ID
```

JWT 不保存密碼。

JWT 主要利用 Signature 確認 Token 沒有被任意修改。

---

## Cookie

目前 API 從：

```text
access_token
```

Cookie 取得 JWT。

流程：

```text
Browser
↓
Cookie
↓
Request
↓
FastAPI
```

後續若使用 HttpOnly Cookie，JavaScript 不需要直接讀取 JWT。

---

## `get_current_member()`

建立：

```text
app/core/auth.py
```

流程：

```text
Request
↓
讀取 access_token Cookie
↓
沒有 Token
→ 401 Unauthorized

有 Token
↓
JWT Decode
↓
取得 member_id
↓
查詢 Member
↓
確認 is_active
↓
回傳 Member
```

即使 Token 尚未過期，如果：

```text
is_active = false
```

仍不允許使用受保護 API。

---

## `/api/auth/me`

建立：

```text
app/api/auth.py
```

API：

```text
GET /api/auth/me
```

用途：

```text
目前 Request
↓
驗證 JWT
↓
確認 Member
↓
回傳目前登入者
```

未登入：

```text
401 Unauthorized
```

使用合法測試 JWT：

```text
200 OK
```

並成功取得：

```text
mid
email
name
```

---

## Router 層級保護

Notes Router：

```python
router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    dependencies=[Depends(get_current_member)]
)
```

Subclass Router 同樣加入：

```text
Depends(get_current_member)
```

因此：

```text
Request
↓
Authentication
↓
原本 Endpoint
```

目前受保護：

```text
/api/notes/...
/api/subclass/...
```

測試：

```text
沒有 JWT
→ 401

合法 JWT
→ 200
```

---

## W06 本週實作

1. 建立 `member` Table。
2. 建立 Member ORM Model。
3. 建立 Member Repository。
4. 建立 Member Upsert。
5. 設定 `dev_user` 最小權限。
6. 安裝 JWT / Authentication 套件。
7. 建立 `security.py`。
8. 建立 JWT Create / Decode。
9. 建立 `auth.py`。
10. 建立 `get_current_member()`。
11. 建立 `/api/auth/me`。
12. 測試 401 / 200。
13. 保護 Notes Router。
14. 保護 Subclass Router。

---

## W06 驗收

- [x] Member Table 已建立
- [x] Member ORM Model 已建立
- [x] Member Repository 已建立
- [x] 第一次 Member 可 INSERT
- [x] 相同 `google_sub` 可 UPDATE
- [x] Member 最小資料庫權限已設定
- [x] JWT 可建立
- [x] JWT 可 Decode
- [x] Token Expiration 已設定
- [x] `/api/auth/me` 未登入回傳 401
- [x] `/api/auth/me` 合法 JWT 回傳 200
- [x] Notes Router 已保護
- [x] Subclass Router 已保護
- [ ] Google OIDC 登入流程

---

## W06 心得

本週理解登入並不是只有 Login Endpoint。

目前後端流程為：

```text
Member
↓
JWT
↓
Cookie
↓
每次 Request
↓
JWT 驗證
↓
Member 驗證
↓
Protected API
```

也理解：

```text
JWT
≠ Password

JWT
≠ Database Session
```

JWT 是由 Server 簽署的 Token，用來表示 Request 所代表的登入身分。

另外 Router 層級的：

```python
dependencies=[Depends(get_current_member)]
```

可以一次保護整組 API，不需要每個 Endpoint 都重複撰寫相同驗證。

---

# W07：EER Model and AI Gen Data

## 學習目標

1. 理解 PostgreSQL Schema。
2. 理解 EER 與 Inheritance。
3. 使用 Shared Primary Key 表達子類。
4. 將課堂 EER 範例轉成目前專案情境。
5. 建立 Dataset / Model / AnalysisRun。
6. 使用測試資料驗證 EER。
7. 建立可重複執行的 Virtual Data Script。

---

## PostgreSQL Schema

W07 建立：

```sql
CREATE SCHEMA IF NOT EXISTS process_eer;
```

並設定：

```sql
SET search_path TO process_eer, public;
```

目前：

```text
process_eer
→ W07 EER Model

public
→ 原本 W01～W06 Table / View
```

---

## Database 與 Schema

可以理解成：

```text
PostgreSQL Server
└─ Database
   ├─ public Schema
   └─ process_eer Schema
```

Schema 是同一個 Database 裡的 Namespace。

因此不同 Schema 可以存在同名 Table：

```text
public.object
process_eer.object
```

兩者是不同物件。

---

## `search_path`

設定：

```sql
SET search_path TO process_eer, public;
```

表示沒有明確指定 Schema 時：

```text
先找 process_eer
↓
找不到
↓
再找 public
```

例如：

```sql
SELECT * FROM object;
```

會優先查：

```text
process_eer.object
```

也可以明確寫：

```sql
SELECT *
FROM public.object;
```

或：

```sql
SELECT *
FROM process_eer.object;
```

---

## EER Model

老師課堂原始概念為：

```text
Object
└─ Member
   ├─ Faculty
   ├─ Staff
   └─ Student
```

本專案保留 EER Inheritance 概念，但改成：

```text
Object
├─ Dataset
├─ Model
└─ AnalysisRun
```

---

## Object

父類：

```text
Object
```

目前主要欄位：

```text
oid
object_type
created_at
```

`oid`：

```text
PRIMARY KEY
+
IDENTITY
```

由 PostgreSQL 自動產生。

---

## Shared Primary Key

Dataset：

```text
dataset.oid
```

同時是：

```text
PRIMARY KEY
+
FOREIGN KEY → object.oid
```

例如：

```text
object
oid = 1
object_type = dataset

dataset
oid = 1
dataset_name = AI4I 2020
```

兩筆資料不是兩個不同 Entity。

而是：

```text
同一個 Dataset Entity
↓
Object 保存共用資訊
Dataset 保存子類資訊
```

Model 與 AnalysisRun 也是相同概念。

---

## Dataset

建立：

```text
process_eer.dataset
```

欄位：

```text
oid
dataset_name
source
version
description
```

目前測試資料：

```text
oid = 1
dataset_name = AI4I 2020
source = UCI Machine Learning Repository
version = v1
```

---

## Model

建立：

```text
process_eer.model
```

欄位：

```text
oid
model_name
algorithm
version
description
```

目前：

```text
oid = 2
model_name = AI4I Failure Predictor
algorithm = Logistic Regression
version = v1
```

---

## AnalysisRun

建立：

```text
process_eer.analysis_run
```

欄位：

```text
oid
dataset_oid
model_oid
threshold
run_time
status
```

目前：

```text
oid = 3
dataset_oid = 1
model_oid = 2
threshold = 0.5000
status = completed
```

代表：

```text
AI4I 2020
↓
AnalysisRun 3
↑
AI4I Failure Predictor
```

---

## Dataset、Model 與 AnalysisRun

一個 Dataset 可以：

```text
Dataset A
├─ Model A
├─ Model B
└─ Model C
```

一個 Model 也可以：

```text
Model A
├─ Dataset A
├─ Dataset B
└─ Dataset C
```

因此：

```text
Dataset
↔
Model
```

可以透過：

```text
AnalysisRun
```

形成多對多關係。

每一筆 AnalysisRun 保存：

```text
哪一份 Dataset
+
哪一個 Model
+
哪一個 Threshold
+
什麼時間執行
+
執行狀態
```

---

## JOIN 驗證

使用：

```sql
SELECT
    r.oid AS run_oid,
    d.dataset_name,
    m.model_name,
    m.algorithm,
    r.threshold,
    r.status,
    r.run_time
FROM analysis_run r
JOIN dataset d
    ON r.dataset_oid = d.oid
JOIN model m
    ON r.model_oid = m.oid;
```

成功取得：

```text
run_oid = 3
dataset_name = AI4I 2020
model_name = AI4I Failure Predictor
algorithm = Logistic Regression
threshold = 0.5000
status = completed
```

確認：

```text
Dataset
↔
AnalysisRun
↔
Model
```

關聯正確。

---

## `process_eer.sql`

建立：

```text
psql/process_eer.sql
```

用途：

```text
CREATE process_eer Schema
↓
CREATE Object
↓
CREATE Dataset
↓
CREATE Model
↓
CREATE AnalysisRun
```

讓 EER 結構可以被 Git 保存，而不只是存在目前 Database。

---

## AI / Virtual Data

建立：

```text
psql/process_vdata.sql
```

目前不需要自行生成大量感測器數據。

因為：

```text
模型訓練 / Demo
→ 使用 AI4I 公開 Dataset

Database 練習
→ 需要 Dataset / Model / Run 等 Metadata
```

因此目前 Virtual Data 主要建立：

```text
Dataset
Model
AnalysisRun
```

作為資料庫關聯、View、API 與歷史紀錄測試資料。

---

## 避免重複測試資料

`process_vdata.sql` 使用：

```sql
WHERE NOT EXISTS (...)
```

執行流程：

```text
資料是否存在？
↓
是
→ 不 INSERT

否
→ INSERT
```

重複執行腳本結果：

```text
SET
INSERT 0 0
INSERT 0 0
INSERT 0 0
```

表示三筆測試資料已經存在，因此沒有再新增。

---

## Encoding

SQL File 第一行：

```sql
\encoding UTF8
```

用來指定 `psql` Client Encoding。

避免系統使用 BIG5 時，遇到 UTF-8 SQL File 產生編碼錯誤。

---

## W07 本週實作

1. 建立 `process_eer` Schema。
2. 設定 `search_path`。
3. 建立 Object Parent Entity。
4. 建立 Dataset。
5. 建立 Model。
6. 建立 AnalysisRun。
7. 使用 Shared Primary Key。
8. 建立 AI4I Dataset。
9. 建立 Logistic Regression Model。
10. 建立 AnalysisRun。
11. 使用 JOIN 驗證關聯。
12. 建立 `process_eer.sql`。
13. 建立 `process_vdata.sql`。
14. 使用 `WHERE NOT EXISTS` 避免測試資料重複。
15. 驗證 SQL File 可重複執行。

---

## W07 驗收

- [x] `process_eer` Schema 已建立
- [x] `search_path` 可正常設定
- [x] Object Table 已建立
- [x] Dataset Table 已建立
- [x] Model Table 已建立
- [x] AnalysisRun Table 已建立
- [x] Shared Primary Key 可正常運作
- [x] AI4I Dataset 已建立
- [x] Logistic Regression Model 已建立
- [x] AnalysisRun 已建立
- [x] Dataset / Model / Run JOIN 成功
- [x] `process_eer.sql` 已建立
- [x] `process_vdata.sql` 已建立
- [x] Virtual Data Script 可重複執行
- [x] UTF-8 Client Encoding 已設定

---

## W07 心得

本週理解 EER Inheritance 如何實際轉成 Relational Database。

例如：

```text
Object oid = 1
Dataset oid = 1
```

表示同一個 Entity 的不同層級資訊。

子類的 `oid` 同時具有：

```text
PRIMARY KEY
+
FOREIGN KEY
```

這就是目前使用的 Shared Primary Key。

另外，也更清楚 Dataset 與 Model 不應直接硬限制成單純一對多：

```text
Dataset
↔
Model
```

可以透過：

```text
AnalysisRun
```

記錄每一次實際分析。

這樣未來即使：

```text
相同 Dataset
+
相同 Model
+
不同 Threshold
```

仍可以保存成不同 Run。

目前 W07 的 EER Model 是課程實作版本，已開始接近正式專題的核心資料結構，但後續仍會依完整需求、資料生命週期與實際應用情境調整。

---

# W01～W07 目前進度摘要

目前已完成：

```text
W01
FastAPI
↓
W02
PostgreSQL + SQLAlchemy + Alembic
↓
W03
Web App + API
↓
W04
RESTful CRUD
↓
W05
Relationship + Function + View
↓
W06
Authentication + JWT
↓
W07
EER + Virtual Data
```

目前後端架構：

```text
Browser / Swagger
↓
FastAPI Router
↓
Authentication
↓
Schema / Repository / ORM
↓
PostgreSQL
├─ public
└─ process_eer
```

目前正式專題逐步形成的核心資料概念：

```text
Member
Dataset
Model
AnalysisRun
```

下一階段將繼續進入 Schema 與可重複使用的 Data View，並逐步將課堂資料庫概念整合到正式的製程異常分析平台。