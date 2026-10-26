# AI 使用與學習紀錄

## Week 1：FastAPI 開發環境與 Git 基礎

### 1. 本週學習內容
- 建立 Python 虛擬環境（venv）
- 安裝 FastAPI 與 Uvicorn
- 建立 FastAPI 基礎 API
- 使用 Pydantic 進行資料驗證
- 測試 GET 與 POST API
- 建立 requirements.txt 與 .gitignore
- 安裝 Git 並建立 Git repository

### 2. AI 協助與問題處理

#### 問題 1：PowerShell 無法啟動虛擬環境
- 問題：執行 `.\venv\Scripts\Activate.ps1` 時，因 PowerShell 的 Execution Policy 而無法執行。
- AI 建議：使用 `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`，只針對目前的 PowerShell 工作階段暫時允許執行腳本。
- 驗證：重新執行 `Activate.ps1` 後，Terminal 出現 `(venv)`，確認虛擬環境成功啟動。
- 我的理解：`-Scope Process` 只影響目前的 PowerShell 工作階段，關閉 Terminal 後設定即失效，不是永久修改整台電腦的執行原則。

#### 問題 2：移動專案後虛擬環境路徑異常
- 問題：專案資料夾路徑變更後，原本的 venv 執行 pip 時出現路徑錯誤。
- AI 建議：刪除原本的 venv，在目前專案位置重新建立虛擬環境並重新安裝套件。
- 驗證：使用 `python -m pip show fastapi` 確認 FastAPI 的安裝位置位於目前專案的 venv 中。
- 我的理解：venv 內可能記錄建立時的路徑，因此專案移動或更名後，直接沿用舊的 venv 可能發生問題；requirements.txt 則可以用來協助重新建立套件環境。

#### 問題 3：Uvicorn 啟動指令格式錯誤
- 問題：第一次啟動 FastAPI 時，將指令寫成 `uvicorn app.main.app --reload`，出現 Import string 格式錯誤。
- AI 協助：確認 Uvicorn 的啟動格式應為 `<module>:<attribute>`。
- 修正：改為 `uvicorn app.main:app --reload`。
- 驗證：瀏覽器開啟 `/health` 後成功取得 `{"status":"ok"}`，並可正常開啟 `/docs`。
- 我的理解：`app.main` 代表 Python module `app/main.py`，冒號後的 `app` 則代表 `main.py` 中由 `FastAPI()` 建立的應用程式物件。

#### 問題 4：測試 API 與資料驗證
- 實作：建立 `GET /health`、`GET /version` 與 `POST /items`。
- AI 協助：理解 GET、POST、Request、Response、HTTP Status Code，以及 Pydantic `BaseModel` 的用途。
- 驗證：使用 FastAPI `/docs` 實際執行 API；正常資料可成功取得回應，錯誤輸入則可觀察到 422 回應。
- 我的理解：FastAPI 可透過 Pydantic 定義輸入資料格式，在資料進入函式前先進行驗證；`/docs` 則可用來實際送出 Request 並觀察 Response。

---

## Week 2：PostgreSQL 與 SQLAlchemy 實作

### 1. 本週學習內容
- 建立 PostgreSQL 與 pgAdmin 開發環境
- 建立 `notes` 資料表
- 使用 SQL `INSERT` 與 `SELECT`
- 建立 Python 與 PostgreSQL 連線
- 建立 SQLAlchemy ORM Model
- 使用 Alembic 管理資料表變更
- 建立單筆 Note 查詢 API
- 使用 Swagger 驗證 API 與資料庫串接

### 2. AI 協助與問題處理

#### 問題 1：`is_archived` 在直接 INSERT 時需要另外指定值
- 問題：`Note` Model 中已設定 `default=False`，但直接使用 PostgreSQL INSERT 時，`is_archived` 仍不能省略。
- AI 協助：一起檢查 ORM 設定與實際 PostgreSQL table schema，確認 Python 端的 `default=False` 不等於資料庫端具有預設值。
- 驗證：使用 PostgreSQL 查看 `notes` table 結構，並在 INSERT 時明確加入 `is_archived = false` 後成功新增資料。
- 我的理解：ORM 中設定的預設值不一定等於 Database Server 本身的預設值，遇到這類問題要查看實際 table schema，而不是只看 Python Model。

