#!/bin/bash
# Smart Rescuer - Quick Deployment Script for VPS
# سكريبت النشر السريع على VPS

set -e  # Stop on error

echo "======================================"
echo "Smart Rescuer - VPS Deployment"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get domain
read -p "Enter your domain (e.g., example.com): " DOMAIN
read -p "Enter your email for SSL: " EMAIL

echo ""
echo -e "${YELLOW}Starting deployment...${NC}"
echo ""

# 1. Update system
echo -e "${GREEN}[1/8]${NC} Updating system..."
apt update && apt upgrade -y

# 2. Install Docker
echo -e "${GREEN}[2/8]${NC} Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    echo "Docker already installed"
fi

# 3. Install Docker Compose
echo -e "${GREEN}[3/8]${NC} Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    apt install docker-compose -y
else
    echo "Docker Compose already installed"
fi

# 4. Create directories
echo -e "${GREEN}[4/8]${NC} Creating directories..."
mkdir -p /var/www/smart-rescuer
cd /var/www/smart-rescuer

# 5. Create .env file
echo -e "${GREEN}[5/8]${NC} Creating environment file..."
SECRET_KEY=$(openssl rand -hex 32)

cat > .env << EOF
# Domain Configuration
DOMAIN=$DOMAIN
EMAIL=$EMAIL

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Frontend Configuration
VITE_API_URL=https://$DOMAIN

# Security
SECRET_KEY=$SECRET_KEY
EOF

echo ".env file created"

# 6. Build and start services
echo -e "${GREEN}[6/8]${NC} Building Docker images..."
docker-compose build

echo -e "${GREEN}[7/8]${NC} Starting services..."
docker-compose up -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# 7. Setup AI Model
echo -e "${GREEN}[8/8]${NC} Setting up AI model..."
docker-compose exec -T backend python scripts/setup_ai_quick.py

# 8. Setup SSL
echo ""
echo -e "${YELLOW}Setting up SSL certificate...${NC}"
docker-compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  -d $DOMAIN \
  --email $EMAIL \
  --agree-tos \
  --no-eff-email \
  --non-interactive

# Restart Nginx
docker-compose restart nginx

# Setup firewall
echo ""
echo -e "${YELLOW}Configuring firewall...${NC}"
if command -v ufw &> /dev/null; then
    ufw --force enable
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    echo "Firewall configured"
fi

# Done!
echo ""
echo "======================================"
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo "======================================"
echo ""
echo "Your application is now running at:"
echo -e "${GREEN}https://$DOMAIN${NC}"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f          # View logs"
echo "  docker-compose restart          # Restart services"
echo "  docker-compose ps               # Check status"
echo ""
echo "To update the application:"
echo "  cd /var/www/smart-rescuer"
echo "  git pull"
echo "  docker-compose down && docker-compose up -d --build"
echo ""
echo "======================================"
