#!/bin/bash

################################################################################
# Deal Win Probability Tool - Deployment Script (Linux/macOS)
################################################################################
# This script sets up and deploys the application
# Supports both Docker and native Python deployment
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="Deal Win Probability Tool"
PYTHON_VERSION="3.10"
VENV_DIR=".venv"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

################################################################################
# Check Prerequisites
################################################################################

check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_CMD=python3
        PYTHON_VER=$(python3 --version | cut -d' ' -f2)
        print_success "Python found: $PYTHON_VER"
    elif command -v python &> /dev/null; then
        PYTHON_CMD=python
        PYTHON_VER=$(python --version | cut -d' ' -f2)
        print_success "Python found: $PYTHON_VER"
    else
        print_error "Python not found. Please install Python $PYTHON_VERSION or higher."
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        PIP_CMD=pip3
        print_success "pip found"
    elif command -v pip &> /dev/null; then
        PIP_CMD=pip
        print_success "pip found"
    else
        print_error "pip not found. Please install pip."
        exit 1
    fi
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        print_success "Docker found"
        DOCKER_AVAILABLE=true
    else
        print_warning "Docker not found. Will use native Python deployment."
        DOCKER_AVAILABLE=false
    fi
    
    # Check Docker Compose (optional)
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1; then
        print_success "Docker Compose found"
        DOCKER_COMPOSE_AVAILABLE=true
    else
        print_warning "Docker Compose not found."
        DOCKER_COMPOSE_AVAILABLE=false
    fi
    
    echo ""
}

################################################################################
# Setup Virtual Environment
################################################################################

setup_venv() {
    print_header "Setting Up Python Virtual Environment"
    
    if [ -d "$VENV_DIR" ]; then
        print_info "Virtual environment already exists at $VENV_DIR"
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Removing existing virtual environment..."
            rm -rf "$VENV_DIR"
        else
            print_info "Using existing virtual environment"
            return 0
        fi
    fi
    
    print_info "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    print_success "Virtual environment created"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    print_success "Virtual environment activated"
    
    # Upgrade pip
    print_info "Upgrading pip..."
    $PIP_CMD install --upgrade pip
    print_success "pip upgraded"
    
    echo ""
}

################################################################################
# Install Dependencies
################################################################################

install_dependencies() {
    print_header "Installing Dependencies"
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found!"
        exit 1
    fi
    
    print_info "Installing Python packages..."
    $PIP_CMD install -r requirements.txt
    print_success "Dependencies installed"
    
    echo ""
}

################################################################################
# Setup Data Directories
################################################################################

setup_directories() {
    print_header "Setting Up Data Directories"
    
    mkdir -p data/input
    mkdir -p data/output
    mkdir -p models
    mkdir -p logs
    
    print_success "Directories created"
    echo ""
}

################################################################################
# Docker Deployment
################################################################################

deploy_docker() {
    print_header "Docker Deployment"
    
    if [ "$DOCKER_AVAILABLE" = false ] || [ "$DOCKER_COMPOSE_AVAILABLE" = false ]; then
        print_error "Docker or Docker Compose not available"
        return 1
    fi
    
    cd docker
    
    print_info "Building Docker images..."
    docker-compose build
    print_success "Docker images built"
    
    print_info "Starting Docker containers..."
    docker-compose up -d
    print_success "Docker containers started"
    
    cd ..
    
    echo ""
    print_success "Docker deployment complete!"
    print_info "Streamlit UI: http://localhost:8501"
    print_info "FastAPI: http://localhost:8000"
    print_info "API Docs: http://localhost:8000/docs"
    echo ""
}

################################################################################
# Native Python Deployment
################################################################################

deploy_native() {
    print_header "Native Python Deployment"
    
    # Activate virtual environment if not already activated
    if [ -z "$VIRTUAL_ENV" ]; then
        source "$VENV_DIR/bin/activate"
    fi
    
    print_info "Starting services..."
    print_info "Use the start_services.sh script to start FastAPI and Streamlit"
    print_info "Or run manually:"
    echo ""
    echo "  Terminal 1: python api.py"
    echo "  Terminal 2: streamlit run app.py"
    echo ""
    
    print_success "Setup complete! Ready to start services."
    echo ""
}

################################################################################
# Main Deployment Flow
################################################################################

main() {
    clear
    print_header "$PROJECT_NAME - Deployment"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Ask deployment method
    echo "Choose deployment method:"
    echo "  1) Docker (recommended for production)"
    echo "  2) Native Python (for development)"
    echo ""
    read -p "Enter choice [1-2]: " choice
    echo ""
    
    case $choice in
        1)
            if [ "$DOCKER_AVAILABLE" = true ] && [ "$DOCKER_COMPOSE_AVAILABLE" = true ]; then
                deploy_docker
            else
                print_error "Docker deployment not available. Falling back to native deployment."
                setup_venv
                install_dependencies
                setup_directories
                deploy_native
            fi
            ;;
        2)
            setup_venv
            install_dependencies
            setup_directories
            deploy_native
            ;;
        *)
            print_error "Invalid choice. Exiting."
            exit 1
            ;;
    esac
    
    print_header "Deployment Complete!"
    print_success "Application is ready to use"
    echo ""
}

# Run main function
main
