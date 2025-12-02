@echo off
REM ============================================================================
REM Deal Win Probability Tool - Stop Services Script (Windows)
REM ============================================================================
REM This script stops all running services
REM ============================================================================

setlocal enabledelayedexpansion

REM Colors
set "GREEN=[32m"
set "RED=[31m"
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

:print_info
echo [94m%~1[0m
goto :eof

REM ============================================================================
REM Stop Docker Services
REM ============================================================================

:stop_docker
call :print_header "Stopping Docker Services"

if exist "docker" (
    cd docker
    call :print_info "Stopping containers..."
    docker-compose stop
    call :print_success "Docker containers stopped"
    cd ..
)
goto :eof

REM ============================================================================
REM Stop Native Python Services
REM ============================================================================

:stop_native
call :print_header "Stopping Native Python Services"

REM Stop FastAPI (Python processes running api.py)
call :print_info "Stopping FastAPI processes..."
wmic process where "CommandLine like '%%api.py%%' and not CommandLine like '%%wmic%%'" call terminate >nul 2>&1
call :print_success "FastAPI stopped"

REM Stop Streamlit (Python processes running streamlit)
call :print_info "Stopping Streamlit processes..."
wmic process where "CommandLine like '%%streamlit%%' and not CommandLine like '%%wmic%%'" call terminate >nul 2>&1
call :print_success "Streamlit stopped"

REM Kill any remaining python processes on specific ports if needed
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8501" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo.
goto :eof

REM ============================================================================
REM Main
REM ============================================================================

:main
cls
call :print_header "Stopping Services"
echo.

echo Choose deployment method to stop:
echo   1) Docker
echo   2) Native Python
echo   3) All
echo.
set /p choice="Enter choice [1-3]: "
echo.

if "%choice%"=="1" (
    call :stop_docker
) else if "%choice%"=="2" (
    call :stop_native
) else if "%choice%"=="3" (
    call :stop_docker
    call :stop_native
) else (
    echo Invalid choice. Exiting.
    pause
    exit /b 1
)

call :print_success "Services stopped successfully"
echo.
pause
goto :eof

REM Run main function
call :main
