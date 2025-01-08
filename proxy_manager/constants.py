SERVICE_NAME = "socks-proxy.service"

SERVICE_FILE_CONTENT = """\
[Unit]
Description=SOCKS Proxy via SSH
After=network.target

[Service]
ExecStart=/usr/bin/ssh -p {ssh_port} -D {port} -q -C -N {ssh_user}@{ssh_host}
Restart=always
User=%u
StandardOutput=null
StandardError=journal
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
"""
