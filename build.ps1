$ErrorActionPreference = "Stop"
python -m PyInstaller --clean --noconfirm --onefile --name cnblog_uploader cnblog_uploader.py
Copy-Item -Force dist\cnblog_uploader.exe .\cnblog_uploader.exe
Write-Host "Built cnblog_uploader.exe. Keep it next to config.json."
