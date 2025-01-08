import pytest
from unittest.mock import patch, MagicMock
import subprocess

from proxy_manager.utils import Utils
from proxy_manager.constants import SERVICE_NAME

@pytest.fixture
def ssh_credentials():
    return {
        'user': 'testuser',
        'host': 'testhost'
    }

@pytest.fixture
def test_port():
    return 8080

def test_check_if_ssh_keys_installed_success(ssh_credentials):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = Utils.check_if_ssh_keys_installed(ssh_credentials['user'], ssh_credentials['host'])
        assert result is True
        mock_run.assert_called_with(["ssh", f"{ssh_credentials['user']}@{ssh_credentials['host']}", "exit"], check=True)

def test_check_if_ssh_keys_installed_failure(ssh_credentials):
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "ssh")
        result = Utils.check_if_ssh_keys_installed(ssh_credentials['user'], ssh_credentials['host'])
        assert result is False

def test_install_ssh_keys_new_installation(ssh_credentials):
    with patch('proxy_manager.utils.Utils.check_if_ssh_keys_installed') as mock_check:
        with patch('subprocess.run') as mock_run:
            mock_check.return_value = False
            Utils.install_ssh_keys(ssh_credentials['user'], ssh_credentials['host'])
            assert mock_run.call_count == 2

def test_install_ssh_keys_existing(ssh_credentials):
    with patch('proxy_manager.utils.Utils.check_if_ssh_keys_installed') as mock_check:
        with patch('subprocess.run') as mock_run:
            mock_check.return_value = True
            Utils.install_ssh_keys(ssh_credentials['user'], ssh_credentials['host'])
            assert mock_run.call_count == 1

def test_check_root_permissions_success():
    with patch('os.geteuid') as mock_geteuid:
        mock_geteuid.return_value = 0
        Utils.check_root_permissions()
        mock_geteuid.assert_called_once()

def test_check_root_permissions_failure():
    with patch('os.geteuid') as mock_geteuid:
        mock_geteuid.return_value = 1000
        with pytest.raises(SystemExit):
            Utils.check_root_permissions()

def test_handle_service_action_success():
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout="success", returncode=0)
        result = Utils.handle_service_action("start")
        assert result == "success"

def test_handle_service_action_failure():
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "systemctl")
        with pytest.raises(SystemExit):
            Utils.handle_service_action("start")

def test_check_port_invalid_range_low():
    with pytest.raises(SystemExit):
        Utils.check_port(999)

def test_check_port_invalid_range_high():
    with pytest.raises(SystemExit):
        Utils.check_port(65536)

def test_check_port_in_use(test_port):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        with pytest.raises(SystemExit):
            Utils.check_port(test_port)

def test_check_port_available(test_port):
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "lsof")
        Utils.check_port(test_port)

def test_remove_service_success():
    with patch('proxy_manager.utils.Utils.handle_service_action') as mock_handle:
        with patch('subprocess.run') as mock_run:
            with patch('os.remove') as mock_remove:
                Utils.remove_service()
                assert mock_handle.call_count == 2
                mock_remove.assert_called_with(f"/etc/systemd/system/{SERVICE_NAME}")
                mock_run.assert_called_with(["systemctl", "daemon-reload"], check=True)

def test_remove_service_file_not_found():
    with patch('proxy_manager.utils.Utils.handle_service_action') as mock_handle:
        with patch('os.remove') as mock_remove:
            mock_remove.side_effect = FileNotFoundError()
            with pytest.raises(SystemExit):
                Utils.remove_service()
