#!/bin/bash

set -e  # Exit on error

echo "🚀 Starting deployment of Gemini Bot..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
BOT_DIR="/opt/bots/gemini-bot"
BACKUP_DIR="/opt/bots/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if . env exists
if [ ! -f "$BOT_DIR/.env" ]; then
    print_error ". env file not found!"
    exit 1
fi

# Backup current version
print_status "Creating backup..."
mkdir -p $BACKUP_DIR
if [ -d "$BOT_DIR" ]; then
    tar -czf "$BACKUP_DIR/gemini-bot_$DATE.tar.gz" -C "$BOT_DIR" .
    print_success "Backup created:  gemini-bot_$DATE.tar.gz"
fi

# Navigate to bot directory
cd $BOT_DIR

# Pull latest changes
print_status "Pulling latest code from GitHub..."
git pull origin main

# Stop existing container
print_status "Stopping existing containers..."
docker-compose down

# Remove old images
print_status "Cleaning up old Docker images..."
docker image prune -f

# Build new image
print_status "Building Docker image..."
docker-compose build --no-cache

# Start the bot
print_status "Starting the bot..."
docker-compose up -d

# Wait for container to be healthy
print_status "Waiting for bot to start..."
sleep 5

# Check if container is running
if [ "$(docker ps -q -f name=gemini-bot)" ]; then
    print_success "✅ Gemini Bot deployed successfully!"
    echo ""
    echo "📊 Container Status:"
    docker-compose ps
    echo ""
    echo "📝 Logs:"
    docker-compose logs --tail=20
else
    print_error "❌ Deployment failed! Container is not running."
    print_status "Rolling back to previous version..."
    tar -xzf "$BACKUP_DIR/gemini-bot_$DATE.tar.gz" -C "$BOT_DIR"
    docker-compose up -d
    exit 1
fi

print_success "🎉 Deployment completed!"