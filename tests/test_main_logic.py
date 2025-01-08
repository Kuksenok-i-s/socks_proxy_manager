import pytest
from unittest.mock import patch, mock_open
from proxy_manager.main_logic import ProxyManager
from proxy_manager.constants import SERVICE_NAME, SERVICE_FILE_CONTENT

@pytest.fixture
def proxy_manager_params():
    return {
        'ssh_user': 'testuser',
        'ssh_host': 'testhost',
        'local_port': 22054,
        'ssh_port': 22
    }

@pytest.fixture
def proxy_manager(proxy_manager_params):
    with patch('proxy_manager.main_logic.Utils') as mock_utils:
        manager = ProxyManager(**proxy_manager_params)
        yield manager, mock_utils

def test_init_validates_requirements(proxy_manager_params):
    with patch('proxy_manager.main_logic.Utils') as mock_utils:
        manager = ProxyManager(**proxy_manager_params)
        
        mock_utils.check_root_permissions.assert_called_once()
        mock_utils.check_port.assert_called_once_with(proxy_manager_params['local_port'])
        mock_utils.install_ssh_keys.assert_called_once_with(
            proxy_manager_params['ssh_user'], 
            proxy_manager_params['ssh_host']
        )

def test_init_sets_attributes(proxy_manager):
    manager, _ = proxy_manager
    assert manager.ssh_user == 'testuser'
    assert manager.ssh_host == 'testhost'
    assert manager.port == 22054
    assert manager.ssh_port == 22
    assert manager.service_name == SERVICE_NAME
    assert manager.service_file_path == f"/etc/systemd/system/{SERVICE_NAME}"

def test_create_service_success(proxy_manager):
    manager, mock_utils = proxy_manager
    
    with patch('builtins.open', new_callable=mock_open) as mock_file, \
         patch('proxy_manager.main_logic.subprocess.run') as mock_run:
        
        manager.create_service()
        
        expected_content = SERVICE_FILE_CONTENT.format(
            ssh_user='testuser',
            ssh_host='testhost',
            ssh_port=22,
            port=22054
        )
        
        mock_file.assert_called_once_with(f"/etc/systemd/system/{SERVICE_NAME}", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with(expected_content)
        mock_run.assert_called_once_with(["systemctl", "daemon-reload"], check=True)
        assert mock_utils.handle_service_action.call_count == 2

def test_create_service_handles_errors(proxy_manager):
    manager, _ = proxy_manager
    
    with patch('builtins.open', mock_open()) as mock_file, \
         pytest.raises(SystemExit):
        mock_file.side_effect = Exception("Failed to write service file")
        manager.create_service()

def test_update_service_flow(proxy_manager):
    manager, mock_utils = proxy_manager
    
    with patch.object(manager, 'create_service') as mock_create:
        manager.update_service()
        
        mock_utils.remove_service.assert_called_once()
        mock_create.assert_called_once()
        assert mock_utils.handle_service_action.call_count == 2

def test_update_service_enables_and_starts(proxy_manager):
    manager, mock_utils = proxy_manager
    
    with patch.object(manager, 'create_service'):
        manager.update_service()
        
        mock_utils.handle_service_action.assert_any_call("enable")
        mock_utils.handle_service_action.assert_any_call("start")
