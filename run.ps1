# Voice AI Launcher
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "        Voice AI - Whisper STT & Kokoro TTS" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting FastAPI application with Uvicorn..." -ForegroundColor Green
Write-Host "Access the web interface at: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host ""

Start-Process "http://127.0.0.1:8000"
python app.py
