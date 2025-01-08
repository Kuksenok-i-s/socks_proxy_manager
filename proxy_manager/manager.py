import sys
import argparse


from proxy_manager.main_logic import ProxyManager, Utils
from proxy_manager.utils import Config, logger


def pm_init(args) -> tuple[ProxyManager, int]:
    if args.config_file:
        config = Config(args.config_file)
        proxy_port = config.local_port
        return ProxyManager(**config.get_config()), proxy_port

    return ProxyManager(
        ssh_host=args.ssh_host,
        ssh_user=args.ssh_user,
        local_port=args.proxy_port,
        ssh_port=args.ssh_port,
    )


def main():

    parser = argparse.ArgumentParser(description="Manage SOCKS proxy service")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    create_parser = subparsers.add_parser("create", help="Create a new proxy service")
    create_parser.add_argument("--config-file", help="Path to the TOML config file")
    create_parser.add_argument("--user", dest="ssh_user", help="SSH username")
    create_parser.add_argument("--host", dest="ssh_host", help="SSH host")
    create_parser.add_argument("--port", dest="ssh_port", type=int, help="SSH port", default=22)
    create_parser.add_argument("--proxy-port", dest="proxy_port", type=int, help="Proxy port")

    update_parser = subparsers.add_parser("update", help="Update proxy service")
    update_parser.add_argument("--config-file", help="Path to the TOML config file")
    update_parser.add_argument("--user", dest="ssh_user", help="SSH username")
    update_parser.add_argument("--host", dest="ssh_host", help="SSH host")
    update_parser.add_argument("--port", dest="ssh_port", type=int, help="SSH port", default=22)
    update_parser.add_argument("--proxy-port", dest="proxy_port", type=int, help="Proxy port")

    subparsers.add_parser("start", help="Start proxy service")
    subparsers.add_parser("stop", help="Stop proxy service")
    subparsers.add_parser("status", help="Check proxy service status")
    subparsers.add_parser("enable", help="Enable proxy service")
    subparsers.add_parser("disable", help="Disable proxy service")
    subparsers.add_parser("remove", help="Remove proxy service")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    if args.action == "create":
        pm = pm_init(args)
        pm[0].create_service()
        logger.info("Service created successfully!")
        logger.info(f"Service name: {pm[0].service_name}")
        logger.info(f"Service file path: {pm[0].service_file_path}")
        logger.info(f"Service URL: localhost:{pm[1]}")
    elif args.action == "update":
        pm = pm_init(args)
        pm[0].update_service()
        logger.info("Service updated successfully!")
        logger.info(f"Service name: {pm[0].service_name}")
        logger.info(f"Service file path: {pm[0].service_file_path}")
        logger.info(f"Service URL: localhost:{pm[1]}")
    elif args.action == "remove":
        Utils.remove_service()
    elif args.action in ["start", "stop", "status", "enable", "disable"]:
        Utils.check_root_permissions()
        print(Utils.handle_service_action(args.action))


if __name__ == "__main__":
    main()
