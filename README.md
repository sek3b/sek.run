# sek.run

Personal website and blog built with Flask.

## Deployment to DigitalOcean

**Droplet IP:** `162.243.107.222`

---

## Initial Server Setup (As Root)

### 1. Connect as Root (First Time Only)

```bash
ssh root@162.243.107.222
```

### 2. Update System

```bash
apt update && apt upgrade -y
```

### 3. Create Deploy User

```bash
adduser sek3b
usermod -aG sudo sek3b
```

### 4. Set Up SSH Key for Deploy User

```bash
mkdir -p /home/sek3b/.ssh
cp /root/.ssh/authorized_keys /home/sek3b/.ssh/
chown -R sek3b:sek3b /home/sek3b/.ssh
chmod 700 /home/sek3b/.ssh
chmod 600 /home/sek3b/.ssh/authorized_keys
```

### 5. Test SSH Access (From Local Machine)

Open a new terminal and verify you can connect:
```bash
ssh sek3b@162.243.107.222
```

### 6. Disable Root SSH Access

Back on the server as root:
```bash
sudo sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### 7. Log Out of Root

```bash
exit
```

---

## Application Deployment (As Deploy User)

### 1. Connect as Deploy User

```bash
ssh sek3b@162.243.107.222
```

### 2. Install Dependencies

```bash
sudo apt install -y python3 python3-pip python3-venv nginx git
```

### 3. Set Up Application Directory

```bash
sudo mkdir -p /var/www/sekrun
sudo chown sek3b:sek3b /var/www/sekrun
```

### 4. Clone the Repository

```bash
cd /var/www/sekrun
git clone https://github.com/sek3b/sek.run.git .
```

### 5. Create Virtual Environment & Install Dependencies

```bash
cd /var/www/sekrun
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 6. Test the Application

```bash
source venv/bin/activate
gunicorn --bind 0.0.0.0:5000 app:app
```

Visit `http://162.243.107.222:5000` to verify it works, then Ctrl+C to stop.

### 7. Create Systemd Service

```bash
sudo tee /etc/systemd/system/sekrun.service << 'EOF'
[Unit]
Description=sek.run Flask Application
After=network.target

[Service]
User=sek3b
Group=sek3b
WorkingDirectory=/var/www/sekrun
Environment="PATH=/var/www/sekrun/venv/bin"
ExecStart=/var/www/sekrun/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
EOF
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable sekrun
sudo systemctl start sekrun
sudo systemctl status sekrun
```

### 8. Configure Nginx

```bash
sudo tee /etc/nginx/sites-available/sekrun << 'EOF'
server {
    listen 80;
    server_name 162.243.107.222 sek.run www.sek.run;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/sekrun/static;
        expires 30d;
    }
}
EOF
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/sekrun /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Configure Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
```

### 10. SSL with Let's Encrypt (Once Domain is Pointed)

After pointing `sek.run` to `162.243.107.222`:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d sek.run -d www.sek.run
```

---

## Useful Commands

```bash
# View logs
sudo journalctl -u sekrun -f

# Restart application
sudo systemctl restart sekrun

# Restart nginx
sudo systemctl restart nginx

# Update application
cd /var/www/sekrun
git pull
sudo systemctl restart sekrun
```

---

## Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Visit `http://127.0.0.1:5000`
