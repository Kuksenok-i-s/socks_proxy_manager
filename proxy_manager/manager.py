import sys
from proxy_manager.main_logic import ProxyManager, Utils
import argparse

def main():

    parser = argparse.ArgumentParser(description='Manage SOCKS proxy service')
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    create_parser = subparsers.add_parser('create', help='Create a new proxy service')
    create_parser.add_argument('ssh_user', help='SSH username')
    create_parser.add_argument('ssh_host', help='SSH host')

    update_parser = subparsers.add_parser('update', help='Update proxy service')
    update_parser.add_argument('ssh_user', help='SSH username')
    update_parser.add_argument('ssh_host', help='SSH host')

    subparsers.add_parser('start', help='Start proxy service')
    subparsers.add_parser('stop', help='Stop proxy service')
    subparsers.add_parser('status', help='Check proxy service status')
    subparsers.add_parser('enable', help='Enable proxy service')
    subparsers.add_parser('remove', help='Remove proxy service')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    if args.action == 'create':
        pm = ProxyManager(args.ssh_user, args.ssh_host)
        pm.create_service()
    elif args.action == 'update':
        pm = ProxyManager(args.ssh_user, args.ssh_host)
        pm.update_service()
    elif args.action == 'remove':
        pm = ProxyManager()
        pm.remove_service()
    elif args.action in ['start', 'stop', 'status', 'enable']:
        Utils.check_root_permissions()
        print(Utils.handle_service_action(args.action))

if __name__ == "__main__":
    main()
