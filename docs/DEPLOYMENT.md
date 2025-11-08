# PaddleCoach Deployment Guide

**Author:** Rakshit  
**Version:** 1.0.0  
**Last Updated:** November 7, 2025

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Minimum:**
- Python 3.10 or higher
- 4GB RAM
- 2GB free disk space
- Modern web browser

**Recommended:**
- Python 3.11+
- 8GB RAM
- 10GB free disk space (for video storage)
- NVIDIA GPU (for faster AI processing)

### Required Software

- Python 3.10+
- pip (Python package manager)
- Git
- Node.js 16+ (optional, for advanced frontend builds)

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd PaddleCoach
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Create a `requirements.txt` file with:

```txt
# Web Framework
flask==3.0.0
flask-socketio==5.3.5
flask-cors==4.0.0

# WebSocket
python-socketio==5.10.0
eventlet==0.33.3

# HTTP Requests
requests==2.31.0

# Environment Variables
python-dotenv==1.0.0

# Data Processing
numpy==1.24.3
pandas==2.0.3

# API Dependencies (will be added by other team members)
# Add Ashwani's vision dependencies
# Add Ashar's database dependencies
# Add Mohnish's AI dependencies
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_APP=src/frontend/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Database Configuration (from Ashar's setup)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=paddlecoach
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# API Keys
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Optional: External APIs
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the Application

```bash
python src/frontend/app.py
```

The application will be available at `http://localhost:5000`

---

## Production Deployment

### Option 1: Traditional Server (Ubuntu/Debian)

#### 1. Prepare the Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3-pip nginx -y

# Install system dependencies for OpenCV (from Ashwani's setup)
sudo apt install libgl1-mesa-glx libglib2.0-0 -y
```

#### 2. Clone and Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/paddlecoach
cd /var/www/paddlecoach

# Clone repository
sudo git clone <repository-url> .

# Create virtual environment
sudo python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Gunicorn

Install Gunicorn:
```bash
pip install gunicorn gevent gevent-websocket
```

Create `gunicorn_config.py`:
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
timeout = 120
keepalive = 5
```

#### 4. Create Systemd Service

Create `/etc/systemd/system/paddlecoach.service`:

```ini
[Unit]
Description=PaddleCoach Flask Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/paddlecoach
Environment="PATH=/var/www/paddlecoach/venv/bin"
ExecStart=/var/www/paddlecoach/venv/bin/gunicorn -c gunicorn_config.py src.frontend.app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl enable paddlecoach
sudo systemctl start paddlecoach
sudo systemctl status paddlecoach
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/paddlecoach`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_read_timeout 86400;
    }

    location /static {
        alias /var/www/paddlecoach/src/frontend/static;
        expires 30d;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/paddlecoach /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. SSL Certificate (Optional but Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "src/frontend/app.py"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DB_HOST=db
      - DB_NAME=paddlecoach
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
    volumes:
      - ./data:/app/data
    depends_on:
      - db
    restart: always

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD}
      - MYSQL_DATABASE=paddlecoach
      - MYSQL_USER=${DB_USER}
      - MYSQL_PASSWORD=${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql
    restart: always

volumes:
  db_data:
```

#### 3. Build and Run

```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: Cloud Platform Deployment

#### Heroku

1. Create `Procfile`:
```
web: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 4 src.frontend.app:app
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Deploy:
```bash
heroku create paddlecoach
heroku config:set FLASK_ENV=production SECRET_KEY=your-secret-key
git push heroku master
```

#### AWS EC2

1. Launch Ubuntu EC2 instance
2. Follow "Traditional Server" setup above
3. Configure security groups (ports 80, 443, 5000)
4. Set up Elastic IP for static address

#### Google Cloud Platform

1. Create GCE instance
2. Follow "Traditional Server" setup
3. Configure firewall rules
4. Set up Cloud SQL for database

---

## Environment Configuration

### Development Environment

`.env.development`:
```env
FLASK_ENV=development
DEBUG=True
HOST=127.0.0.1
PORT=5000
```

### Production Environment

`.env.production`:
```env
FLASK_ENV=production
DEBUG=False
HOST=0.0.0.0
PORT=5000
SECRET_KEY=<generate-strong-key>
```

Generate strong secret key:
```python
import secrets
print(secrets.token_hex(32))
```

### Database Configuration

Ensure MySQL is configured with proper user permissions:

```sql
CREATE DATABASE paddlecoach;
CREATE USER 'paddlecoach_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON paddlecoach.* TO 'paddlecoach_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## Monitoring and Maintenance

### Log Management

**View Application Logs:**
```bash
# Systemd service
sudo journalctl -u paddlecoach -f

# Docker
docker-compose logs -f web
```

**Configure Log Rotation:**

Create `/etc/logrotate.d/paddlecoach`:
```
/var/log/paddlecoach/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

### Backup Strategy

**Database Backup:**
```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u root -p paddlecoach > /backups/paddlecoach_$DATE.sql
```

**Application Data Backup:**
```bash
# Backup uploaded files and data
tar -czf paddlecoach_data_$(date +%Y%m%d).tar.gz /var/www/paddlecoach/data
```

### Performance Tuning

**Nginx Optimization:**
```nginx
# Add to nginx.conf
gzip on;
gzip_types text/plain text/css application/json application/javascript;
client_max_body_size 100M;  # For video uploads
```

**Gunicorn Workers:**
- CPU-bound tasks: workers = (2 × CPU cores) + 1
- I/O-bound tasks: workers = (4 × CPU cores)

---

## Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Database Connection Failed:**
- Check MySQL is running: `sudo systemctl status mysql`
- Verify credentials in `.env`
- Check firewall rules
- Test connection: `mysql -u user -p`

**WebSocket Not Working:**
- Ensure Nginx is configured for WebSocket upgrade
- Check firewall allows WebSocket connections
- Verify `flask-socketio` is installed correctly

**Static Files Not Loading:**
- Check Nginx static file configuration
- Verify file permissions: `chmod -R 755 static/`
- Clear browser cache

### Health Checks

Create `health_check.sh`:
```bash
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/)
if [ $response -eq 200 ]; then
    echo "Service is healthy"
    exit 0
else
    echo "Service is down"
    exit 1
fi
```

---

## Security Best Practices

1. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Use Environment Variables** - Never commit secrets to git

3. **Enable HTTPS** - Use Let's Encrypt for free SSL

4. **Configure Firewall**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

5. **Regular Backups** - Automate database and file backups

6. **Monitor Logs** - Set up log monitoring and alerts

---

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (Nginx, HAProxy)
- Deploy multiple application instances
- Use Redis for session storage
- Implement database replication

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Implement caching (Redis, Memcached)
- Use CDN for static files

---

## Support

For deployment issues:
- Check application logs
- Review Nginx error logs: `/var/log/nginx/error.log`
- Consult API documentation
- Contact development team

---

**Deployment Complete!** 🚀

Your PaddleCoach application should now be running successfully. Monitor logs regularly and keep the system updated for optimal performance.
