# Step-by-Step Guide: Installing WSL → Ubuntu → Docker on Windows

---

## Part 1: Installing WSL (Windows Subsystem for Linux)

### Prerequisites

- Windows 10 (version 2004+, Build 19041+) or Windows 11
- Administrator access

### Step 1: Open PowerShell as Administrator

- Right-click the **Start** button
- Select **Terminal (Admin)** or **Windows PowerShell (Admin)**
- Click **Yes** on the UAC prompt

### Step 2: Install WSL

Run the following command:

```powershell
wsl --install
```

This single command will:

- ✅ Enable the **Virtual Machine Platform** feature
- ✅ Enable the **Windows Subsystem for Linux** feature
- ✅ Download and install the latest Linux kernel
- ✅ Set **WSL 2** as the default version
- ✅ Download and install **Ubuntu** (by default)

### Step 3: Restart Your Computer

```powershell
shutdown /r /t 0
```

A restart is **required** to complete the installation.

### Step 4: Verify WSL Installation

After reboot, open PowerShell again and run:

```powershell
wsl --status
```

You should see WSL 2 listed as the default version. You can also check available distros:

```powershell
wsl --list --verbose
```

---

## Part 2: Setting Up Ubuntu

### Step 5: Launch Ubuntu

- After restart, Ubuntu may **auto-launch** and begin setup
- If not, search for **"Ubuntu"** in the Start menu and open it
- Alternatively, type `wsl` in PowerShell

### Step 6: Create Your Linux User Account

Ubuntu will prompt you to:

1. **Enter a new UNIX username** — pick something simple (lowercase, no spaces)
2. **Enter a new password** — this is your `sudo` password (you won't see characters as you type — that's normal)
3. **Confirm the password**

### Step 7: Update Ubuntu Packages

Always update first:

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 8: (Optional) Install a Specific Ubuntu Version

If you want a different Ubuntu version instead of the default:

```powershell
# List available distros
wsl --list --online

# Install a specific one (e.g., Ubuntu 24.04)
wsl --install -d Ubuntu-24.04
```

---

## Part 3: Installing Docker Inside WSL/Ubuntu

You have **two options** here. Choose the one that fits your needs:

---

### Option A: Docker Desktop for Windows (Recommended for Beginners)

This gives you a GUI and seamless WSL 2 integration.

#### Step 9A: Download Docker Desktop

1. Go to [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Download the **Windows** installer

#### Step 10A: Install Docker Desktop

1. Run the `.exe` installer
2. During setup, ensure **"Use WSL 2 instead of Hyper-V"** is ✅ checked
3. Click **OK** and let the installation complete
4. **Restart** your computer if prompted

#### Step 11A: Configure Docker Desktop for WSL

1. Open **Docker Desktop**
2. Go to **Settings** (⚙️ gear icon)
3. Navigate to **Resources → WSL Integration**
4. Toggle on your Ubuntu distro
5. Click **Apply & Restart**

#### Step 12A: Verify in Ubuntu

Open your Ubuntu terminal and run:

```bash
docker --version
docker run hello-world
```

You should see a success message from the `hello-world` container. 🎉

---

### Option B: Docker Engine Directly in Ubuntu (No Docker Desktop)

This is a lightweight, CLI-only approach — great for developers and servers.

#### Step 9B: Remove Old Docker Packages (if any)

```bash
sudo apt remove docker docker-engine docker.io containerd runc 2>/dev/null
```

#### Step 10B: Install Prerequisites

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release
```

#### Step 11B: Add Docker's Official GPG Key

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

#### Step 12B: Add Docker Repository

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### Step 13B: Install Docker Engine

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Step 14B: Start Docker Service

WSL doesn't use `systemd` by default, so start Docker manually:

```bash
sudo service docker start
```

> **💡 Tip:** To enable `systemd` (so Docker auto-starts), edit `/etc/wsl.conf`:
>
> ```bash
> sudo nano /etc/wsl.conf
> ```
>
> Add:
>
> ```ini
> [boot]
> systemd=true
> ```
>
> Then restart WSL from PowerShell: `wsl --shutdown` and reopen Ubuntu.

#### Step 15B: Add Your User to the Docker Group

This lets you run `docker` without `sudo`:

```bash
sudo usermod -aG docker $USER
```

Then **close and reopen** your Ubuntu terminal (or run `newgrp docker`).

#### Step 16B: Verify Installation

```bash
docker --version
docker compose version
docker run hello-world
```

You should see output like:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## 🧪 Quick Sanity Check (Both Options)

Run these commands to confirm everything works end-to-end:

| Command                       | Expected Result                        |
| ----------------------------- | -------------------------------------- |
| `wsl --list --verbose`        | Shows Ubuntu running on WSL 2          |
| `docker --version`            | Shows Docker version (e.g., 27.x)     |
| `docker compose version`      | Shows Compose version (e.g., 2.x)     |
| `docker run hello-world`      | Prints success message                 |
| `docker run -it ubuntu bash`  | Drops you into an Ubuntu container     |

---

## 🔧 Common Troubleshooting

| Issue                              | Solution                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------ |
| **WSL install fails**              | Ensure virtualization is enabled in BIOS/UEFI (Intel VT-x / AMD-V)      |
| **"WSL 2 requires an update"**     | Run `wsl --update` in PowerShell                                         |
| **Docker daemon not running**      | Run `sudo service docker start` or enable systemd                        |
| **Permission denied on docker**    | Run `sudo usermod -aG docker $USER` then restart terminal                |
| **Slow file performance**          | Store project files inside WSL (`/home/user/`) not on `/mnt/c/`          |

---

You're all set! You now have a full **WSL 2 + Ubuntu + Docker** development environment on Windows. 🚀
