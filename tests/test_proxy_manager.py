import pytest
from unittest.mock import patch, mock_open, MagicMock
from proxy_manager.main_logic import ProxyManager, Utils
from proxy_manager.constants import SERVICE_NAME, SERVICE_FILE_CONTENT

@pytest.fixture
def proxy_manager():
    with patch.object(Utils, 'check_root_permissions'), \
         patch.object(Utils, 'check_port'), \
         patch.object(Utils, 'install_ssh_keys'):
        return ProxyManager('testuser', 'testhost')

def test_proxy_manager_init():
    with patch.object(Utils, 'check_root_permissions') as mock_root, \
         patch.object(Utils, 'check_port') as mock_port, \
         patch.object(Utils, 'install_ssh_keys') as mock_ssh:
        
        pm = ProxyManager('testuser', 'testhost')
        
        assert pm.ssh_user == 'testuser'
        assert pm.ssh_host == 'testhost'
        assert pm.port == 22054
        assert pm.ssh_port == 22
        assert pm.service_name == SERVICE_NAME
        
        mock_root.assert_called_once()
        mock_port.assert_called_once_with(22054)
        mock_ssh.assert_called_once_with('testuser', 'testhost')

def test_create_service_success(proxy_manager):
    mock_file = mock_open()
    with patch('builtins.open', mock_file), \
         patch('subprocess.run') as mock_run, \
         patch.object(Utils, 'handle_service_action') as mock_handle:
        
        proxy_manager.create_service()
        
        expected_content = SERVICE_FILE_CONTENT.format(
            ssh_user='testuser',
            ssh_host='testhost',
            ssh_port=22,
            port=22054
        )
        mock_file().write.assert_called_once_with(expected_content)
        mock_run.assert_called_once_with(['systemctl', 'daemon-reload'], check=True)
        assert mock_handle.call_count == 2

def test_create_service_failure(proxy_manager):
    with patch('builtins.open', side_effect=Exception('Test error')), \
         patch('sys.exit') as mock_exit:
        
        proxy_manager.create_service()
        mock_exit.assert_called_once_with(1)

def test_remove_service_success():
    with patch.object(Utils, 'handle_service_action') as mock_handle, \
         patch('os.remove') as mock_remove, \
         patch('subprocess.run') as mock_run:
        
        ProxyManager.remove_service()
        
        assert mock_handle.call_count == 2
        mock_remove.assert_called_once_with(f'/etc/systemd/system/{SERVICE_NAME}')
        mock_run.assert_called_once_with(['systemctl', 'daemon-reload'], check=True)

def test_remove_service_file_not_found():
    with patch.object(Utils, 'handle_service_action'), \
         patch('os.remove', side_effect=FileNotFoundError):
        
        ProxyManager.remove_service()

def test_update_service(proxy_manager):
    with patch.object(ProxyManager, 'remove_service') as mock_remove, \
         patch.object(ProxyManager, 'create_service') as mock_create, \
         patch.object(Utils, 'handle_service_action') as mock_handle:
        
        proxy_manager.update_service()
        
        mock_remove.assert_called_once()
        mock_create.assert_called_once()
        assert mock_handle.call_count == 2
