import sys
import subprocess

from .utils import Utils, logger
from .constants import SERVICE_NAME, SERVICE_FILE_CONTENT


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

    def update_service(self) -> None:
        Utils.remove_service()
        self.create_service()
        Utils.handle_service_action("enable")
        Utils.handle_service_action("start")
        logger.info("Service updated.")
