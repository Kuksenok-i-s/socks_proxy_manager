# Description

Socks Proxy Manager is a Python package that provides a simple interface for managing SOCKS proxies systemwide.
It allows you to create, start, stop, and delete SOCKS proxies, as well as view their status.

**Main features:**

- Create SOCKS proxies with custom configurations.
- Start, stop, and delete SOCKS proxies.
- View the status of SOCKS proxies.
- Manage SOCKS proxies using a simple command-line interface.

## Setup

### Prerequisites

- Python 3.9 or higher
- OpenSSH client

You should have a working SSH server running on the remote machine, and please make sure that you have generated openSSH keys on your local machine, this can be done with the following command:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**ATTENTION:** __ssh-keygen__ will overwrite the existing SSH keys on your local machine!!!


## Under the hood

- Uses Systemd services for managing SOCKS proxies.

## Building from source

### Python package

1. Clone the repository:

```bash
git clone https://github.com/Kuksenok-i-s/socks_proxy_manager.git
cd socks_proxy_manager
```

2. Make venv active and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Debian package

1. Install build dependencies:

```bash
sudo apt update -yqq
sudo apt install -yqq openssh-client
sudo apt install -yqq  build-essential devscripts debhelper
sudo apt install -yqq python3-all dh-python python3-all python3-setuptools python3-pip
```

2. Clone the repository:

```bash
git clone https://github.com/Kuksenok-i-s/socks_proxy_manager.git
cd socks_proxy_manager
```

3. Build the package:

```bash
debuild -us -uc
```

4. Install the generated .deb package:

```bash
sudo dpkg -i ../socks-proxy-manager_*.deb
sudo apt-get install -f
```