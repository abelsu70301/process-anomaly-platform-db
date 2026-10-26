# 製程異常分析與可疑因子平台 — 資料庫系統

本專案為資料庫系統課程實作，使用 FastAPI、PostgreSQL、
SQLAlchemy 與 Alembic，逐步建立製程異常分析平台的資料保存與 API。

## 專案目標

預計保存資料集版本、分析設定、模型評估結果、可疑因子排名
及工程師備註，支援後續查詢與案例比較。

可疑因子排名提供優先調查方向，實際異常原因仍需工程師
結合設備紀錄、現場狀況及製程知識確認。

## 目前實作

- 已建立 FastAPI 專案。
- 已完成 PostgreSQL 資料庫連線。
- 已使用 SQLAlchemy 建立 ORM Model。
- 已建立 notes、users 資料表相關 Model 與 Alembic 遷移檔。
- 已建立 notes 的 `is_archived` 欄位遷移檔。
- 已將 FastAPI 與 Web 靜態頁面整合。
- 已將 API 統一規劃於 `/api/` 路徑。
- 已完成 Note RESTful CRUD API。
- 已完成 User RESTful CRUD API。
- 已完成不存在資源時的 `404 Not Found` 錯誤處理。
- 已使用 Swagger UI 完成 CRUD 功能驗證。
- 已建立 Class、Inheritance、Object、CO 關聯式資料結構。
- 已建立 `insertClass()` PostgreSQL Function。
- 已建立 `vd_subclass`、`vd_objectlist`、`vd_object` View。
- 已建立 View 對應的 FastAPI API。
- 已使用 `GRANT SELECT` 設定 API 使用者的 View 最小讀取權限。
- 已使用 Swagger UI 驗證 View API。
- 完整平台功能持續開發中；各週進度與驗證紀錄見 `psql.md`。

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

### Users

```text
POST   /api/users/
GET    /api/users/
GET    /api/users/{user_id}
PUT    /api/users/{user_id}
DELETE /api/users/{user_id}
```

### Subclass / Object Views

```text
GET /api/subclass/pcid/{id}
GET /api/subclass/objectlist/cid/{id}
GET /api/subclass/object/{id}
```

其中：

```text
/api/subclass/pcid/{id}
→ 依 parent class id 查詢 child class

/api/subclass/objectlist/cid/{id}
→ 依 class id 查詢該分類底下的 Object

/api/subclass/object/{id}
→ 依 object id 查詢單一 Object 詳細資料
```

## 目前程式結構

```text
DB/
├─ api/
│  ├─ app/
│  │  ├─ api/
│  │  │  ├─ notes.py
│  │  │  ├─ users.py
│  │  │  └─ subclass.py
│  │  ├─ core/
│  │  │  └─ database.py
│  │  ├─ models/
│  │  │  ├─ note.py
│  │  │  └─ user.py
│  │  ├─ schemas/
│  │  │  ├─ note.py
│  │  │  └─ user.py
│  │  └─ main.py
│  ├─ alembic/
│  ├─ requirements.txt
│  └─ run.bat
├─ psql/
│  └─ academic.sql
├─ psql.md
├─ ai.md
└─ README.md
```

目前 API 架構分為：

```text
Router
→ 負責 API Path 與 CRUD／查詢操作

Schema
→ 負責 API 輸入與輸出資料格式

Model
→ 負責 SQLAlchemy ORM 與資料表對應

Database
→ 負責 PostgreSQL 連線與 Session

PostgreSQL View
→ 將常用的多資料表查詢整理成可重複使用的資料介面
```

W05 新增的 View API 資料流程：

```text
Browser / Swagger
↓
FastAPI Router
↓
get_db()
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

## 檔案說明

| 路徑 | 用途 |
|---|---|
| `api/app/api/` | FastAPI Router |
| `api/app/models/` | SQLAlchemy ORM Model |
| `api/app/schemas/` | Pydantic Schema |
| `api/app/core/` | 資料庫連線設定 |
| `api/alembic/` | 資料庫結構遷移 |
| `api/requirements.txt` | Python 套件清單 |
| `psql/academic.sql` | Class、Inheritance、Object、CO、Function 與 View |
| `psql.md` | 課程規劃與實作進度 |
| `ai.md` | AI 使用與問題排查紀錄 |

## 本機啟動

以下指令適用於 Windows PowerShell，從 DB 資料夾執行。

進入 API 資料夾：

```powershell
cd api
```

首次建立環境時執行：

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

已有虛擬環境者可直接啟動：

```powershell
.\run.bat
```

或使用：

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload
```

啟動後可開啟：

```text
首頁：
http://127.0.0.1:7777/

API 文件：
http://127.0.0.1:7777/api/docs
```

使用資料庫功能前，須先啟動 PostgreSQL，並在本機設定
`api/.env` 的資料庫連線資訊。

## 與學期專題的關係

目前 Note 與 User CRUD 主要作為資料庫課程的 API 與資料庫操作練習。

W05 的 Class、Inheritance、Object、CO 與 View 則用來練習：

```text
多資料表關聯
↓
Function
↓
View
↓
FastAPI API
```

課堂原始範例的資料情境已改為製程異常分析平台功能分類，例如：

```text
首頁
└─ 製程異常分析平台
   ├─ 資料管理
   ├─ 分析設定
   ├─ 分析結果
   ├─ 歷史紀錄
   └─ 系統設定
```

目前「資料管理」下的測試 Object 包含：

```text
上傳資料集
資料品質檢查
版本管理
```

這些資料目前主要用於練習 Class、Object、View 與 API 的關係，
不代表正式專題的最終資料庫 Entity 設計。

正式學期專題仍為：

**製程異常分析與可疑因子輔助平台**

後續將逐步把目前 CRUD 與資料庫架構套用到實際專題 Entity，例如：

```text
Dataset
Analysis Batch
Prediction Result
Model Version
Engineer Note
```

並持續完成：

```text
CSV 上傳
→ 資料品質檢查
→ 異常預測
→ 可疑因子排名
→ 分析結果保存
→ 歷史紀錄查詢
```

## 版本管理

`.env`、`venv` 與 Python 快取不納入 Git。

課程實作進度記錄於 `psql.md`，
AI 協助與問題排查記錄於 `ai.md`。