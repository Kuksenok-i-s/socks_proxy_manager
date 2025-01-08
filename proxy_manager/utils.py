import logging
import subprocess
import sys
import syslog
import os
import toml

from proxy_manager.constants import SERVICE_NAME


class SysLogHandler(logging.Handler):
    def __init__(self, ident="PROXY_MANAGER"):
        super().__init__()
        self.ident = ident
        syslog.openlog(ident=self.ident, facility=syslog.LOG_LOCAL0)

    def emit(self, record):
        msg = self.format(record)
        syslog.syslog(msg)

    def close(self):
        syslog.closelog()
        super().close()


logger = logging.getLogger("proxy_manager")
logger.setLevel(logging.INFO)

syslog_handler = SysLogHandler()
logger.addHandler(syslog_handler)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
logger.addHandler(stdout_handler)


class Config:
    def __init__(self, config_file: str = "config.toml"):
        self.config = toml.load(config_file)
        self.ssh_user = self.config.get("ssh", {}).get("user")
        self.ssh_host = self.config.get("ssh", {}).get("host")
        try:
            self.ssh_port = int(self.config.get("ssh", {}).get("port"))
            self.local_port = int(self.config.get("proxy", {}).get("port"))
        except ValueError as error:
            raise ValueError(f"Invalid configuration: {error}") from error

    def get_config(self):
        return {
            "ssh_user": self.ssh_user,
            "ssh_host": self.ssh_host,
            "ssh_port": self.ssh_port,
            "local_port": self.local_port,
        }

    def check_config(self) -> bool:
        return any(
            [
                not self.ssh_user,
                not self.ssh_host,
                not self.ssh_port,
                not self.local_port,
            ]
        )


class Utils:
    @staticmethod
    def check_if_ssh_keys_installed(ssh_user, ssh_host) -> bool:
        try:
            subprocess.run(["ssh", f"{ssh_user}@{ssh_host}", "exit"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def install_ssh_keys(ssh_user, ssh_host) -> None:
        try:
            if not Utils.check_if_ssh_keys_installed(ssh_user, ssh_host):
                logger.info("SSH keys not found. Installing...")
                subprocess.run(["ssh-keygen", "-t", "ed25519", "-f", "~/.ssh/id_ed25519"], check=True)
                logger.info("SSH keys installed successfully.")
            else:
                logger.info("SSH keys already exist.")
            subprocess.run(["ssh-copy-id", f"{ssh_user}@{ssh_host}"], check=True, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            logger.error(f"Failed to install SSH keys for {ssh_user}@{ssh_host}.")
            sys.exit(1)

    @staticmethod
    def check_root_permissions() -> None:
        if os.geteuid() != 0:
            logger.error("This script must run as root.")
            print("Please run this script as root.")
            sys.exit(1)

    @staticmethod
    def handle_service_action(action: str) -> str:
        try:
            result = subprocess.run(
                ["systemctl", action, SERVICE_NAME],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            logger.error(f"Failed to {action} service {SERVICE_NAME}.")
            sys.exit(1)

    @staticmethod
    def check_port(port) -> None:
        if isinstance(port, str):
            port = int(port)
        if port < 1000 or port > 65535:
            logger.error(f"Invalid port number: {port}. Port must be between 1000 and 65535.")
            sys.exit(1)
        try:
            subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, check=True)
            logger.error(f"Port {port} is already in use.")
            sys.exit(1)
        except subprocess.CalledProcessError:
            pass

    @classmethod
    def remove_service(cls) -> None:
        try:
            cls.handle_service_action("stop")
            cls.handle_service_action("disable")
            os.remove(f"/etc/systemd/system/{SERVICE_NAME}")
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            logger.info(f"Service {SERVICE_NAME} removed.")
        except subprocess.CalledProcessError:
            logger.error(f"Failed to remove the service. Check the logs.")
            sys.exit(1)
        except FileNotFoundError:
            logger.error(f"Service file {SERVICE_NAME} not found. Continue.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Error removing service: {e}")
            sys.exit(1)
