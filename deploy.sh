#!/bin/bash
# Deployment Script for Schedule Creator

set -e

echo "🚀 Schedule Creator Deployment Script"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    print_success "Docker is installed"
}

# Check if Docker Compose is installed
check_docker_compose() {
    print_status "Checking Docker Compose installation..."
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    print_success "Docker Compose is installed"
}

# Check if required files exist
check_files() {
    print_status "Checking required files..."
    
    required_files=(
        "schedule_creator_app.py"
        "templates/schedule_creator.html"
        "Dockerfile"
        "docker-compose.yml"
        "requirements.txt"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            print_error "Required file $file not found!"
            exit 1
        fi
    done
    
    print_success "All required files found"
}

# Build Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t schedule-creator:latest .
    print_success "Docker image built successfully"
}

# Run with Docker Compose
deploy_with_compose() {
    print_status "Deploying with Docker Compose..."
    docker-compose up -d
    print_success "Application deployed with Docker Compose"
}

# Run with Docker run
deploy_with_docker() {
    print_status "Deploying with Docker run..."
    
    # Stop existing container if running
    docker stop schedule-creator-app 2>/dev/null || true
    docker rm schedule-creator-app 2>/dev/null || true
    
    # Run new container
    docker run -d \
        --name schedule-creator-app \
        -p 8080:8080 \
        -v "$(pwd)/credentials.json:/app/credentials.json:ro" \
        -v "$(pwd)/token.pickle:/app/token.pickle:rw" \
        -v "$(pwd)/schedule_backup.json:/app/schedule_backup.json:rw" \
        schedule-creator:latest
    
    print_success "Application deployed with Docker run"
}

# Check deployment status
check_deployment() {
    print_status "Checking deployment status..."
    
    # Wait for container to start
    sleep 5
    
    # Check if container is running
    if docker ps | grep -q schedule-creator-app; then
        print_success "Container is running"
    else
        print_error "Container is not running"
        docker logs schedule-creator-app
        exit 1
    fi
    
    # Check if application is responding
    if curl -f http://localhost:8080/ > /dev/null 2>&1; then
        print_success "Application is responding"
    else
        print_warning "Application is not responding yet. It may take a moment to start."
    fi
}

# Show deployment info
show_info() {
    echo ""
    echo "🎉 Deployment Complete!"
    echo "======================"
    echo ""
    echo "📱 Access your application at:"
    echo "   http://localhost:8080"
    echo ""
    echo "🔧 Useful commands:"
    echo "   View logs:     docker logs schedule-creator-app"
    echo "   Stop app:      docker stop schedule-creator-app"
    echo "   Start app:     docker start schedule-creator-app"
    echo "   Remove app:    docker rm -f schedule-creator-app"
    echo ""
    echo "🐳 Docker Compose commands:"
    echo "   View logs:     docker-compose logs"
    echo "   Stop all:      docker-compose down"
    echo "   Restart:       docker-compose restart"
    echo ""
}

# Main deployment function
main() {
    echo "Starting deployment process..."
    echo ""
    
    check_docker
    check_docker_compose
    check_files
    
    echo ""
    print_status "Choose deployment method:"
    echo "1) Docker Compose (recommended)"
    echo "2) Docker run"
    echo ""
    read -p "Enter your choice (1 or 2): " choice
    
    case $choice in
        1)
            build_image
            deploy_with_compose
            ;;
        2)
            build_image
            deploy_with_docker
            ;;
        *)
            print_error "Invalid choice. Please run the script again."
            exit 1
            ;;
    esac
    
    check_deployment
    show_info
}

# Run main function
main "$@"
