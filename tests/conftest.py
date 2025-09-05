"""
Pytest configuration and fixtures for Azure Speech Synthesis tests.
"""
import pytest
import sys
import os
from unittest.mock import Mock, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def mock_speechsdk():
    """Mock Azure Speech SDK module."""
    mock_sdk = MagicMock()
    
    # Mock SpeechConfig
    mock_speech_config = Mock()
    mock_sdk.SpeechConfig.return_value = mock_speech_config
    
    # Mock AudioOutputConfig
    mock_audio_config = Mock()
    mock_sdk.audio.AudioOutputConfig.return_value = mock_audio_config
    
    # Mock SpeechSynthesizer
    mock_synthesizer = Mock()
    mock_sdk.SpeechSynthesizer.return_value = mock_synthesizer
    
    # Mock synthesis result
    mock_result = Mock()
    mock_result.reason = mock_sdk.ResultReason.SynthesizingAudioCompleted
    mock_synthesizer.speak_text_async.return_value.get.return_value = mock_result
    mock_synthesizer.speak_ssml_async.return_value.get.return_value = mock_result
    
    # Mock enum values
    mock_sdk.ResultReason.SynthesizingAudioCompleted = "SynthesizingAudioCompleted"
    mock_sdk.ResultReason.Canceled = "Canceled"
    mock_sdk.CancellationReason.Error = "Error"
    
    return mock_sdk

@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "Hello, this is a test for Azure Speech Services."

@pytest.fixture
def test_config():
    """Test configuration values."""
    return {
        'speech_key': 'test_speech_key_12345',
        'speech_endpoint': 'https://test-region.api.cognitive.microsoft.com/',
        'default_voice': 'en-US-AndrewMultilingualNeural'
    }

@pytest.fixture
def temp_config_file(tmp_path, test_config):
    """Create a temporary config file for testing."""
    config_file = tmp_path / "config.py"
    config_content = f'''# Test configuration
SPEECH_KEY = "{test_config['speech_key']}"
SPEECH_ENDPOINT = "{test_config['speech_endpoint']}"
DEFAULT_VOICE = "{test_config['default_voice']}"
DEFAULT_OUTPUT_FOLDER = "output"
DEFAULT_FILENAME_PREFIX = "speech_output"
'''
    config_file.write_text(config_content)
    return config_file

@pytest.fixture
def mock_input_side_effects():
    """Common input side effects for user interaction tests."""
    return {
        'choice_speakers': ['1'],
        'choice_file': ['2', 'test_output'],
        'text_input': ['Test speech synthesis'],
        'voice_selection': ['1'],
        'voice_style': ['1'],
        'voice_speed': ['1'],
        'confirm_yes': ['y'],
        'confirm_no': ['n']
    }

@pytest.fixture
def mock_file_operations(tmp_path):
    """Mock file operations for testing."""
    # Create temporary directories
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    return {
        'output_dir': output_dir,
        'temp_dir': tmp_path
    }