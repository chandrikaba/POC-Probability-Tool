#!/bin/bash

################################################################################
# Deal Win Probability Tool - Stop Services Script (Linux/macOS)
################################################################################
# This script stops all running services
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
LOG_DIR="logs"
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

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

################################################################################
# Stop Docker Services
################################################################################

stop_docker() {
    print_header "Stopping Docker Services"
    
    if [ -d "docker" ]; then
        cd docker
        if docker-compose ps | grep -q "Up"; then
            print_info "Stopping containers..."
            docker-compose stop
            print_success "Docker containers stopped"
        else
            print_info "No running Docker containers found"
        fi
        cd ..
    fi
}

################################################################################
# Stop Native Python Services
################################################################################

stop_native() {
    print_header "Stopping Native Python Services"
    
    # Stop API
    if [ -f "$API_PID_FILE" ]; then
        PID=$(cat "$API_PID_FILE")
        if ps -p $PID > /dev/null; then
            print_info "Stopping FastAPI (PID: $PID)..."
            kill $PID
            print_success "FastAPI stopped"
        else
            print_info "FastAPI process not found"
        fi
        rm "$API_PID_FILE"
    else
        # Try to find by port
        PID=$(lsof -t -i:8000)
        if [ ! -z "$PID" ]; then
            print_info "Stopping FastAPI on port 8000 (PID: $PID)..."
            kill $PID
            print_success "FastAPI stopped"
        fi
    fi
    
    # Stop Streamlit
    if [ -f "$STREAMLIT_PID_FILE" ]; then
        PID=$(cat "$STREAMLIT_PID_FILE")
        if ps -p $PID > /dev/null; then
            print_info "Stopping Streamlit (PID: $PID)..."
            kill $PID
            print_success "Streamlit stopped"
        else
            print_info "Streamlit process not found"
        fi
        rm "$STREAMLIT_PID_FILE"
    else
        # Try to find by port
        PID=$(lsof -t -i:8501)
        if [ ! -z "$PID" ]; then
            print_info "Stopping Streamlit on port 8501 (PID: $PID)..."
            kill $PID
            print_success "Streamlit stopped"
        fi
    fi
    
    echo ""
}

################################################################################
# Main
################################################################################

main() {
    clear
    print_header "Stopping Services"
    echo ""
    
    # Ask deployment method
    echo "Choose deployment method to stop:"
    echo "  1) Docker"
    echo "  2) Native Python"
    echo "  3) All"
    echo ""
    read -p "Enter choice [1-3]: " choice
    echo ""
    
    case $choice in
        1)
            stop_docker
            ;;
        2)
            stop_native
            ;;
        3)
            stop_docker
            stop_native
            ;;
        *)
            echo "Invalid choice. Exiting."
            exit 1
            ;;
    esac
    
    print_success "Services stopped successfully"
    echo ""
}

# Run main function
main