#### 問題 2：確認 W2 測試資料是否真的寫入資料庫
- 問題：需要確認課程要求的測試資料是否真的已經存在 PostgreSQL 中。
- AI 協助：使用 SQL 查詢方式逐步確認資料內容。
- 驗證：成功建立三筆測試資料，並使用：

    SELECT * FROM notes;

  查詢到三筆資料。
- 我的理解：程式沒有報錯不代表資料一定已經寫入，還是要直接查 Database 確認。

#### 問題 3：確認 FastAPI 是否真的讀到 PostgreSQL 資料
- 問題：SQL 查詢成功後，還需要確認 FastAPI API 是否真的能從 PostgreSQL 取得相同資料。
- AI 協助：一起檢查單筆查詢 API，並使用 Swagger 測試。
- 驗證：執行：

    GET /api/note/2

  成功取得 `200 OK` 與資料庫中的 Note 資料。
- 我的理解：SQL 查詢成功與 API 查詢成功是兩個不同階段，要分開驗證。

#### 問題 4：Alembic Migration 與目前資料表狀態需要一起確認
- 問題：專案中已有建立 `notes`、`users` 與新增 `is_archived` 的 Migration，但需要確認哪些是目前實際資料庫已套用的內容。
- AI 協助：協助閱讀 Migration 檔與資料表結果，不直接把「有 Migration 檔」視為「資料庫一定已完成更新」。
- 驗證：實際查看 PostgreSQL table structure 與目前 Alembic 紀錄。
- 我的理解：Migration 檔存在、Migration 已執行、Database Schema 已更新，是三件要分開確認的事情。

---

## Week 3：FastAPI 同時服務 Web App 與 API

### 1. 本週學習內容
- 建立 `run.bat`
- 使用專案虛擬環境啟動 FastAPI
- 使用 `0.0.0.0:7777`
- 將 API 整理到 `/api/`
- 將 `WEB/site` 設為 Web Public Directory
- 使用 `StaticFiles` 提供 Web App
- 驗證 Web App 與 API 可同時運作

### 2. AI 協助與問題處理

#### 問題 1：`run.bat` 執行時遇到 Python／Uvicorn 路徑問題
- 問題：原本啟動方式可能使用到錯誤的 Python 或失效的 Uvicorn Launcher。
- AI 協助：一起確認目前 venv 中的 Python 與 Uvicorn 狀態，最後改成直接使用專案 venv 的 Python 執行 Uvicorn。
- 修正：

    "%~dp0venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload

- 驗證：使用 `run.bat` 後 FastAPI 可正常啟動。
- 我的理解：直接指定目前專案 venv 的 Python，可以避免誤用其他 Python 環境或失效的 Uvicorn 執行檔。

#### 問題 2：StaticFiles 設定後首頁仍顯示原本 Hello World
- 問題：已加入 StaticFiles，但開啟 `/` 時仍看到原本的 Hello World 頁面。
- AI 協助：一起檢查 `main.py`，發現原本仍有 `@app.get("/")` Route。
- 修正：移除原本首頁 Route，改由 StaticFiles 掛載：

    app.mount(
        "/",
        StaticFiles(directory=PUBLIC_DIRECTORY, html=True),
        name="web"
    )

- 驗證：重新開啟 `/` 後成功顯示 `WEB/site/index.html`。
- 我的理解：如果相同路徑已經有 FastAPI Route，需要先確認 Route 與 StaticFiles 是否互相衝突。

