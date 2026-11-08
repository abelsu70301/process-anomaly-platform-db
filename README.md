# 製程異常分析與可疑因子平台 — 資料庫系統

本專案為資料庫系統課程實作，使用 FastAPI、PostgreSQL、SQLAlchemy 與 Alembic，逐步建立製程異常分析平台的後端與資料庫架構。

目前已完成 FastAPI 基礎架構、CRUD API、PostgreSQL Function / View、JWT 身分驗證，以及 EER Model 與 AI4I 測試資料。

---

## 專案目標

本專案預計建立一套可透過瀏覽器操作的製程異常分析平台，協助工程師進行：

- 製程／設備資料上傳
- 資料品質檢查
- 異常預測
- 模型評估
- 可疑因子排序
- 分析結果保存
- 工程師備註
- 歷史分析紀錄查詢

平台輸出的「可疑因子」主要提供工程師後續調查方向，不直接代表已確認的異常根因。

目前開發與展示主要使用公開資料集，現階段以 **AI4I 2020** 作為主要專案資料情境。

---

## 技術架構

目前使用：

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT
- HTML / CSS / JavaScript
- Git / GitHub

系統基本架構：

```text
Browser
↓
FastAPI
├─ Web App
└─ /api/
   ↓
Authentication
   ↓
SQLAlchemy / SQL
   ↓
PostgreSQL
```

---

## 目前開發進度

### W01：FastAPI 基礎架構

完成：

- FastAPI 專案建立
- Python venv
- Uvicorn
- 基礎 GET / POST API
- Swagger UI
- Pydantic 資料驗證
- Git / GitHub
- `requirements.txt`
- `.gitignore`

---

### W02：PostgreSQL 與 SQLAlchemy

完成：

- PostgreSQL 開發環境
- Python 連線 PostgreSQL
- SQLAlchemy Engine / Session
- ORM Model
- Alembic Migration
- `notes` Table
- `users` Table
- `notes.is_archived` 欄位
- FastAPI 查詢 PostgreSQL 資料

---

### W03：FastAPI Web App 與 API

完成：

- 建立 `run.bat`
- FastAPI 使用 Port 7777
- API 統一放在 `/api/`
- FastAPI 提供 `WEB/site` 靜態前端
- HTML / CSS / JavaScript 與 Backend 整合
- Local IP 測試
- Browser Cache 測試

---

### W04：RESTful CRUD API

完成 Note CRUD：

```text
POST   /api/notes/
GET    /api/notes/
GET    /api/notes/{note_id}
PUT    /api/notes/{note_id}
DELETE /api/notes/{note_id}
```

完成 User CRUD：

```text
POST   /api/users/
GET    /api/users/
GET    /api/users/{user_id}
PUT    /api/users/{user_id}
DELETE /api/users/{user_id}
```

並完成：

- Router / Schema / Model 分層
- `404 Not Found`
- Swagger CRUD 驗證

---

### W05：關聯式設計、Function 與 View

建立：

```text
Class
Inheritance
Object
CO
```

關係：

```text
Inheritance
→ Class ↔ Class

CO
→ Class ↔ Object
```

建立 PostgreSQL Function：

```text
insertClass()
```

建立 View：

```text
vd_subclass
vd_objectlist
vd_object
```

建立對應 API：

```text
GET /api/subclass/pcid/{id}
GET /api/subclass/objectlist/cid/{id}
GET /api/subclass/object/{id}
```

目前課程測試分類：

```text
首頁
└─ 製程異常分析平台
   ├─ 資料管理
   ├─ 分析設定
   ├─ 分析結果
   ├─ 歷史紀錄
   └─ 系統設定
```

「資料管理」測試 Object：

```text
上傳資料集
資料品質檢查
版本管理
```

FastAPI 使用 `dev_user` 連線 PostgreSQL，View 僅提供所需的 `SELECT` 權限。

---

### W06：Member、JWT 與 API 保護

建立 Member 資料結構：

```text
mid
google_sub
email
name
is_active
created_at
last_login
```

新增：

```text
app/models/member.py
app/repositories/member.py
app/core/security.py
app/core/auth.py
app/api/auth.py
```

