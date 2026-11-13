#!/bin/bash
set -euo pipefail

# ---------------------------------------------------------------------------
# System updates and dependencies
# ---------------------------------------------------------------------------
yum update -y
yum install -y docker git postgresql15

systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user

# ---------------------------------------------------------------------------
# Docker Compose plugin
# ---------------------------------------------------------------------------
mkdir -p /usr/local/lib/docker/cli-plugins
curl -SL \
  https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# ---------------------------------------------------------------------------
# Clone application repository
# ---------------------------------------------------------------------------
cd /home/ec2-user
git clone https://github.com/YOUR_GITHUB_USER/ask-your-database.git app
chown -R ec2-user:ec2-user app
cd app

# ---------------------------------------------------------------------------
# Write environment file
# ---------------------------------------------------------------------------
cat > .env <<EOF
DATABASE_URL=postgresql://app:${db_password}@${db_endpoint}/ask_your_db
LLM_BACKEND=bedrock
AWS_REGION=${aws_region}
APP_READONLY_USER=app_readonly
APP_READONLY_PASSWORD=app_readonly_password
EOF

# ---------------------------------------------------------------------------
# Start application
# ---------------------------------------------------------------------------
docker compose up -d

# ---------------------------------------------------------------------------
# Log startup complete
# ---------------------------------------------------------------------------
echo "ask-your-database startup complete at $(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  >> /var/log/app-startup.log
