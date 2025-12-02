@echo off
REM ============================================================================
REM Deal Win Probability Tool - Start Services Script (Windows)
REM ============================================================================
REM This script starts all required services for the application
REM Supports both Docker and native Python deployment
REM ============================================================================

setlocal enabledelayedexpansion

REM Configuration
set VENV_DIR=.venv
set API_PORT=8000
set STREAMLIT_PORT=8501
set LOG_DIR=logs

REM Colors
set "GREEN=[32m"
set "RED=[31m"
set "YELLOW=[33m"
set "BLUE=[34m"
set "NC=[0m"

REM ============================================================================
REM Helper Functions
REM ============================================================================

:print_header
echo.
echo ========================================
echo %~1
echo ========================================
echo.
goto :eof

:print_success
echo [92m%~1[0m
goto :eof

:print_error
echo [91m%~1[0m
goto :eof

:print_info
echo [94m%~1[0m
goto :eof

REM ============================================================================
REM Start Docker Services
REM ============================================================================

:start_docker
call :print_header "Starting Docker Services"

where docker >nul 2>&1
if %errorlevel% neq 0 (
    call :print_error "Docker not found!"
    goto :eof
)

cd docker

call :print_info "Starting Docker containers..."
docker-compose up -d

call :print_info "Waiting for services to start..."
timeout /t 5 /nobreak >nul

call :print_success "Docker containers started"
docker-compose ps

cd ..

echo.
call :print_success "Services are running!"
call :print_info "Streamlit UI: http://localhost:8501"
call :print_info "FastAPI: http://localhost:8000"
call :print_info "API Docs: http://localhost:8000/docs"
echo.
goto :eof

REM ============================================================================
REM Start Native Python Services
REM ============================================================================

:start_native
call :print_header "Starting Native Python Services"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Activate virtual environment
if exist "%VENV_DIR%" (
    call "%VENV_DIR%\Scripts\activate.bat"
    call :print_success "Virtual environment activated"
) else (
    call :print_error "Virtual environment not found. Please run deployment.bat first."
    pause
    exit /b 1
)

REM Start FastAPI
call :print_info "Starting FastAPI backend..."
start "FastAPI Backend" /min cmd /c "python api.py > %LOG_DIR%\api.log 2>&1"
call :print_success "FastAPI started in new window"

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start Streamlit
call :print_info "Starting Streamlit UI..."
start "Streamlit UI" /min cmd /c "streamlit run app.py > %LOG_DIR%\streamlit.log 2>&1"
call :print_success "Streamlit started in new window"

REM Wait for services
call :print_info "Waiting for services to start..."
timeout /t 5 /nobreak >nul

echo.
call :print_success "Services are running!"
call :print_info "Streamlit UI: http://localhost:%STREAMLIT_PORT%"
call :print_info "FastAPI: http://localhost:%API_PORT%"
call :print_info "API Docs: http://localhost:%API_PORT%/docs"
echo.
call :print_info "To stop services, run: stop_services.bat"
call :print_info "Logs are available in the %LOG_DIR% directory"
echo.
goto :eof

REM ============================================================================
REM Main
REM ============================================================================

:main
cls
call :print_header "Starting Services"
echo.

echo Choose deployment method:
echo   1) Docker
echo   2) Native Python
echo.
set /p choice="Enter choice [1-2]: "
echo.

if "%choice%"=="1" (
    call :start_docker
) else if "%choice%"=="2" (
    call :start_native
) else (
    call :print_error "Invalid choice. Exiting."
    pause
    exit /b 1
)

pause
goto :eof

REM Run main function
call :main
