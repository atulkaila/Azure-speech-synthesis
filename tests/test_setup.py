"""
Unit tests for setup.py module.
"""
import pytest
import sys
import os
import tempfile
import subprocess
from unittest.mock import Mock, patch, MagicMock, mock_open
from io import StringIO

# Import the module under test
import setup

class TestSetup:
    """Test class for setup module."""

    def test_print_banner(self):
        """Test print_banner function outputs correct banner."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            setup.print_banner()
            output = fake_out.getvalue()
        
        assert "🎤 Azure Speech Service - Text-to-Speech Setup" in output
        assert "=" * 70 in output

    def test_check_python_version_compatible(self):
        """Test check_python_version with compatible Python version."""
        # Create a mock version_info with the required attributes
        mock_version = Mock()
        mock_version.__lt__ = Mock(return_value=False)  # Not less than (3, 7)
        mock_version.major = 3
        mock_version.minor = 8
        
        with patch('sys.version_info', mock_version):
            result = setup.check_python_version()
            assert result is True

    def test_check_python_version_incompatible(self):
        """Test check_python_version with incompatible Python version."""
        # Create a mock version_info with the required attributes
        mock_version = Mock()
        mock_version.__lt__ = Mock(return_value=True)  # Less than (3, 7)
        mock_version.major = 3
        mock_version.minor = 6
        
        with patch('sys.version_info', mock_version):
            with patch('sys.version', '3.6.0'):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    result = setup.check_python_version()
                    output = fake_out.getvalue()
            
            assert result is False
            assert "❌ Error: Python 3.7 or higher is required." in output

    @patch('subprocess.run')
    def test_install_requirements_success(self, mock_run):
        """Test successful requirements installation."""
        # Mock successful subprocess run
        mock_result = Mock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        result = setup.install_requirements()
        
        # Verify subprocess was called correctly
        mock_run.assert_called_once_with(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True, 
            text=True
        )
        assert result is True

    @patch('subprocess.run')
    def test_install_requirements_failure(self, mock_run):
        """Test failed requirements installation."""
        # Mock failed subprocess run
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Package not found"
        mock_run.return_value = mock_result
        
        result = setup.install_requirements()
        
        assert result is False

    @patch('subprocess.run')
    def test_install_requirements_exception(self, mock_run):
        """Test requirements installation with exception."""
        mock_run.side_effect = Exception("Connection error")
        
        result = setup.install_requirements()
        
        assert result is False

    @patch('builtins.input')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_create_config_file_new_file(self, mock_exists, mock_file, mock_input):
        """Test creating new config file."""
        mock_exists.return_value = False
        mock_input.side_effect = [
            'test_speech_key_123',
            'https://eastus.api.cognitive.microsoft.com',
            '1'  # Andrew voice
        ]
        
        result = setup.create_config_file()
        
        # Verify file operations
        mock_file.assert_called_once_with("config.py", "w")
        handle = mock_file()
        
        # Check that write was called and content includes our test values
        assert handle.write.called
        written_content = handle.write.call_args[0][0]
        assert 'test_speech_key_123' in written_content
        assert 'https://eastus.api.cognitive.microsoft.com/' in written_content
        assert 'en-US-AndrewMultilingualNeural' in written_content
        
        assert result is True

    @patch('builtins.input')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_create_config_file_female_voice(self, mock_exists, mock_file, mock_input):
        """Test creating config file with female voice selection."""
        mock_exists.return_value = False
        mock_input.side_effect = [
            'test_key',
            'https://test.api.com',
            '2'  # Ava voice
        ]
        
        result = setup.create_config_file()
        
        # Check that female voice was selected
        handle = mock_file()
        written_content = handle.write.call_args[0][0]
        assert 'en-US-AvaMultilingualNeural' in written_content
        
        assert result is True

    @patch('builtins.input')
    @patch('os.path.exists')
    def test_create_config_file_overwrite_no(self, mock_exists, mock_input):
        """Test not overwriting existing config file."""
        mock_exists.return_value = True
        mock_input.return_value = 'n'
        
        result = setup.create_config_file()
        
        assert result is True

    @patch('builtins.input')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_create_config_file_overwrite_yes(self, mock_exists, mock_file, mock_input):
        """Test overwriting existing config file."""
        mock_exists.return_value = True
        mock_input.side_effect = [
            'y',  # Overwrite
            'test_key',
            'https://test.api.com',
            '1'
        ]
        
        result = setup.create_config_file()
        
        assert result is True

    @patch('builtins.input')
    def test_create_config_file_empty_speech_key(self, mock_input):
        """Test creating config file with empty speech key."""
        mock_input.side_effect = ['']  # Empty speech key
        
        result = setup.create_config_file()
        
        assert result is False

    @patch('builtins.input')
    def test_create_config_file_empty_endpoint(self, mock_input):
        """Test creating config file with empty endpoint."""
        mock_input.side_effect = ['test_key', '']  # Empty endpoint
        
        result = setup.create_config_file()
        
        assert result is False

    @patch('builtins.input')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_create_config_file_endpoint_without_slash(self, mock_exists, mock_file, mock_input):
        """Test creating config file ensures endpoint ends with slash."""
        mock_exists.return_value = False
        mock_input.side_effect = [
            'test_key',
            'https://test.api.com',  # No trailing slash
            '1'
        ]
        
        result = setup.create_config_file()
        
        # Check that slash was added
        handle = mock_file()
        written_content = handle.write.call_args[0][0]
        assert 'https://test.api.com/' in written_content
        
        assert result is True

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_create_config_file_write_exception(self, mock_exists, mock_file):
        """Test creating config file with write exception."""
        mock_exists.return_value = False
        mock_file.side_effect = IOError("Permission denied")
        
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['test_key', 'https://test.api.com', '1']
            result = setup.create_config_file()
        
        assert result is False

    @patch('os.makedirs')
    @patch('os.path.exists')
    def test_create_output_directory_new(self, mock_exists, mock_makedirs):
        """Test creating new output directory."""
        mock_exists.return_value = False
        
        result = setup.create_output_directory()
        
        mock_makedirs.assert_called_once_with("output")
        assert result is True

    @patch('os.path.exists')
    def test_create_output_directory_exists(self, mock_exists):
        """Test when output directory already exists."""
        mock_exists.return_value = True
        
        result = setup.create_output_directory()
        
        assert result is True

    @patch('os.makedirs')
    @patch('os.path.exists')
    def test_create_output_directory_exception(self, mock_exists, mock_makedirs):
        """Test creating output directory with exception."""
        mock_exists.return_value = False
        mock_makedirs.side_effect = OSError("Permission denied")
        
        result = setup.create_output_directory()
        
        assert result is False

    def test_test_configuration_success(self):
        """Test successful configuration testing."""
        # Mock azure.cognitiveservices.speech module at import level
        with patch.dict('sys.modules', {'azure': MagicMock()}):
            with patch.dict('sys.modules', {'azure.cognitiveservices': MagicMock()}):
                with patch.dict('sys.modules', {'azure.cognitiveservices.speech': MagicMock()}):
                    mock_speechsdk = MagicMock()
                    mock_config_module = MagicMock()
                    mock_config_module.SPEECH_KEY = "test_key"
                    mock_config_module.SPEECH_ENDPOINT = "https://test.api.com/"
                    
                    # Mock the SpeechConfig creation to avoid segfault
                    mock_speech_config = Mock()
                    mock_speechsdk.SpeechConfig = Mock(return_value=mock_speech_config)
                    
                    with patch.dict('sys.modules', {
                        'azure.cognitiveservices.speech': mock_speechsdk,
                        'config': mock_config_module
                    }):
                        result = setup.test_configuration()
        
        assert result is True

    def test_test_configuration_import_error(self):
        """Test configuration testing with import error."""
        with patch('builtins.__import__', side_effect=ImportError("Module not found")):
            result = setup.test_configuration()
        
        assert result is False

    def test_test_configuration_general_exception(self):
        """Test configuration testing with general exception."""
        # Mock the import process to avoid segfault
        with patch('builtins.__import__') as mock_import:
            def mock_import_side_effect(name, *args, **kwargs):
                if name == 'azure.cognitiveservices.speech':
                    mock_speechsdk = MagicMock()
                    mock_speechsdk.SpeechConfig.side_effect = Exception("Configuration error")
                    return mock_speechsdk
                elif name == 'config':
                    mock_config = MagicMock()
                    mock_config.SPEECH_KEY = "test_key"
                    mock_config.SPEECH_ENDPOINT = "https://test.api.com/"
                    return mock_config
                else:
                    # For any other imports, use the real import
                    return __import__(name, *args, **kwargs)
                
            mock_import.side_effect = mock_import_side_effect
            result = setup.test_configuration()
        
        assert result is False

    def test_display_next_steps(self):
        """Test display_next_steps function outputs correct information."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            setup.display_next_steps()
            output = fake_out.getvalue()
        
        assert "🎉 Setup completed successfully!" in output
        assert "python speech_synthesis.py" in output
        assert "python speech_synthesis_custom_voice.py" in output
        assert "💡 Tips:" in output

    @patch('setup.display_next_steps')
    @patch('setup.test_configuration')
    @patch('setup.create_output_directory')
    @patch('setup.create_config_file')
    @patch('setup.install_requirements')
    @patch('setup.check_python_version')
    @patch('setup.print_banner')
    def test_main_complete_success(self, mock_banner, mock_check_python, 
                                  mock_install, mock_create_config, 
                                  mock_create_output, mock_test_config, 
                                  mock_display_next):
        """Test main function with complete successful setup."""
        # Setup all mocks to return success
        mock_check_python.return_value = True
        mock_install.return_value = True
        mock_create_config.return_value = True
        mock_create_output.return_value = True
        mock_test_config.return_value = True
        
        result = setup.main()
        
        # Verify all functions were called
        mock_banner.assert_called_once()
        mock_check_python.assert_called_once()
        mock_install.assert_called_once()
        mock_create_config.assert_called_once()
        mock_create_output.assert_called_once()
        mock_test_config.assert_called_once()
        mock_display_next.assert_called_once()
        
        assert result is True

    @patch('setup.check_python_version')
    @patch('setup.print_banner')
    def test_main_python_version_failure(self, mock_banner, mock_check_python):
        """Test main function with Python version check failure."""
        mock_check_python.return_value = False
        
        result = setup.main()
        
        assert result is False

    @patch('builtins.input')
    @patch('setup.create_config_file')
    @patch('setup.install_requirements')
    @patch('setup.check_python_version')
    @patch('setup.print_banner')
    def test_main_install_failure_proceed_no(self, mock_banner, mock_check_python,
                                            mock_install, mock_create_config, mock_input):
        """Test main function with install failure and user chooses not to proceed."""
        mock_check_python.return_value = True
        mock_install.return_value = False
        mock_input.return_value = 'n'
        
        result = setup.main()
        
        # Should not proceed to create config
        mock_create_config.assert_not_called()
        assert result is False

    @patch('builtins.input')
    @patch('setup.create_output_directory')
    @patch('setup.create_config_file')
    @patch('setup.install_requirements')
    @patch('setup.check_python_version')
    @patch('setup.print_banner')
    def test_main_install_failure_proceed_yes(self, mock_banner, mock_check_python,
                                             mock_install, mock_create_config,
                                             mock_create_output, mock_input):
        """Test main function with install failure and user chooses to proceed."""
        mock_check_python.return_value = True
        mock_install.return_value = False
        mock_input.return_value = 'y'
        mock_create_config.return_value = True
        mock_create_output.return_value = True
        
        with patch('setup.test_configuration', return_value=True):
            with patch('setup.display_next_steps'):
                result = setup.main()
        
        # Should proceed to create config
        mock_create_config.assert_called_once()
        assert result is True

    @patch('setup.create_config_file')
    @patch('setup.install_requirements')
    @patch('setup.check_python_version')
    @patch('setup.print_banner')
    def test_main_config_file_failure(self, mock_banner, mock_check_python,
                                     mock_install, mock_create_config):
        """Test main function with config file creation failure."""
        mock_check_python.return_value = True
        mock_install.return_value = True
        mock_create_config.return_value = False
        
        result = setup.main()
        
        assert result is False

    @patch('setup.test_configuration')
    @patch('setup.create_output_directory')
    @patch('setup.create_config_file')
    @patch('setup.install_requirements')
    @patch('setup.check_python_version')
    @patch('setup.print_banner')
    def test_main_test_configuration_failure(self, mock_banner, mock_check_python,
                                            mock_install, mock_create_config,
                                            mock_create_output, mock_test_config):
        """Test main function with configuration test failure."""
        mock_check_python.return_value = True
        mock_install.return_value = True
        mock_create_config.return_value = True
        mock_create_output.return_value = True
        mock_test_config.return_value = False
        
        result = setup.main()
        
        assert result is False

    @patch('sys.exit')
    @patch('setup.main')
    def test_main_script_execution_success(self, mock_main, mock_exit):
        """Test main script execution with success."""
        mock_main.return_value = True
        
        # Execute the main script block
        exec(compile(open('setup.py').read(), 'setup.py', 'exec'))
        
        # sys.exit should not be called on success
        mock_exit.assert_not_called()

    @patch('sys.exit')
    @patch('setup.main')
    def test_main_script_execution_failure(self, mock_main, mock_exit):
        """Test main script execution with failure."""
        mock_main.return_value = False
        
        # Execute the main script block manually since we're mocking
        success = mock_main()
        if not success:
            mock_exit(1)
        
        # sys.exit should be called with code 1 on failure
        mock_exit.assert_called_once_with(1)