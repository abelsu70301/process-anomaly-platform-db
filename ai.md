# AI 使用與問題排查紀錄

本文件記錄資料庫系統課程與專案開發過程中，實際使用 AI 協助修改程式、分析錯誤與排查問題的紀錄。

AI 提供的建議不直接視為正確答案，所有修改仍會透過 Terminal、PostgreSQL、Swagger、Browser 或實際程式執行結果進行驗證。

`.env`、密碼、Token、Secret Key 與其他敏感資料不提供給 AI，也不納入 Git。

---

## W01：FastAPI 開發環境與 Git

### 1. PowerShell 無法啟動虛擬環境

#### 問題

執行：

```powershell
.\venv\Scripts\Activate.ps1
```

時，因 PowerShell Execution Policy 無法執行腳本。

#### AI 協助

使用：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

只針對目前 PowerShell 工作階段暫時允許執行腳本。

#### 結果

重新執行 `Activate.ps1` 後 Terminal 出現：

```text
(venv)
```

確認虛擬環境成功啟動。

---

### 2. 移動專案後 venv 路徑異常

#### 問題

專案資料夾移動後，原本 venv 執行 pip 時出現路徑錯誤。

#### AI 協助

刪除舊 venv，在目前專案位置重新建立：

```powershell
python -m venv venv
```

再重新安裝套件。

#### 結果

使用：

```powershell
python -m pip show fastapi
```

確認 FastAPI 安裝於目前專案的 venv。

---

### 3. Uvicorn 啟動指令格式錯誤

#### 問題

第一次啟動 FastAPI 時使用：

```text
uvicorn app.main.app --reload
```

出現 Import String 格式錯誤。

#### AI 協助

確認 Uvicorn 啟動格式應為：

```text
<module>:<attribute>
```

修正為：

```powershell
uvicorn app.main:app --reload
```

#### 結果

FastAPI 可正常啟動，並成功開啟 API 文件。

---

### 4. API 與資料驗證測試

建立：

```text
GET /health
GET /version
POST /items
```

使用 Swagger UI 實際測試 Request / Response。

正常資料可取得成功回應，錯誤輸入可觀察到 FastAPI / Pydantic 的資料驗證錯誤。

---

## W02：PostgreSQL 與 SQLAlchemy

### 1. `is_archived` 在直接 INSERT 時沒有預設值

#### 問題

`Note` ORM Model 已設定：

```python
default=False
```

但直接使用 PostgreSQL INSERT 時仍需要指定 `is_archived`。

#### AI 協助

檢查 ORM Model 與 PostgreSQL 實際 Table Schema，確認：

```text
Python / SQLAlchemy default
≠
PostgreSQL server_default
```

#### 結果

在 SQL INSERT 中明確加入：

```text
is_archived = false
```

後成功新增資料。

---

### 2. 確認測試資料是否真的寫入 PostgreSQL

#### 問題

程式沒有報錯，但仍需要確認資料是否真的存在 Database。

#### AI 協助

直接使用：

```sql
SELECT * FROM notes;
```

檢查實際資料。

#### 結果

成功查詢到三筆 W02 測試資料。

---

### 3. 確認 FastAPI 是否真的讀取 PostgreSQL

#### 問題

SQL 查詢成功後，還需要確認 API 是否真的透過 PostgreSQL 取得資料。

#### AI 協助

使用 Swagger 測試：

```text
GET /api/note/2
```

#### 結果

成功回傳：

```text
200 OK
```

並取得 PostgreSQL 中的 Note 資料。

---

### 4. Alembic Migration 與 Database 狀態確認

#### 問題

專案中已有 Migration File，但需要確認 Database 是否真的套用相同結構。

#### AI 協助

分別確認：

```text
Migration File 是否存在
Migration 是否執行
Database Schema 是否更新
```

#### 結果

透過 PostgreSQL Table Structure 與 Alembic 紀錄確認目前資料庫狀態。

---

## W03：FastAPI 同時提供 Web App 與 API

### 1. `run.bat` Python / Uvicorn 路徑問題

#### 問題

原本啟動方式可能使用到錯誤 Python 或失效的 Uvicorn Launcher。

#### AI 協助

改為直接指定專案 venv Python：

```bat
"%~dp0venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload
```

#### 結果

使用：

```powershell
.\run.bat
```

可以正常啟動 FastAPI。

---

### 2. StaticFiles 設定後首頁仍顯示 Hello World

#### 問題

加入 StaticFiles 後，開啟 `/` 仍顯示原本的 FastAPI Hello World。

#### AI 協助

檢查 `main.py` 後發現原本仍存在：

```python
@app.get("/")
```

首頁 Route。

移除後改由：

```python
app.mount(
    "/",
    StaticFiles(directory=PUBLIC_DIRECTORY, html=True),
    name="web"
)
```

提供 Web App。

#### 結果

重新開啟 `/` 後成功顯示：

```text
WEB/site/index.html
```

---

### 3. FastAPI 找不到 `WEB/site`

#### 問題

DB 與 WEB 專案分開後，FastAPI 必須正確找到另一個資料夾中的前端檔案。

