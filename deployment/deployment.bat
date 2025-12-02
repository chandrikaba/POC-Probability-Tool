@echo off
REM ============================================================================
REM Deal Win Probability Tool - Deployment Script (Windows)
REM ============================================================================
REM This script sets up and deploys the application
REM Supports both Docker and native Python deployment
REM ============================================================================

setlocal enabledelayedexpansion

REM Configuration
set PROJECT_NAME=Deal Win Probability Tool
set PYTHON_VERSION=3.10
set VENV_DIR=.venv

REM Colors (using PowerShell for colored output)
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

:print_warning
echo [93m%~1[0m
goto :eof

:print_info
echo [94m%~1[0m
goto :eof

REM ============================================================================
REM Check Prerequisites
REM ============================================================================

:check_prerequisites
call :print_header "Checking Prerequisites"

REM Check Python
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
    call :print_success "Python found: !PYTHON_VER!"
) else (
    call :print_error "Python not found. Please install Python %PYTHON_VERSION% or higher."
    pause
    exit /b 1
)

REM Check pip
where pip >nul 2>&1
if %errorlevel% equ 0 (
    set PIP_CMD=pip
    call :print_success "pip found"
) else (
    call :print_error "pip not found. Please install pip."
    pause
    exit /b 1
)

REM Check Docker (optional)
where docker >nul 2>&1
if %errorlevel% equ 0 (
    call :print_success "Docker found"
    set DOCKER_AVAILABLE=true
) else (
    call :print_warning "Docker not found. Will use native Python deployment."
    set DOCKER_AVAILABLE=false
)

REM Check Docker Compose (optional)
where docker-compose >nul 2>&1
if %errorlevel% equ 0 (
    call :print_success "Docker Compose found"
    set DOCKER_COMPOSE_AVAILABLE=true
) else (
    docker compose version >nul 2>&1
    if %errorlevel% equ 0 (
        call :print_success "Docker Compose found"
        set DOCKER_COMPOSE_AVAILABLE=true
    ) else (
        call :print_warning "Docker Compose not found."
        set DOCKER_COMPOSE_AVAILABLE=false
    )
)

echo.
goto :eof

REM ============================================================================
REM Setup Virtual Environment
REM ============================================================================

:setup_venv
call :print_header "Setting Up Python Virtual Environment"

if exist "%VENV_DIR%" (
    call :print_info "Virtual environment already exists at %VENV_DIR%"
    set /p RECREATE="Do you want to recreate it? (y/N): "
    if /i "!RECREATE!"=="y" (
        call :print_info "Removing existing virtual environment..."
        rmdir /s /q "%VENV_DIR%"
    ) else (
        call :print_info "Using existing virtual environment"
        goto :activate_venv
    )
)

call :print_info "Creating virtual environment..."
%PYTHON_CMD% -m venv "%VENV_DIR%"
call :print_success "Virtual environment created"

:activate_venv
REM Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"
call :print_success "Virtual environment activated"

REM Upgrade pip
call :print_info "Upgrading pip..."
%PIP_CMD% install --upgrade pip >nul 2>&1
call :print_success "pip upgraded"

echo.
goto :eof

REM ============================================================================
REM Install Dependencies
REM ============================================================================

:install_dependencies
call :print_header "Installing Dependencies"

if not exist "requirements.txt" (
    call :print_error "requirements.txt not found!"
    pause
    exit /b 1
)

call :print_info "Installing Python packages..."
%PIP_CMD% install -r requirements.txt
call :print_success "Dependencies installed"

echo.
goto :eof

REM ============================================================================
REM Setup Data Directories
REM ============================================================================

:setup_directories
call :print_header "Setting Up Data Directories"

if not exist "data\input" mkdir "data\input"
if not exist "data\output" mkdir "data\output"
if not exist "models" mkdir "models"
if not exist "logs" mkdir "logs"

call :print_success "Directories created"
echo.
goto :eof

REM ============================================================================
REM Docker Deployment
REM ============================================================================

:deploy_docker
call :print_header "Docker Deployment"

if "%DOCKER_AVAILABLE%"=="false" (
    call :print_error "Docker not available"
    goto :eof
)

if "%DOCKER_COMPOSE_AVAILABLE%"=="false" (
    call :print_error "Docker Compose not available"
    goto :eof
)

cd docker

call :print_info "Building Docker images..."
docker-compose build
call :print_success "Docker images built"

call :print_info "Starting Docker containers..."
docker-compose up -d
call :print_success "Docker containers started"

cd ..

echo.
call :print_success "Docker deployment complete!"
call :print_info "Streamlit UI: http://localhost:8501"
call :print_info "FastAPI: http://localhost:8000"
call :print_info "API Docs: http://localhost:8000/docs"
echo.
goto :eof

REM ============================================================================
REM Native Python Deployment
REM ============================================================================

:deploy_native
call :print_header "Native Python Deployment"

call :print_info "Starting services..."
call :print_info "Use the start_services.bat script to start FastAPI and Streamlit"
call :print_info "Or run manually:"
echo.
echo   Terminal 1: python api.py
echo   Terminal 2: streamlit run app.py
echo.

call :print_success "Setup complete! Ready to start services."
echo.
goto :eof

REM ============================================================================
REM Main Deployment Flow
REM ============================================================================

:main
cls
call :print_header "%PROJECT_NAME% - Deployment"
echo.

REM Check prerequisites
call :check_prerequisites

REM Ask deployment method
echo Choose deployment method:
echo   1) Docker (recommended for production)
echo   2) Native Python (for development)
echo.
set /p choice="Enter choice [1-2]: "
echo.

if "%choice%"=="1" (
    if "%DOCKER_AVAILABLE%"=="true" (
        if "%DOCKER_COMPOSE_AVAILABLE%"=="true" (
            call :deploy_docker
        ) else (
            call :print_error "Docker Compose not available. Falling back to native deployment."
            call :setup_venv
            call :install_dependencies
            call :setup_directories
            call :deploy_native
        )
    ) else (
        call :print_error "Docker not available. Falling back to native deployment."
        call :setup_venv
        call :install_dependencies
        call :setup_directories
        call :deploy_native
    )
) else if "%choice%"=="2" (
    call :setup_venv
    call :install_dependencies
    call :setup_directories
    call :deploy_native
) else (
    call :print_error "Invalid choice. Exiting."
    pause
    exit /b 1
)

call :print_header "Deployment Complete!"
call :print_success "Application is ready to use"
echo.
pause
goto :eof

REM Run main function
call :main