Member Repository 支援：

```text
第一次登入
→ INSERT Member

相同 google_sub 再次登入
→ UPDATE Member
```

建立 JWT：

```text
member.mid
↓
create_access_token()
↓
JWT
```

JWT 目前包含：

```text
sub
iat
exp
```

目前登入驗證流程：

```text
Request
↓
access_token Cookie
↓
JWT Decode
↓
member_id
↓
查詢有效 Member
↓
Protected API
```

建立：

```text
GET /api/auth/me
```

測試結果：

```text
沒有 JWT
→ 401 Unauthorized

合法 JWT
→ 200 OK
```

目前已加入登入驗證的 Router：

```text
/api/notes/...
/api/subclass/...
```

Google OIDC 登入流程目前暫緩，現階段先完成本地 Member、JWT 與受保護 API 的核心流程。

---

### W07：EER Model 與 AI4I 測試資料

建立獨立 PostgreSQL Schema：

```text
process_eer
```

目前 EER Model：

```text
Object
├─ Dataset
├─ Model
└─ AnalysisRun
```

`Dataset`、`Model` 與 `AnalysisRun` 使用 Shared Primary Key 繼承 `Object`。

例如：

```text
object.oid = 1
dataset.oid = 1
```

代表同一個 Dataset Entity 在父類與子類 Table 中保存不同層級的資料。

Dataset 與 Model 透過 AnalysisRun 建立分析紀錄：

```text
Dataset
   ↓
AnalysisRun
   ↑
Model
```

因此：

```text
一個 Dataset
→ 可以搭配多個 Model

一個 Model
→ 可以搭配多個 Dataset
```

兩者可透過多筆 AnalysisRun 形成多對多關係。

目前測試資料：

```text
Dataset
→ AI4I 2020

Source
→ UCI Machine Learning Repository

Model
→ AI4I Failure Predictor

Algorithm
→ Logistic Regression

Threshold
→ 0.5000

Status
→ completed
```

建立：

```text
psql/process_eer.sql
psql/process_vdata.sql
```

用途：

```text
process_eer.sql
→ 建立 process_eer Schema
→ 建立 Object / Dataset / Model / AnalysisRun

process_vdata.sql
→ 建立 AI4I Dataset / Model / AnalysisRun 測試資料
```

`process_vdata.sql` 使用 `WHERE NOT EXISTS`，可重複執行而不重複新增相同測試資料。

---

## 目前 API

### System

```text
GET  /api/health
GET  /api/version
POST /api/items
```

### Notes

```text
POST   /api/notes/
GET    /api/notes/
GET    /api/notes/{note_id}
PUT    /api/notes/{note_id}
DELETE /api/notes/{note_id}
```

目前 Notes Router 需要 JWT 驗證。

### Users

```text
POST   /api/users/
GET    /api/users/
GET    /api/users/{user_id}
PUT    /api/users/{user_id}
DELETE /api/users/{user_id}
```

### Subclass / Object

```text
GET /api/subclass/pcid/{id}
GET /api/subclass/objectlist/cid/{id}
GET /api/subclass/object/{id}
```

用途：

```text
/api/subclass/pcid/{id}
→ 依 parent class id 查詢 child class

/api/subclass/objectlist/cid/{id}
→ 依 class id 查詢該分類下的 Object

/api/subclass/object/{id}
→ 依 object id 查詢單一 Object
```

目前 Subclass Router 需要 JWT 驗證。

### Auth

```text
GET /api/auth/me
```

用途：

```text
access_token Cookie
↓
JWT 驗證
↓
Member ID
↓
查詢 Member
↓
回傳目前登入者
```

---

## 目前專案結構

