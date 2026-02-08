@echo off
REM Evolution of Todo - Local Development Startup Script (Batch)
REM Run this script to start all services for hackathon demo

echo.
echo ============================================================
echo   Evolution of Todo - Hackathon Local Development
echo ============================================================
echo.

REM Navigate to project root
cd /d "%~dp0\.."

echo Choose which phase to run:
echo.
echo   1. Phase I  - CLI only (no server needed)
echo   2. Phase II - Web App (Backend + Frontend)
echo   3. Phase III - Chatbot (Chatbot Backend + Simple UI)
echo   4. Phase III - Chatbot (Chatbot Backend + Next.js UI)
echo   5. All Services (Phase II + III together)
echo   6. Phase V - Event-Driven (requires Docker)
echo.
set /p choice="Enter choice (1-6): "

if "%choice%"=="1" goto phase1
if "%choice%"=="2" goto phase2
if "%choice%"=="3" goto phase3
if "%choice%"=="4" goto phase3nextjs
if "%choice%"=="5" goto all
if "%choice%"=="6" goto phase5
goto end

:phase1
echo.
echo Phase I - CLI Todo App
echo -----------------------
echo.
echo Usage examples:
echo   cd phase1_cli
echo   python -m src.main add --title "My task"
echo   python -m src.main list
echo   python -m src.main complete --id 1
echo   python -m src.main delete --id 1
echo.
start "Phase 1 CLI" cmd /k "cd phase1_cli && echo Ready! Try: python -m src.main list"
goto end

:phase2
echo.
echo Starting Phase II - Web App...
echo.
echo Starting Todo API Backend on http://localhost:8000...
start "Todo Backend (8000)" cmd /k "cd backend && pip install -r requirements.txt 2>nul && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo Starting Todo Frontend on http://localhost:3000...
start "Todo Frontend (3000)" cmd /k "cd frontend && npm install 2>nul && npm run dev"
echo.
echo Services:
echo   - Frontend: http://localhost:3000
echo   - Backend:  http://localhost:8000
goto end

:phase3
echo.
echo Starting Phase III - Chatbot (Simple UI)...
echo.
echo Starting Chatbot Backend on http://localhost:8000...
start "Chatbot Backend (8000)" cmd /k "cd chatbot_backend && pip install -r requirements.txt 2>nul && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo Starting Chatbot Frontend on http://localhost:8001...
start "Chatbot Frontend (8001)" cmd /k "python -m http.server 8001 -d chatbot_frontend"
echo.
echo Services:
echo   - Chatbot UI: http://localhost:8001
echo   - Chatbot API: http://localhost:8000
goto end

:phase3nextjs
echo.
echo Starting Phase III - Chatbot (Next.js UI)...
echo.
echo Starting Chatbot Backend on http://localhost:8000...
start "Chatbot Backend (8000)" cmd /k "cd chatbot_backend && pip install -r requirements.txt 2>nul && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo Starting Chatbot Frontend (Next.js) on http://localhost:3001...
start "Chatbot Frontend (3001)" cmd /k "cd chatbot_frontend_nextjs && npm install 2>nul && npm run dev -- -p 3001"
echo.
echo Services:
echo   - Chatbot UI: http://localhost:3001
echo   - Chatbot API: http://localhost:8000
goto end

:all
echo.
echo Starting ALL Services (Phase II + III)...
echo.
echo Starting Todo API Backend on http://localhost:8000...
start "Todo Backend (8000)" cmd /k "cd backend && pip install -r requirements.txt 2>nul && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo Starting Chatbot Backend on http://localhost:8001...
start "Chatbot Backend (8001)" cmd /k "cd chatbot_backend && pip install -r requirements.txt 2>nul && uvicorn main:app --host 0.0.0.0 --port 8001 --reload"
timeout /t 3 /nobreak >nul
echo Starting Todo Frontend on http://localhost:3000...
start "Todo Frontend (3000)" cmd /k "cd frontend && npm install 2>nul && npm run dev"
echo Starting Chatbot Frontend on http://localhost:3001...
start "Chatbot Frontend (3001)" cmd /k "cd chatbot_frontend_nextjs && npm install 2>nul && npm run dev -- -p 3001"
echo.
echo Services:
echo   - Todo Frontend:    http://localhost:3000
echo   - Todo Backend:     http://localhost:8000
echo   - Chatbot Frontend: http://localhost:3001
echo   - Chatbot Backend:  http://localhost:8001
goto end

:phase5
echo.
echo Starting Phase V - Event-Driven (Kafka)...
echo.
echo Starting Kafka via Docker Compose...
start "Docker Compose" cmd /k "docker-compose up"
timeout /t 10 /nobreak >nul
echo Starting Reminders Service...
start "Reminders Service" cmd /k "cd reminders_service && pip install -r requirements.txt 2>nul && python main.py"
echo.
echo Services:
echo   - Kafka: localhost:9093
echo   - Kafka UI: http://localhost:8080
echo   - Reminders Service: Running
goto end

:end
echo.
echo ============================================================
echo Close the opened windows to stop services.
echo ============================================================
pause
