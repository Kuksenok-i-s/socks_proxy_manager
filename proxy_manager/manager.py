import sys
import argparse

from proxy_manager.main_logic import ProxyManager, Utils


def main():

    parser = argparse.ArgumentParser(description="Manage SOCKS proxy service")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    create_parser = subparsers.add_parser("create", help="Create a new proxy service")
    create_parser.add_argument("ssh_user", help="SSH username")
    create_parser.add_argument("ssh_host", help="SSH host")

    update_parser = subparsers.add_parser("update", help="Update proxy service")
    update_parser.add_argument("ssh_user", help="SSH username")
    update_parser.add_argument("ssh_host", help="SSH host")
    update_parser.add_argument("ssh_port", help="SSH port")
    update_parser.add_argument("proxy_port", help="Proxy port")

    subparsers.add_parser("start", help="Start proxy service")
    subparsers.add_parser("stop", help="Stop proxy service")
    subparsers.add_parser("status", help="Check proxy service status")
    subparsers.add_parser("enable", help="Enable proxy service")
    subparsers.add_parser("remove", help="Remove proxy service")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    if args.action == "create":
        if not args.ssh_port:
            args.ssh_port = 22
        pm = ProxyManager(
            args.ssh_user,
            args.ssh_host,
            args.ssh_port,
            local_port=args.proxy_port,
        )
        pm.create_service()
        print("Service created successfully!")
        print("Service name:", pm.service_name)
        print("Service file path:", pm.service_file_path)
        print(f"Service URL: http://localhost:{args.proxy_port}/")
    elif args.action == "update":
        pm = ProxyManager(args.ssh_user, args.ssh_host)
        pm.update_service()
    elif args.action == "remove":
        pm = ProxyManager()
        pm.remove_service()
    elif args.action in ["start", "stop", "status", "enable"]:
        Utils.check_root_permissions()
        print(Utils.handle_service_action(args.action))


if __name__ == "__main__":
    main()