```text
DB/
├─ api/
│  ├─ app/
│  │  ├─ api/
│  │  │  ├─ auth.py
│  │  │  ├─ notes.py
│  │  │  ├─ subclass.py
│  │  │  └─ users.py
│  │  ├─ core/
│  │  │  ├─ auth.py
│  │  │  ├─ database.py
│  │  │  ├─ db_test.py
│  │  │  └─ security.py
│  │  ├─ models/
│  │  │  ├─ member.py
│  │  │  ├─ note.py
│  │  │  └─ user.py
│  │  ├─ repositories/
│  │  │  ├─ __init__.py
│  │  │  └─ member.py
│  │  ├─ schemas/
│  │  │  ├─ note.py
│  │  │  └─ user.py
│  │  └─ main.py
│  ├─ alembic/
│  ├─ requirements.txt
│  └─ run.bat
├─ psql/
│  ├─ academic.sql
│  ├─ process_eer.sql
│  └─ process_vdata.sql
├─ psql.md
├─ ai.md
└─ README.md
```

---

## 程式分層

### Router

```text
api/app/api/
```

負責：

- API Path
- HTTP Method
- Request 處理
- Response 回傳

### Schema

```text
api/app/schemas/
```

負責：

- API 輸入資料格式
- API 輸出資料格式
- Pydantic 資料驗證

### Model

```text
api/app/models/
```

負責：

- SQLAlchemy ORM
- Python Object 與 PostgreSQL Table 對應

### Repository

```text
api/app/repositories/
```

負責：

- 集中處理資料查詢
- INSERT / UPDATE
- 資料存取邏輯

### Core

```text
api/app/core/
```

目前包含：

```text
database.py
→ PostgreSQL Engine / Session

security.py
→ JWT 建立與驗證

auth.py
→ Current Member 驗證
```

---

## 主要檔案

| 路徑 | 用途 |
|---|---|
| `api/app/api/` | FastAPI Router |
| `api/app/api/auth.py` | Current Member API |
| `api/app/models/` | SQLAlchemy ORM Model |
| `api/app/models/member.py` | Member ORM Model |
| `api/app/schemas/` | Pydantic Schema |
| `api/app/repositories/` | Repository Layer |
| `api/app/repositories/member.py` | Member 查詢、新增與更新 |
| `api/app/core/database.py` | PostgreSQL Connection / Session |
| `api/app/core/security.py` | JWT 建立與驗證 |
| `api/app/core/auth.py` | Current Member Authentication |
| `api/alembic/` | Database Migration |
| `api/requirements.txt` | Python 套件 |
| `psql/academic.sql` | W05 Class / Inheritance / Object / CO / Function / View |
| `psql/process_eer.sql` | W07 EER Schema 與 Table |
| `psql/process_vdata.sql` | AI4I 測試資料 |
| `psql.md` | 資料庫系統課程學習與實作紀錄 |
| `ai.md` | AI 協助與 Debug 紀錄 |

---

## 本機啟動

以下指令適用於 Windows PowerShell。

進入 API 資料夾：

```powershell
cd api
```

首次建立環境：

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

啟動 FastAPI：

```powershell
.\run.bat
```

或：

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload
```

啟動後：

```text
首頁：
http://127.0.0.1:7777/

Swagger：
http://127.0.0.1:7777/api/docs
```

使用資料庫功能前需先啟動 PostgreSQL，並在本機設定：

```text
api/.env
```

`.env` 不納入 Git。

---

## 與正式學期專題的關係

目前部分內容仍屬於資料庫課程概念練習，例如：

```text
Note
User
Class
Inheritance
CO
```

主要用於學習：

```text
CRUD
↓
Relational Database
↓
Function
↓
View
↓
Authentication
↓
EER
```

正式專題為：

**製程異常分析與可疑因子輔助平台**

目前預計流程：

```text
CSV 上傳
↓
資料品質檢查
↓
模型推論
↓
異常預測
↓
可疑因子排序
↓
分析結果保存
↓
工程師備註
↓
歷史紀錄
```

目前主要使用 **AI4I 2020** 作為開發與展示資料。

W07 開始建立較接近正式專題的核心 Entity：

```text
Dataset
Model
AnalysisRun
```

但目前仍屬於課程階段的 EER Model，後續會依完整需求、資料生命週期與實際使用情境持續調整。

---

## 版本管理

以下內容不納入 Git：

```text
.env
venv
Secret Key
Token
Password
Python Cache
```

課程實作與學習紀錄：

```text
psql.md
```

AI 協助、實際修改與問題排查紀錄：

```text
ai.md
```

## Current Progress

目前已完成 Database 課程 W01～W08 的主要練習與 API 整合。

### Database

目前使用：

- PostgreSQL
- FastAPI
- SQLAlchemy
- Alembic

已完成：

- Notes / Users 基礎資料表
- Class / Inheritance / Object 關聯結構
- Database Views
- Subclass / Object List / Object Detail API

### Authentication

目前已完成基礎 Authentication 架構：

- `member` Table
- JWT Access Token
- Cookie 驗證
- `get_current_member`
- Protected API Router
- `/api/auth/me`

Google OIDC 正式登入目前暫未實作。

### EER Practice

新增：

```text
process_eer
```

Schema，作為 EER 練習模型。

目前結構：

```text
Object
├─ Dataset
├─ Model
└─ AnalysisRun
```

目前測試資料使用 AI4I 2020。

```text
Dataset
→ AI4I 2020