#### 問題 3：FastAPI 需要正確找到 `WEB/site`
- 問題：DB 與 WEB 分開後，`main.py` 需要正確找到另一個資料夾中的前端檔案。
- AI 協助：一起確認目前專案目錄階層，改用 `Path(__file__).resolve()` 從目前程式位置計算 `WEB/site` 路徑。
- 修正：

    PUBLIC_DIRECTORY = (
        Path(__file__).resolve().parents[3]
        / "WEB"
        / "site"
    )

- 驗證：
  - `/` 可正常顯示 Web App。
  - `/api/health` 可正常回傳 API。
  - Local IP 與公開 HTTPS Demo 皆可正常存取。
- 我的理解：使用專案目錄結構計算路徑，比直接寫死完整 Windows Path 更適合專案移動，也確認目前 FastAPI 已能同時提供 Web App 與 API。

---

## AI 使用反思

目前 AI 主要用在：

- 協助分析實際 Error Message
- 一起檢查程式與資料夾結構
- 將問題拆成可以逐步測試的小步驟
- 協助比較老師教材要求與目前專案實際情況
- 協助整理實作紀錄

目前的使用方式是：

    遇到問題
    ↓
    與 AI 討論可能原因
    ↓
    一次修改一個部分
    ↓
    實際執行
    ↓
    確認結果
    ↓
    再決定是否保留

AI 提供的建議不直接視為正確答案，仍需透過實際程式、Database、Swagger、Browser 或 Terminal 驗證。

另外不將 `.env`、密碼、Token、Secret Key 或其他敏感資料提供給 AI。
---

## W04：CRUD API 完整實作 {#CRUD}

### 1. `notes.py` 建立在錯誤目錄

#### 問題

建立 Note Router 時，不小心多建立了一層 `api` 資料夾，導致檔案位置變成：

```text
DB/api/api/app/api/notes.py
```

正確位置應為：

```text
DB/api/app/api/notes.py
```

#### AI 協助

使用 PowerShell 將檔案移到正確位置：

```powershell
Move-Item .\api\app\api\notes.py .\app\api\notes.py
```

再刪除多餘的資料夾：

```powershell
Remove-Item -Recurse .\api
```

#### 結果

`notes.py` 回到正確位置：

```text
app/api/notes.py
```

FastAPI 可以正常匯入 `notes` Router。

---

### 2. FastAPI 啟動出現 `NameError`

#### 問題

整理 `main.py` 的 import 時，不小心刪除了：

```python
from fastapi import FastAPI
```

重新執行：

```powershell
.\run.bat
```

後出現：

```text
NameError: name 'FastAPI' is not defined
```

錯誤位置：

```python
app = FastAPI(...)
```

#### AI 協助

重新檢查 `main.py` 的 import，補回：

```python
from fastapi import FastAPI
```

#### 結果

重新啟動 FastAPI 後可以正常執行。

---

### 3. 原有 CRUD 與新的 Router 架構重複

#### 問題

原本部分 Note CRUD 直接寫在：

```text
app/main.py
```

W04 開始改成獨立 Router：

```text
app/api/notes.py
```

因此舊程式與新 Router 架構會重複。

#### AI 協助

將 Note CRUD 集中到：

```text
app/api/notes.py
```

將 API 輸入與輸出格式移到：

```text
app/schemas/note.py
```

`main.py` 只負責註冊 Router：

```python
from app.api import notes

app.include_router(notes.router, prefix="/api")
```

#### 結果

程式結構改為：

```text
app/
├─ api/
│  └─ notes.py
├─ models/
│  └─ note.py
├─ schemas/
│  └─ note.py
└─ main.py
```

Model、Schema 與 Router 分開管理。

---

### 4. `/api` 與 Router Prefix 的組合

#### 問題

W03 已將 API 統一放在：

```text
/api/
```

W04 的 Note Router 則設定：

```python
prefix="/notes"
```

不確定兩者應如何組合。

#### AI 協助

在 `notes.py`：

```python
router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)
```

在 `main.py`：

```python
app.include_router(notes.router, prefix="/api")
```

因此實際 API Path 為：

```text
/api/notes/
```

#### 結果

Note Router 可以在原本 W03 的 `/api` 架構下正常使用。