#### AI 協助

改用：

```python
Path(__file__).resolve()
```

依目前程式所在位置計算路徑：

```python
PUBLIC_DIRECTORY = (
    Path(__file__).resolve().parents[3]
    / "WEB"
    / "site"
)
```

#### 結果

以下功能皆可正常使用：

```text
/
→ Web App

/api/health
→ Backend API
```

---

## W04：CRUD API

### 1. `notes.py` 建立在錯誤目錄

#### 問題

建立 Note Router 時不小心多建立一層 `api`，檔案位置變成：

```text
DB/api/api/app/api/notes.py
```

正確位置應為：

```text
DB/api/app/api/notes.py
```

#### AI 協助

使用 PowerShell 將檔案移回正確位置，並刪除多餘資料夾。

#### 結果

`notes.py` 回到：

```text
app/api/notes.py
```

FastAPI 可以正常 Import Router。

---

### 2. FastAPI 啟動出現 `NameError`

#### 問題

整理 `main.py` 時不小心移除：

```python
from fastapi import FastAPI
```

執行後出現：

```text
NameError: name 'FastAPI' is not defined
```

#### AI 協助

重新檢查 Import 並補回：

```python
from fastapi import FastAPI
```

#### 結果

FastAPI 恢復正常啟動。

---

### 3. 舊 CRUD 與新 Router 架構重複

#### 問題

部分 Note CRUD 原本直接寫在：

```text
app/main.py
```

W04 又建立：

```text
app/api/notes.py
```

造成程式功能重複。

#### AI 協助

將功能重新整理為：

```text
Router
→ app/api/notes.py

Schema
→ app/schemas/note.py

Model
→ app/models/note.py

main.py
→ 註冊 Router
```

#### 結果

Model、Schema 與 Router 分開管理。

---

### 4. `/api` 與 Router Prefix 組合

#### 問題

`main.py` 使用：

```python
app.include_router(notes.router, prefix="/api")
```

而 Note Router 使用：

```python
prefix="/notes"
```

需要確認實際 URL。

#### 結果

兩層 Prefix 組合後：

```text
/api
+
/notes

→ /api/notes/
```

---

### 5. User CRUD 延伸

完成 Note CRUD 後，使用相同結構建立：

```text
app/schemas/user.py
app/api/users.py
```

並在 `main.py` 註冊 User Router。

#### 結果

Note 與 User 都使用：

```text
Router
Schema
Model
```

分層方式完成 CRUD。

---

## W05：關聯式設計與 View

### 1. `academic.sql` SQL 語法與編碼問題

#### 問題

建立 `academic.sql` 時曾遇到：

- PRIMARY KEY 後缺少逗號
- Constraint 後多逗號
- Function 參數列最後多逗號
- `RETURING` 拼字錯誤
- PowerShell 顯示中文亂碼

加入：

```sql
\encoding UTF8
```

時，也曾因同一行後方接註解造成 `psql` 警告。

#### AI 協助

逐段檢查 SQL，並將：

```sql
\encoding UTF8
```

改成獨立一行。

#### 結果

`academic.sql` 可以正常執行。

---

### 2. PostgreSQL `psql.exe` 路徑錯誤

#### 問題

原本使用錯誤版本的 PostgreSQL 路徑，因此 PowerShell 找不到 `psql.exe`。

#### AI 協助

確認本機 PostgreSQL 實際版本。

目前使用：

```text
C:\Program Files\PostgreSQL\16\bin\psql.exe
```

#### 結果

可以正常使用 `psql` 執行 SQL File。

---

### 3. `vd_subclass` API 出現 `500 Internal Server Error`

#### 問題

建立：

```text
GET /api/subclass/pcid/{id}
```

後 Swagger 回傳：

```text
500 Internal Server Error
```

查看 Uvicorn Traceback 發現：

```python
result.mapping().all()
```

寫錯。

#### AI 協助

修正為：

```python
result.mappings().all()
```

#### 結果

Swagger 可以正常取得 `vd_subclass` 資料。

---

### 4. View 權限不足

#### 問題

FastAPI 使用 `dev_user` 連線，但新建立的 View 沒有 SELECT 權限。

#### AI 協助

加入：

```sql
GRANT SELECT ON vd_subclass TO dev_user;
GRANT SELECT ON vd_objectlist TO dev_user;
GRANT SELECT ON vd_object TO dev_user;
```

#### 結果

FastAPI 可正常讀取三個 View。

---

## W06：Authentication / JWT

### 1. `member` Table 權限不足

#### 問題

建立 Member 功能後，第一次透過 FastAPI 使用的 `dev_user` 寫入 `member` Table 時，PostgreSQL 回傳權限不足：

```text
psycopg.errors.InsufficientPrivilege:
permission denied for table member
```

原因是新建立的 `member` Table 尚未授權給 FastAPI 使用的 `dev_user`。

另外，`mid` 使用 Identity 自動產生，因此新增資料時也需要對對應 Sequence 具有使用權限。

#### AI 協助

依照目前登入流程實際需要的操作，補上最小必要權限：

