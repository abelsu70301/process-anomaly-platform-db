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