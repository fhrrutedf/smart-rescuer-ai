#!/bin/bash

# Quick deployment script for VPS
# نص سريع للنشر على VPS

echo "🚀 Smart Rescuer - VPS Deployment"
echo "=================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Please run as root (use sudo)${NC}"
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}📦 Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}📦 Installing Docker Compose...${NC}"
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

echo -e "${GREEN}✅ Docker installed${NC}"

# Ask for domain
read -p "🌐 Enter your domain (e.g., example.com): " DOMAIN
read -p "📧 Enter your email for SSL: " EMAIL

# Update configuration files
echo -e "${YELLOW}⚙️  Updating configuration...${NC}"

# Update docker-compose.yml
sed -i "s/yourdomain.com/$DOMAIN/g" docker-compose.yml
sed -i "s/your-email@example.com/$EMAIL/g" docker-compose.yml

# Update nginx.conf
sed -i "s/yourdomain.com/$DOMAIN/g" nginx/nginx.conf

echo -e "${GREEN}✅ Configuration updated${NC}"

# Build and start services
echo -e "${YELLOW}🔨 Building containers...${NC}"
docker-compose build

echo -e "${YELLOW}🚀 Starting services...${NC}"
docker-compose up -d nginx backend frontend

# Wait for services
echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 10

# Get SSL certificate
echo -e "${YELLOW}🔒 Getting SSL certificate...${NC}"
docker-compose run --rm certbot

# Restart nginx with SSL
echo -e "${YELLOW}🔄 Restarting Nginx with SSL...${NC}"
docker-compose restart nginx

# Check services
echo ""
echo -e "${GREEN}=================================="
echo "🎉 Deployment Complete!"
echo "==================================${NC}"
echo ""
echo "📊 Service Status:"
docker-compose ps
echo ""
echo -e "${GREEN}🌐 Your application is now available at:${NC}"
echo -e "   👉 https://$DOMAIN"
echo ""
echo -e "${YELLOW}📱 Test the camera feature:${NC}"
echo -e "   👉 https://$DOMAIN/emergency"
echo ""
echo -e "${YELLOW}📚 API Documentation:${NC}"
echo -e "   👉 https://$DOMAIN/docs"
echo ""
echo -e "${YELLOW}📝 Useful commands:${NC}"
echo "   docker-compose logs -f          # View logs"
echo "   docker-compose restart          # Restart all services"
echo "   docker-compose down             # Stop all services"
echo ""
