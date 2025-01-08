from setuptools import setup, find_packages

setup(
    name="socks-proxy-manager",
    version="0.2.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "proxy-manager=proxy_manager.manager:main",
        ]
    },
    install_requires=[],
    description="A tool to manage SOCKS proxy via SSH with systemd.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ilya Kuksenok",
    author_email="kuksyenok.i.s@gmail.com",
    url="https://github.com/yourname/socks-proxy-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)
