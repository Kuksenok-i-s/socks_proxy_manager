# Description

Socks Proxy Manager is a Python package that provides a simple interface for managing SOCKS proxies systemwide.
It allows you to create, start, stop, and delete SOCKS proxies, as well as view their status.

**Main Use**
access to the remote machine via SSH and manage SOCKS proxies for easier web development.

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
sudo apt install -yqq python3-all dh-python python3-all python3-setuptools python3-pip python3-toml
```

1.1 Install runtime dependencies:

```bash
sudo apt install -yqq python3 openssh-client python3-toml
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


## Usage

**Config file**

```toml
[ssh]
user = "username"
host = "remote.server.com"
port = 22

[proxy]
port = 1080
```

**Commands**

```bash
# Create a new SOCKS proxy
socks-proxy-manager create --config-file config.toml
# Start a SOCKS proxy
socks-proxy-manager start
# Stop a SOCKS proxy
socks-proxy-manager stop
# Delete a SOCKS proxy
socks-proxy-manager remove
# View the status of SOCKS proxies
socks-proxy-manager status
```

**No config file**

```bash
# Create a new SOCKS proxy
socks-proxy-manager create --user username --host remote.server.com --port 22 --proxy-port 1080
# Start a SOCKS proxy
# other commands will  be the same as with a config file
```

**Example output**

```bash
sudo proxy-manager create --config-file config.toml
SSH keys already exist.
Service file created at /etc/systemd/system/socks-proxy.service.
Service created successfully!
Service name: socks-proxy.service
Service file path: /etc/systemd/system/socks-proxy.service
Service URL: localhost:1080
```

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.



## Legal and Ethical Use Disclaimer

**Socks Proxy Manager** is a tool designed to provide a simple interface for managing SOCKS proxies for legitimate purposes, such as enhancing security, managing remote development, or facilitating secure connections **in compliance** with applicable laws.

By using this software, you agree to the following:

1. **Compliance with Laws**: You will use this software in compliance with all applicable local, regional, and national laws. 
It is your responsibility to ensure that your use of this software does not violate any laws or regulations.

2. **Prohibited Use**: This software must not be used to:
   - Circumvent government-imposed restrictions or censorship.
   - Engage in any illegal activities.
   - Interfere with the security or integrity of any system or network.
   - Break network restrictions or bypass network filters.

3. **User Responsibility**: The developer is not responsible for any misuse of this software. Users bear full responsibility for their actions and any consequences thereof.

---

## Additional Notes for Users in Restricted Regions

If you are in a country with strict internet regulations (e.g., blocking unauthorized proxies or VPNs), please check your local laws before using this software.
The use of proxy management tools may be subject to specific legal restrictions. 
Thank you for your understanding and compliance with local laws.
