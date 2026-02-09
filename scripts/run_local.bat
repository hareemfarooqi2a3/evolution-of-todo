@echo off
REM Evolution of Todo - Phase Launcher
REM Run this script to start any phase of the hackathon project

echo.
echo ============================================================
echo   EVOLUTION OF TODO - Hackathon Project Launcher
echo ============================================================
echo.
echo   See PHASES.md for detailed documentation
echo.
echo Choose a phase to run:
echo.
echo   [PHASE I]   CLI Application
echo     1. CLI Todo App (file-based storage)
echo.
echo   [PHASE II]  Web Application
echo     2. Backend API + Frontend (http://localhost:8000 + :3000)
echo.
echo   [PHASE III] AI Chatbot
echo     3. Chatbot with Simple UI (requires OpenAI API key)
echo     4. Chatbot with Next.js UI (requires OpenAI API key)
echo.
echo   [PHASE IV]  Kubernetes
echo     5. Deploy to Minikube (requires Docker + Minikube)
echo.
echo   [PHASE V]   Event-Driven
echo     6. Kafka + Reminders Service (requires Docker)
echo.
echo   [ALL]
echo     7. Run Phase II + III together
echo.
set /p choice="Enter choice (1-7): "

if "%choice%"=="1" goto phase1
if "%choice%"=="2" goto phase2
if "%choice%"=="3" goto phase3
if "%choice%"=="4" goto phase3nextjs
if "%choice%"=="5" goto phase4
if "%choice%"=="6" goto phase5
if "%choice%"=="7" goto all
goto end

:phase1
echo.
echo ============================================================
echo   PHASE I - CLI Todo Application
echo ============================================================
echo.
echo Commands:
echo   python -m src.main add --title "Task name"
echo   python -m src.main list
echo   python -m src.main complete --id 1
echo   python -m src.main delete --id 1
echo.
start "Phase I - CLI" cmd /k "cd /d "%~dp0\..\phase1_cli" && echo Ready! Type commands above to manage todos."
goto end

:phase2
echo.
echo ============================================================
echo   PHASE II - Web Application
echo ============================================================
echo.
echo Starting Backend API on http://localhost:8000...
start "Phase II - Backend (8000)" cmd /k "cd /d "%~dp0\..\backend" && pip install -r requirements.txt 2>nul && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo Starting Frontend on http://localhost:3000...
start "Phase II - Frontend (3000)" cmd /k "cd /d "%~dp0\..\frontend" && npm install 2>nul && npm run dev"
echo.
echo Services starting:
echo   - Backend API:  http://localhost:8000
echo   - Frontend:     http://localhost:3000
echo.
echo Open http://localhost:3000 in your browser
goto end

:phase3
echo.
echo ============================================================
echo   PHASE III - AI Chatbot (Simple UI)
echo ============================================================
echo.
echo NOTE: Requires OpenAI API key in chatbot_backend\.env
echo.
echo Starting Chatbot API on http://localhost:8000...
start "Phase III - Chatbot API (8000)" cmd /k "cd /d "%~dp0\..\chatbot_backend" && pip install -r requirements.txt 2>nul && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo Starting Chatbot UI on http://localhost:8001...
start "Phase III - Chatbot UI (8001)" cmd /k "cd /d "%~dp0\.." && python -m http.server 8001 -d chatbot_frontend"
echo.
echo Services starting:
echo   - Chatbot API:  http://localhost:8000
echo   - Chatbot UI:   http://localhost:8001
echo.
echo Open http://localhost:8001 in your browser
goto end

:phase3nextjs
echo.
echo ============================================================
echo   PHASE III - AI Chatbot (Next.js UI)
echo ============================================================
echo.
echo NOTE: Requires OpenAI API key in chatbot_backend\.env
echo.
echo Starting Chatbot API on http://localhost:8000...
start "Phase III - Chatbot API (8000)" cmd /k "cd /d "%~dp0\..\chatbot_backend" && pip install -r requirements.txt 2>nul && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo Starting Chatbot Next.js UI on http://localhost:3001...
start "Phase III - Chatbot Next.js (3001)" cmd /k "cd /d "%~dp0\..\chatbot_frontend_nextjs" && npm install 2>nul && npm run dev -- -p 3001"
echo.
echo Services starting:
echo   - Chatbot API:      http://localhost:8000
echo   - Chatbot Next.js:  http://localhost:3001
echo.
echo Open http://localhost:3001 in your browser
goto end

:phase4
echo.
echo ============================================================
echo   PHASE IV - Kubernetes Deployment
echo ============================================================
echo.
echo Requires: Docker, Minikube, Helm
echo.
echo Starting Minikube...
start "Phase IV - Minikube" cmd /k "minikube start && cd /d "%~dp0\.." && scripts\deploy-local.sh"
goto end

:phase5
echo.
echo ============================================================
echo   PHASE V - Event-Driven Architecture
echo ============================================================
echo.
echo Requires: Docker
echo.
echo Starting Kafka via Docker Compose...
start "Phase V - Kafka" cmd /k "cd /d "%~dp0\.." && docker-compose up"
timeout /t 10 /nobreak >nul
echo Starting Reminders Service...
start "Phase V - Reminders" cmd /k "cd /d "%~dp0\..\reminders_service" && pip install -r requirements.txt 2>nul && python main.py"
echo.
echo Services starting:
echo   - Kafka:      localhost:9093
echo   - Kafka UI:   http://localhost:8080
echo   - Reminders:  Running
goto end

:all
echo.
echo ============================================================
echo   ALL SERVICES - Phase II + III
echo ============================================================
echo.
echo Starting all services...
echo.
echo Starting Phase II Backend on http://localhost:8000...
start "Phase II - Backend (8000)" cmd /k "cd /d "%~dp0\..\backend" && pip install -r requirements.txt 2>nul && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo Starting Phase III Chatbot on http://localhost:8001...
start "Phase III - Chatbot (8001)" cmd /k "cd /d "%~dp0\..\chatbot_backend" && pip install -r requirements.txt 2>nul && uvicorn main:app --host 0.0.0.0 --port 8001 --reload"
timeout /t 3 /nobreak >nul
echo Starting Phase II Frontend on http://localhost:3000...
start "Phase II - Frontend (3000)" cmd /k "cd /d "%~dp0\..\frontend" && npm install 2>nul && npm run dev"
echo Starting Phase III Chatbot UI on http://localhost:3001...
start "Phase III - Chatbot UI (3001)" cmd /k "cd /d "%~dp0\..\chatbot_frontend_nextjs" && npm install 2>nul && npm run dev -- -p 3001"
echo.
echo Services starting:
echo   - Phase II Backend:   http://localhost:8000
echo   - Phase II Frontend:  http://localhost:3000
echo   - Phase III Chatbot:  http://localhost:8001
echo   - Phase III Chat UI:  http://localhost:3001
goto end

:end
echo.
echo ============================================================
echo   Close the opened windows to stop services.
echo ============================================================
echo.
pause
