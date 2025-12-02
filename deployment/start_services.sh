#!/bin/bash

################################################################################
# Deal Win Probability Tool - Start Services Script (Linux/macOS)
################################################################################
# This script starts all required services for the application
# Supports both Docker and native Python deployment
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
VENV_DIR=".venv"
API_PORT=8000
STREAMLIT_PORT=8501
LOG_DIR="logs"

# PID files
API_PID_FILE="$LOG_DIR/api.pid"
STREAMLIT_PID_FILE="$LOG_DIR/streamlit.pid"

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

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

################################################################################
# Check if services are already running
################################################################################

check_running() {
    # Check if API is running
    if lsof -Pi :$API_PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        print_info "FastAPI is already running on port $API_PORT"
        API_RUNNING=true
    else
        API_RUNNING=false
    fi
    
    # Check if Streamlit is running
    if lsof -Pi :$STREAMLIT_PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        print_info "Streamlit is already running on port $STREAMLIT_PORT"
        STREAMLIT_RUNNING=true
    else
        STREAMLIT_RUNNING=false
    fi
}

################################################################################
# Start Docker Services
################################################################################

start_docker() {
    print_header "Starting Docker Services"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker not found!"
        exit 1
    fi
    
    cd docker
    
    # Check if containers are already running
    if docker-compose ps | grep -q "Up"; then
        print_info "Docker containers are already running"
        docker-compose ps
    else
        print_info "Starting Docker containers..."
        docker-compose up -d
        
        # Wait for services to be ready
        print_info "Waiting for services to start..."
        sleep 5
        
        print_success "Docker containers started"
        docker-compose ps
    fi
    
    cd ..
    
    echo ""
    print_success "Services are running!"
    print_info "Streamlit UI: http://localhost:8501"
    print_info "FastAPI: http://localhost:8000"
    print_info "API Docs: http://localhost:8000/docs"
    echo ""
}

################################################################################
# Start Native Python Services
################################################################################

start_native() {
    print_header "Starting Native Python Services"
    
    # Create logs directory
    mkdir -p "$LOG_DIR"
    
    # Activate virtual environment
    if [ -d "$VENV_DIR" ]; then
        source "$VENV_DIR/bin/activate"
        print_success "Virtual environment activated"
    else
        print_error "Virtual environment not found. Please run deployment.sh first."
        exit 1
    fi
    
    # Start FastAPI
    if [ "$API_RUNNING" = false ]; then
        print_info "Starting FastAPI backend..."
        nohup python api.py > "$LOG_DIR/api.log" 2>&1 &
        API_PID=$!
        echo $API_PID > "$API_PID_FILE"
        print_success "FastAPI started (PID: $API_PID)"
        print_info "Logs: $LOG_DIR/api.log"
    fi
    
    # Wait a moment for API to start
    sleep 2
    
    # Start Streamlit
    if [ "$STREAMLIT_RUNNING" = false ]; then
        print_info "Starting Streamlit UI..."
        nohup streamlit run app.py > "$LOG_DIR/streamlit.log" 2>&1 &
        STREAMLIT_PID=$!
        echo $STREAMLIT_PID > "$STREAMLIT_PID_FILE"
        print_success "Streamlit started (PID: $STREAMLIT_PID)"
        print_info "Logs: $LOG_DIR/streamlit.log"
    fi
    
    # Wait for services to be ready
    print_info "Waiting for services to start..."
    sleep 5
    
    echo ""
    print_success "Services are running!"
    print_info "Streamlit UI: http://localhost:$STREAMLIT_PORT"
    print_info "FastAPI: http://localhost:$API_PORT"
    print_info "API Docs: http://localhost:$API_PORT/docs"
    echo ""
    print_info "To stop services, run: ./stop_services.sh"
    print_info "To view logs:"
    echo "  FastAPI: tail -f $LOG_DIR/api.log"
    echo "  Streamlit: tail -f $LOG_DIR/streamlit.log"
    echo ""
}

################################################################################
# Main
################################################################################

main() {
    clear
    print_header "Starting Services"
    echo ""
    
    # Check if services are already running
    check_running
    
    # Ask deployment method
    echo "Choose deployment method:"
    echo "  1) Docker"
    echo "  2) Native Python"
    echo ""
    read -p "Enter choice [1-2]: " choice
    echo ""
    
    case $choice in
        1)
            start_docker
            ;;
        2)
            start_native
            ;;
        *)
            print_error "Invalid choice. Exiting."
            exit 1
            ;;
    esac
}

# Run main function
main