---

### 5. User CRUD 延伸實作

#### 問題

完成 Note CRUD 後，需要將相同架構套用到既有的 `User` Model。

先確認：

```text
app/models/user.py
```

目前 User 欄位為：

```text
id
email
hashed_password
created_at
```

#### AI 協助

依現有 User Model 建立：

```text
app/schemas/user.py
app/api/users.py
```

並在 `main.py` 中加入：

```python
from app.api import notes, users
```

以及：

```python
app.include_router(notes.router, prefix="/api")
app.include_router(users.router, prefix="/api")
```

#### 結果

Note 與 User 都使用相同的 Router / Schema / Model 分層方式。

---

### 本週 AI 協助摘要

本週主要使用 AI 協助：

1. 修正 `notes.py` 建立在錯誤目錄的問題。
2. 排查 `FastAPI` import 遺失造成的 `NameError`。
3. 將原本寫在 `main.py` 的 CRUD 拆分成 Router、Schema 與 Model。
4. 確認 `/api` 與 Router prefix 的組合方式。
5. 依既有 `User` Model 延伸建立 User CRUD 架構。

---

---

## W05：關聯式設計與 View

### 1. `academic.sql` 語法與編碼問題

#### 問題

建立 `academic.sql` 時，曾遇到數個 SQL 語法與編碼問題，包括：

- PRIMARY KEY 後缺少逗號
- 最後一個 UNIQUE constraint 後多逗號
- Function 參數列最後多逗號
- `RETURING` 拼字錯誤
- PowerShell `Get-Content` 顯示中文時出現亂碼

另外，加入：

\encoding UTF8

後，因為同一行後面接了註解，`psql` 執行時出現額外參數警告。

#### AI 協助

逐段檢查 SQL 語法，並將：

\encoding UTF8

改成獨立一行，不與註解寫在同一行。

#### 結果

`academic.sql` 可以正常執行，資料庫中的中文內容也能正常顯示。

---

### 2. PostgreSQL `psql.exe` 路徑版本不符

#### 問題

原本執行 PostgreSQL 指令時，使用了錯誤版本的 `psql.exe` 路徑，因此 PowerShell 找不到執行檔。

#### AI 協助

重新確認本機 PostgreSQL 的實際版本與安裝位置。

最後確認目前使用：

C:\Program Files\PostgreSQL\16\bin\psql.exe

#### 結果

改用 PostgreSQL 16 的 `psql.exe` 後，可以正常執行 `academic.sql`。

---

### 3. `vd_subclass` API 出現 `500 Internal Server Error`

#### 問題

建立：

GET /api/subclass/pcid/{id}

後，Swagger 回傳：

500 Internal Server Error

先補上 View 的 `SELECT` 權限後，仍然出現 500。

#### AI 協助

查看 Uvicorn traceback，發現程式中寫成：

rows = result.mapping().all()

錯誤訊息指出：

CursorResult object has no attribute 'mapping'

正確寫法應為：

rows = result.mappings().all()

#### 結果

修改成 `mappings()` 後，Swagger 可以正常回傳 `vd_subclass` 資料。

---

### 4. View 權限不足

#### 問題

FastAPI 使用的 `dev_user` 原本沒有新建立 View 的讀取權限，因此 API 無法正常查詢 View。

#### AI 協助

補上：

GRANT SELECT ON vd_subclass TO dev_user;
GRANT SELECT ON vd_objectlist TO dev_user;
GRANT SELECT ON vd_object TO dev_user;

#### 結果

FastAPI 可以正常讀取三個 View。

---

### 本週 AI 協助摘要

本週主要使用 AI 協助：

1. 修正 `academic.sql` 的 SQL 語法與 UTF-8 編碼問題。
2. 確認 PostgreSQL 16 的正確 `psql.exe` 路徑。
3. 透過 Uvicorn traceback 修正 `mapping()` 與 `mappings()` 錯誤。
4. 補上 `dev_user` 對 View 的 `SELECT` 權限。