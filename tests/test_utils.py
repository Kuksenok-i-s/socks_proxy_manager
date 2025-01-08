import pytest
import subprocess
from unittest.mock import patch, MagicMock
from proxy_manager.main_logic import Utils
from proxy_manager.constants import SERVICE_NAME

def test_install_ssh_keys_success():
    with patch('subprocess.run') as mock_run:
        Utils.install_ssh_keys('testuser', 'testhost')
        mock_run.assert_called_once_with(['ssh-copy-id', 'testuser@testhost'], check=True)

def test_install_ssh_keys_failure():
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
        with pytest.raises(SystemExit):
            Utils.install_ssh_keys('testuser', 'testhost')

def test_check_root_permissions_as_root():
    with patch('os.geteuid', return_value=0):
        Utils.check_root_permissions()

def test_check_root_permissions_as_non_root():
    with patch('os.geteuid', return_value=1000):
        with pytest.raises(SystemExit):
            Utils.check_root_permissions()

def test_handle_service_action_success():
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout='success')
        result = Utils.handle_service_action('start')
        assert result == 'success'
        mock_run.assert_called_once_with(['systemctl', 'start', SERVICE_NAME], 
                                       capture_output=True, text=True, check=True)

def test_handle_service_action_failure():
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd', stderr=b'error')
        with pytest.raises(SystemExit):
            Utils.handle_service_action('start')

def test_check_port_invalid_range():
    with pytest.raises(SystemExit):
        Utils.check_port(500)
    with pytest.raises(SystemExit):
        Utils.check_port(70000)

def test_check_port_available():
    with patch('socket.socket') as mock_socket:
        mock_instance = MagicMock()
        mock_instance.connect_ex.return_value = 1
        mock_socket.return_value = mock_instance
        Utils.check_port(28080)
