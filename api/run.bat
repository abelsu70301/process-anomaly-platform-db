@echo off
::不要把每條批次指令都印在畫面上
::call venv\Scripts\activate
:: 啟用這個專案的 Python 虛擬環境
"%~dp0venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload
:: 使用本專案 venv 的 Python 啟動 FastAPI
::不只接受自己電腦 localhost 的連線，也允許透過這台電腦的 local IP 進來
::使用老師指定的 7777 port
::修改 Python 程式後自動重新載入
::%~dp0 代表這個run.bat所在的資料夾
