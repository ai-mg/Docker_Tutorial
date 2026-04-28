# WSL + Ubuntu + Docker Installation Guide

## 1. Install WSL & Ubuntu

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

Restart your computer.

After reboot, Ubuntu will open automatically. Create a username and password when prompted.

## 2. Update Ubuntu

```bash
sudo apt update && sudo apt upgrade -y
```

## 3. Install Docker

```bash
# Add Docker repository
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Run Docker without sudo
sudo usermod -aG docker $USER
newgrp docker
```

## 4. Enable Auto-Start

```bash
echo -e "[boot]\nsystemd=true" | sudo tee /etc/wsl.conf
```

Restart WSL from PowerShell:

```powershell
wsl --shutdown
```

Reopen Ubuntu.

## 5. Verify

```bash
docker run hello-world
```

Done.
