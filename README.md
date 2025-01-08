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


## Legal and Ethical Use Disclaimer

**Socks Proxy Manager** is a tool designed to provide a simple interface for managing SOCKS proxies for legitimate purposes, such as enhancing security, managing private networks, or facilitating secure connections in compliance with applicable laws.

By using this software, you agree to the following:

1. **Compliance with Laws**: You will use this software in compliance with all applicable local, regional, and national laws. It is your responsibility to ensure that your use of this software does not violate any laws or regulations.

2. **Prohibited Use**: This software must not be used to:
   - Circumvent government-imposed restrictions or censorship.
   - Engage in any illegal activities.

3. **User Responsibility**: The developer is not responsible for any misuse of this software. Users bear full responsibility for their actions and any consequences thereof.

---

## Additional Notes for Users in Restricted Regions

If you are in a country with strict internet regulations (e.g., blocking unauthorized proxies or VPNs), please check your local laws before using this software. The use of proxy management tools may be subject to specific legal restrictions.
