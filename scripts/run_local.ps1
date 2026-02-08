# Evolution of Todo - Local Development Startup Script (PowerShell)
# Run this script to start all services for hackathon demo

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Evolution of Todo - Hackathon Local Development" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$rootDir = Split-Path -Parent $PSScriptRoot

Write-Host "Choose which phase to run:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Phase I  - CLI only (no server needed)"
Write-Host "  2. Phase II - Web App (Backend + Frontend)"
Write-Host "  3. Phase III - Chatbot (Chatbot Backend + Simple UI)"
Write-Host "  4. Phase III - Chatbot (Chatbot Backend + Next.js UI)"
Write-Host "  5. All Services (Phase II + III together)"
Write-Host "  6. Phase V - Event-Driven (requires Docker)"
Write-Host ""
$choice = Read-Host "Enter choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Phase I - CLI Todo App" -ForegroundColor Green
        Write-Host "-----------------------"
        Write-Host ""
        Write-Host "Usage examples:"
        Write-Host "  cd phase1_cli"
        Write-Host "  python -m src.main add --title 'My task'"
        Write-Host "  python -m src.main list"
        Write-Host "  python -m src.main complete --id 1"
        Write-Host "  python -m src.main delete --id 1"
        Write-Host ""
        Set-Location "$rootDir\phase1_cli"
    }
    "2" {
        Write-Host ""
        Write-Host "Starting Phase II - Web App..." -ForegroundColor Green
        Write-Host ""

        Write-Host "Starting Todo API Backend on http://localhost:8000..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\backend'; pip install -r requirements.txt; uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

        Start-Sleep -Seconds 3

        Write-Host "Starting Todo Frontend on http://localhost:3000..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\frontend'; npm install; npm run dev"

        Write-Host ""
        Write-Host "Services:" -ForegroundColor Cyan
        Write-Host "  - Frontend: http://localhost:3000"
        Write-Host "  - Backend:  http://localhost:8000"
    }
    "3" {
        Write-Host ""
        Write-Host "Starting Phase III - Chatbot (Simple UI)..." -ForegroundColor Green
        Write-Host ""

        Write-Host "Starting Chatbot Backend on http://localhost:8000..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\chatbot_backend'; pip install -r requirements.txt; uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

        Start-Sleep -Seconds 3

        Write-Host "Starting Chatbot Frontend on http://localhost:8001..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir'; python -m http.server 8001 -d chatbot_frontend"

        Write-Host ""
        Write-Host "Services:" -ForegroundColor Cyan
        Write-Host "  - Chatbot UI:  http://localhost:8001"
        Write-Host "  - Chatbot API: http://localhost:8000"
    }
    "4" {
        Write-Host ""
        Write-Host "Starting Phase III - Chatbot (Next.js UI)..." -ForegroundColor Green
        Write-Host ""

        Write-Host "Starting Chatbot Backend on http://localhost:8000..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\chatbot_backend'; pip install -r requirements.txt; uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

        Start-Sleep -Seconds 3

        Write-Host "Starting Chatbot Frontend (Next.js) on http://localhost:3001..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\chatbot_frontend_nextjs'; npm install; npm run dev -- -p 3001"

        Write-Host ""
        Write-Host "Services:" -ForegroundColor Cyan
        Write-Host "  - Chatbot UI:  http://localhost:3001"
        Write-Host "  - Chatbot API: http://localhost:8000"
    }
    "5" {
        Write-Host ""
        Write-Host "Starting ALL Services (Phase II + III)..." -ForegroundColor Green
        Write-Host ""

        Write-Host "Starting Todo API Backend on http://localhost:8000..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\backend'; pip install -r requirements.txt; uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

        Write-Host "Starting Chatbot Backend on http://localhost:8001..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\chatbot_backend'; pip install -r requirements.txt; uvicorn main:app --host 0.0.0.0 --port 8001 --reload"

        Start-Sleep -Seconds 3

        Write-Host "Starting Todo Frontend on http://localhost:3000..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\frontend'; npm install; npm run dev"

        Write-Host "Starting Chatbot Frontend on http://localhost:3001..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\chatbot_frontend_nextjs'; npm install; npm run dev -- -p 3001"

        Write-Host ""
        Write-Host "Services:" -ForegroundColor Cyan
        Write-Host "  - Todo Frontend:    http://localhost:3000"
        Write-Host "  - Todo Backend:     http://localhost:8000"
        Write-Host "  - Chatbot Frontend: http://localhost:3001"
        Write-Host "  - Chatbot Backend:  http://localhost:8001"
    }
    "6" {
        Write-Host ""
        Write-Host "Starting Phase V - Event-Driven (Kafka)..." -ForegroundColor Green
        Write-Host ""

        Write-Host "Starting Kafka via Docker Compose..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir'; docker-compose up"

        Start-Sleep -Seconds 10

        Write-Host "Starting Reminders Service..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\reminders_service'; pip install -r requirements.txt; python main.py"

        Write-Host ""
        Write-Host "Services:" -ForegroundColor Cyan
        Write-Host "  - Kafka: localhost:9093"
        Write-Host "  - Kafka UI: http://localhost:8080"
        Write-Host "  - Reminders Service: Running"
    }
    default {
        Write-Host "Invalid choice. Exiting." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Close the opened windows to stop services." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