Model
→ AI4I Failure Predictor
→ Logistic Regression

AnalysisRun
→ Dataset + Model + Threshold
```

### Schema

目前 `fastapi_dev` 主要包含：

```text
fastapi_dev
├─ public
└─ process_eer
```

其中：

- `public`：主要應用程式資料表、Views 與 API 資料來源。
- `process_eer`：EER 練習模型。

已練習：

- Schema namespace
- 同名 Table 隔離
- `search_path`
- `schema.table` 明確指定資料來源

例如目前同時存在：

```text
public.object
process_eer.object
```

但兩者用途不同。

### Reuse Data Views

`public.vd_subclass` 已加入：

```text
n
```

欄位，用來表示每個 Child Class 直接關聯的 Object 數量。

目前分類：

```text
首頁
└─ 製程異常分析平台
   ├─ 資料管理
   ├─ 分析設定
   ├─ 分析結果
   ├─ 歷史紀錄
   └─ 系統設定
```

其中「資料管理」目前包含：

```text
上傳資料集
資料品質檢查
版本管理
```

### Repository Reuse

新增：

```text
app/repositories/subclass.py
```

將 subclass / object 相關 SQL 查詢集中管理。

目前共用函式：

```python
get_subclasses_by_pcid()
get_objects_by_cid()
get_object_by_oid()
```

目前架構：

```text
API Route
↓
Repository Function
↓
Database View
↓
PostgreSQL
```

這樣可以減少 API Route 中重複撰寫 SQL。

### Current APIs

目前主要 API：

```text
GET /api/root
GET /api/subclass/pcid/{id}
GET /api/subclass/objectlist/cid/{id}
GET /api/subclass/object/{id}
GET /api/auth/me
```

其中：

```text
/api/root
/api/subclass/pcid/{id}
```

皆共用：

```python
get_subclasses_by_pcid()
```

完成 W08 Reuse 的練習。

### Project Direction

本專案目前以：

```text
製程異常分析與可疑因子輔助平台
```

為主要應用方向。

預計系統流程：

```text
製程資料上傳
↓
資料品質檢查
↓
資料前處理
↓
異常分類 / 模型分析
↓
Precision / Recall / F1
↓
可疑因子排序
↓
分析結果保存
↓
歷史紀錄與工程師備註
```

目前 Database 課程仍以資料庫設計、EER、View、Authentication 與 API Reuse 為主要練習內容，後續再逐步整合至完整平台資料模型。

### Advanced Query

目前 `/api/subclass/objectlist/cid/{id}` 已支援進階查詢參數：

```text
page
page_size
class_name
search
```

已完成：

- Pagination：使用 `LIMIT` / `OFFSET` 進行分頁。
- Query Validation：限制 `page >= 1`、`page_size` 為 1～100。
- Filter：可依 `class_name` 進行精確篩選。
- Search：使用 PostgreSQL `ILIKE` 進行 `object_title` 關鍵字搜尋。

例如：

```text
GET /api/subclass/objectlist/cid/2?page=1&page_size=10&class_name=資料管理&search=資料
```

目前資料查詢流程：

```text
API Query Parameters
↓
Repository Function
↓
Database View
↓
PostgreSQL
↓
JSON Response
```