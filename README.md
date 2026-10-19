# 製程異常分析與可疑因子平台 — 資料庫系統

本專案為資料庫系統課程實作，使用 FastAPI、PostgreSQL、SQLAlchemy 與 Alembic，逐步建立製程異常分析平台的後端與資料庫功能。

平台預計保存資料集版本、分析設定、模型評估結果、可疑因子排名與工程師備註，支援後續查詢與案例比較。

可疑因子排名僅提供優先調查方向，實際異常原因仍需結合設備紀錄、現場狀況與製程知識確認。

---

## 目前進度

目前已完成：

- FastAPI 專案建立
- PostgreSQL 連線
- SQLAlchemy ORM 基礎設定
- Alembic Migration
- `notes`、`users` 相關資料表練習
- 單筆 Note 查詢 API
- FastAPI 同時提供 Web App 與 `/api/` API
- `run.bat` 啟動方式
- Local IP 與公開 HTTPS 存取驗證

目前正在進行：

- Notes CRUD API 完整驗證

完整每週實作與學習紀錄請參考 `psql.md`。

---

## 技術

- Python
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Alembic
- HTML
- CSS
- JavaScript
- Git / GitHub

---

## 專案結構

    Process_Anomaly_Platform/
    ├─ DB/
    │  ├─ README.md
    │  ├─ psql.md
    │  └─ api/
    │     ├─ app/
    │     ├─ alembic/
    │     ├─ requirements.txt
    │     └─ run.bat
    │
    └─ WEB/
       └─ site/
          ├─ index.html
          ├─ app.js
          └─ css/

主要用途：

| 路徑 | 用途 |
|---|---|
| `DB/api/app/` | FastAPI 後端程式 |
| `DB/api/alembic/` | 資料庫 Migration |
| `DB/api/requirements.txt` | Python 套件清單 |
| `DB/api/run.bat` | 啟動 FastAPI |
| `DB/psql.md` | 資料庫系統課程實作紀錄 |
| `WEB/site/` | Web 前端公開資源 |

---

## 本機啟動

進入：

    DB/api

第一次建立環境：

    python -m venv venv
    .\venv\Scripts\python.exe -m pip install -r requirements.txt

使用資料庫功能前，需先啟動 PostgreSQL，並於本機設定 `.env` 資料庫連線資訊。

請勿將真實帳號、密碼或其他敏感設定提交至 Git。

---

## 啟動 FastAPI

執行：

    .\run.bat

FastAPI 會使用：

    0.0.0.0:7777

啟動後可開啟：

    http://127.0.0.1:7777/

Web App：

    /

API：

    /api/...

Swagger UI：

    /api/docs

---

## 目前 API

目前已建立或開始實作：

    GET    /api/health
    GET    /api/version
    POST   /api/items

    GET    /api/note/{note_id}

    GET    /api/notes
    POST   /api/notes
    PUT    /api/notes/{note_id}
    DELETE /api/notes/{note_id}

CRUD API 尚在 W04 驗證階段。

---

## 版本管理

以下內容不納入 Git：

    .env
    venv/
    __pycache__/

Commit 前先執行：

    git status

確認沒有將敏感資料或不必要檔案加入 Git。

---

## 課程紀錄

詳細每週內容、操作步驟、驗收結果與學習筆記請參考：

    psql.md