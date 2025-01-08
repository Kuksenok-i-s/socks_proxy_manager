import os
import sys
import subprocess
import socket
import syslog

import logging

from .constants import SERVICE_NAME, SERVICE_FILE_CONTENT


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


class Utils:
    @staticmethod
    def install_ssh_keys(ssh_user, ssh_host) -> None:
        try:
            subprocess.run(["ssh-copy-id", f"{ssh_user}@{ssh_host}"], check=True)
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
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get service {action}.")
            sys.exit(1)

    @staticmethod
    def check_port(port) -> None:
        if port < 1000 or port > 65535:
            logger.error(f"Invalid port number: {port}. Port must be between 1000 and 65535.")
            sys.exit(1)
        try:
            subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, check=True)
            logger.error(f"Port {port} is already in use.")
            sys.exit(1)
        except subprocess.CalledProcessError:
            pass


class ProxyManager:
    def __init__(
        self,
        ssh_user: str = None,
        ssh_host: str = None,
        local_port: int = 22054,
        ssh_port: int = 22,
    ):
        Utils.check_root_permissions()
        Utils.check_port(local_port)
        Utils.install_ssh_keys(ssh_user, ssh_host)
        self.service_name = SERVICE_NAME
        self.service_file_path = f"/etc/systemd/system/{self.service_name}"
        self.port = local_port
        self.ssh_user = ssh_user
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port

    def create_service(self) -> None:
        service_file_path = f"/etc/systemd/system/{SERVICE_NAME}"
        content = SERVICE_FILE_CONTENT.format(
            ssh_user=self.ssh_user,
            ssh_host=self.ssh_host,
            ssh_port=self.ssh_port,
            port=self.port,
        )

        try:
            with open(service_file_path, "w", encoding="utf-8") as service_file:
                service_file.write(content)
            logger.info(f"Service file created at {service_file_path}.")
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            Utils.handle_service_action("enable")
            Utils.handle_service_action("start")
        except Exception as e:
            logger.error(f"Error creating service: {e}")
            sys.exit(1)

    @staticmethod
    def remove_service() -> None:
        try:
            Utils.handle_service_action("stop")
            Utils.handle_service_action("disable")
            os.remove(f"/etc/systemd/system/{SERVICE_NAME}")
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            logger.info(f"Service {SERVICE_NAME} removed.")
        except subprocess.CalledProcessError:
            logger.error(f"Failed to remove the service. Check the logs.")
            sys.exit(1)
        except FileNotFoundError:
            logger.error(f"Service file {SERVICE_NAME} not found. Continue.")
        except Exception as e:
            logger.error(f"Error removing service: {e}")
            sys.exit(1)

    def update_service(self) -> None:
        self.remove_service()
        self.create_service()
        Utils.handle_service_action("enable")
        Utils.handle_service_action("start")
        logger.info("Service updated.")