```sql
GRANT SELECT, INSERT, UPDATE
ON TABLE member
TO dev_user;

GRANT USAGE, SELECT
ON SEQUENCE member_mid_seq
TO dev_user;
```

目前登入流程不需要刪除 Member，因此沒有額外提供 `DELETE` 權限。

#### 結果

重新執行 Member 測試後可以正常新增資料。

再次使用相同 `google_sub` 測試時，也可以正常更新既有 Member，不再出現資料庫權限錯誤。

### W06 AI 協助摘要

本週實際需要 AI 協助排查的問題主要為：

1. `dev_user` 沒有新建立 `member` Table 的操作權限。
2. 補上 `member` Table 的 `SELECT / INSERT / UPDATE` 權限。
3. 補上 Identity Sequence 的 `USAGE / SELECT` 權限。
4. 依最小授權原則，不提供目前功能不需要的 `DELETE` 權限。

---

## W07：EER Model / AI Gen Data

### 1. `process_vdata.sql` 誤加入 SECOM 測試資料

#### 問題

建立 W07 測試資料時，`process_vdata.sql` 中仍殘留先前 SECOM 情境的內容。

執行後資料庫中意外新增：

```text
SECOM Dataset
SECOM Failure Predictor
```

並產生額外的 Object：

```text
oid = 4
oid = 5
```

但目前專案已決定使用 AI4I 2020 作為主要測試資料情境。

#### AI 協助

先查詢：

```text
object
dataset
model
analysis_run
```

確認多出的 SECOM Dataset / Model 是否已被其他資料引用。

確認未被 AnalysisRun 使用後，依 Foreign Key 關係先刪除子類資料，再刪除父類 Object：

```sql
DELETE FROM model
WHERE oid = 5;

DELETE FROM dataset
WHERE oid = 4;

DELETE FROM object
WHERE oid IN (4, 5);
```

#### 結果

資料重新整理為：

```text
Object 1
→ Dataset
→ AI4I 2020

Object 2
→ Model
→ AI4I Failure Predictor

Object 3
→ AnalysisRun
```

後續 W07 測試資料統一使用 AI4I 2020。

---

### 2. `process_vdata.sql` 重複執行可能重複新增資料

#### 問題

原本測試資料腳本直接使用 `INSERT`。

若重複執行：

```text
process_vdata.sql
```

可能再次新增相同的：

```text
Dataset
Model
AnalysisRun
```

造成測試資料重複。

#### AI 協助

將測試資料新增邏輯改為先確認資料是否已存在：

```sql
WHERE NOT EXISTS (...)
```

只有找不到相同資料時才建立新的 Object 與子類資料。

#### 驗證

再次執行：

```powershell
& 'C:\Program Files\PostgreSQL\16\bin\psql.exe' `
  -U postgres `
  -d fastapi_dev `
  -f .\psql\process_vdata.sql
```

結果：

```text
SET
INSERT 0 0
INSERT 0 0
INSERT 0 0
```

#### 結果

確認重複執行 SQL File 時，不會再次新增相同的 AI4I Dataset、Model 與 AnalysisRun。

---

### 3. `process_vdata.sql` 出現 BIG5 / UTF-8 編碼錯誤

#### 問題

執行：

```text
psql/process_vdata.sql
```

時出現：

```text
ERROR: character with byte sequence ...
in encoding "BIG5"
has no equivalent in encoding "UTF8"
```

代表目前 `psql` Client Encoding 與 SQL File / Database 使用的 UTF-8 不一致。

#### AI 協助

在 `process_vdata.sql` 第一行加入：

```sql
\encoding UTF8
```

並保持為獨立一行。

#### 驗證

重新執行後：

```text
SET
INSERT 0 0
INSERT 0 0
INSERT 0 0
```

#### 結果

SQL File 可以正常執行，BIG5 / UTF-8 Encoding Error 已排除。

---

### 4. 多建立一個空的 `api/process_vdata.sql`

#### 問題

Commit 前執行：

```powershell
git status
```

發現同時存在：

```text
api/process_vdata.sql
psql/process_vdata.sql
```

其中正確的 W07 SQL File 應位於：

```text
psql/process_vdata.sql
```

#### AI 協助

檢查多出的檔案：

```powershell
Get-Item .\api\process_vdata.sql
Get-Content .\api\process_vdata.sql
```

確認：

```text
Length = 0
```

是一個誤建立的空檔案。

因此刪除：

```powershell
Remove-Item .\api\process_vdata.sql
```

#### 結果

專案只保留正確的：

```text
psql/process_vdata.sql
```

避免將無用途的空檔案一起 Commit。

---

### W07 AI 協助摘要

本週實際需要 AI 協助排查的問題主要為：

1. `process_vdata.sql` 誤加入 SECOM 測試資料。
2. 清除錯誤測試資料時確認 Foreign Key 與父子資料刪除順序。
3. 修正測試資料重複執行可能重複 INSERT 的問題。
4. 排除 `BIG5` 與 `UTF8` Client Encoding 錯誤。
5. Commit 前發現並刪除誤建立的空白 `api/process_vdata.sql`。