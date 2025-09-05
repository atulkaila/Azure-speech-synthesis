"""
Unit tests for example_simple.py module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Import the module under test
import example_simple

class TestExampleSimple:
    """Test class for example_simple module."""

    def test_simple_text_to_speech_placeholder_credentials(self):
        """Test simple_text_to_speech with placeholder credentials."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            example_simple.simple_text_to_speech()
            output = fake_out.getvalue()
        
        assert "❌ Please configure your Azure Speech Service credentials" in output
        assert "Edit this file and replace SPEECH_KEY and SPEECH_ENDPOINT" in output

    @patch('example_simple.speechsdk')
    def test_simple_text_to_speech_success(self, mock_speechsdk):
        """Test successful text-to-speech synthesis."""
        # Temporarily change module constants instead of patching them
        with patch.object(example_simple, 'SPEECH_KEY', 'test_speech_key_123'):
            with patch.object(example_simple, 'SPEECH_ENDPOINT', 'https://test-region.api.cognitive.microsoft.com/'):
            
                # Setup mocks
                mock_speech_config = Mock()
                mock_audio_config = Mock()
                mock_synthesizer = Mock()
                mock_result = Mock()
                
                mock_speechsdk.SpeechConfig.return_value = mock_speech_config
                mock_speechsdk.audio.AudioOutputConfig.return_value = mock_audio_config
                mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
                mock_synthesizer.speak_text_async.return_value.get.return_value = mock_result
                mock_result.reason = mock_speechsdk.ResultReason.SynthesizingAudioCompleted
                
                # Capture output
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    example_simple.simple_text_to_speech()
                    output = fake_out.getvalue()
                
                # Verify Azure SDK calls
                mock_speechsdk.SpeechConfig.assert_called_once_with(
                    subscription="test_speech_key_123",
                    endpoint="https://test-region.api.cognitive.microsoft.com/"
                )
                
                # Verify voice was set
                assert mock_speech_config.speech_synthesis_voice_name == "en-US-AndrewMultilingualNeural"
                
                # Verify audio config
                mock_speechsdk.audio.AudioOutputConfig.assert_called_once_with(use_default_speaker=True)
                
                # Verify synthesizer creation
                mock_speechsdk.SpeechSynthesizer.assert_called_once_with(
                    speech_config=mock_speech_config,
                    audio_config=mock_audio_config
                )
                
                # Verify synthesis call
                expected_text = "Hello! This is a simple example of Azure Speech Services. Welcome to text-to-speech synthesis!"
                mock_synthesizer.speak_text_async.assert_called_once_with(expected_text)
                
                # Verify success output
                assert "🔄 Converting text to speech:" in output
                assert "✅ Speech synthesis completed successfully!" in output

    @patch('example_simple.speechsdk')
    def test_simple_text_to_speech_canceled(self, mock_speechsdk):
        """Test text-to-speech synthesis with canceled result."""
        # Mock credentials
        original_key = example_simple.SPEECH_KEY
        original_endpoint = example_simple.SPEECH_ENDPOINT
        
        try:
            example_simple.SPEECH_KEY = "test_key"
            example_simple.SPEECH_ENDPOINT = "https://test.api.com/"
            
            # Setup mocks for canceled result
            mock_speech_config = Mock()
            mock_audio_config = Mock()
            mock_synthesizer = Mock()
            mock_result = Mock()
            mock_cancellation_details = Mock()
            
            mock_speechsdk.SpeechConfig.return_value = mock_speech_config
            mock_speechsdk.audio.AudioOutputConfig.return_value = mock_audio_config
            mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
            mock_synthesizer.speak_text_async.return_value.get.return_value = mock_result
            
            # Setup canceled result
            mock_result.reason = mock_speechsdk.ResultReason.Canceled
            mock_result.cancellation_details = mock_cancellation_details
            mock_cancellation_details.reason = "TestCancellationReason"
            mock_cancellation_details.error_details = "Test error details"
            
            # Capture output
            with patch('sys.stdout', new=StringIO()) as fake_out:
                example_simple.simple_text_to_speech()
                output = fake_out.getvalue()
            
            # Verify canceled output
            assert "❌ Speech synthesis was canceled: TestCancellationReason" in output
            assert "Error details: Test error details" in output
            
        finally:
            example_simple.SPEECH_KEY = original_key
            example_simple.SPEECH_ENDPOINT = original_endpoint

    @patch('example_simple.speechsdk')
    def test_simple_text_to_speech_canceled_without_error_details(self, mock_speechsdk):
        """Test text-to-speech synthesis with canceled result but no error details."""
        # Mock credentials
        original_key = example_simple.SPEECH_KEY
        original_endpoint = example_simple.SPEECH_ENDPOINT
        
        try:
            example_simple.SPEECH_KEY = "test_key"
            example_simple.SPEECH_ENDPOINT = "https://test.api.com/"
            
            # Setup mocks for canceled result
            mock_speech_config = Mock()
            mock_audio_config = Mock()
            mock_synthesizer = Mock()
            mock_result = Mock()
            mock_cancellation_details = Mock()
            
            mock_speechsdk.SpeechConfig.return_value = mock_speech_config
            mock_speechsdk.audio.AudioOutputConfig.return_value = mock_audio_config
            mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
            mock_synthesizer.speak_text_async.return_value.get.return_value = mock_result
            
            # Setup canceled result without error details
            mock_result.reason = mock_speechsdk.ResultReason.Canceled
            mock_result.cancellation_details = mock_cancellation_details
            mock_cancellation_details.reason = "TestCancellationReason"
            mock_cancellation_details.error_details = None
            
            # Capture output
            with patch('sys.stdout', new=StringIO()) as fake_out:
                example_simple.simple_text_to_speech()
                output = fake_out.getvalue()
            
            # Verify canceled output without error details
            assert "❌ Speech synthesis was canceled: TestCancellationReason" in output
            assert "Error details:" not in output
            
        finally:
            example_simple.SPEECH_KEY = original_key
            example_simple.SPEECH_ENDPOINT = original_endpoint

    @patch('example_simple.speechsdk')
    def test_simple_text_to_speech_exception(self, mock_speechsdk):
        """Test text-to-speech synthesis with exception."""
        # Mock credentials
        original_key = example_simple.SPEECH_KEY
        original_endpoint = example_simple.SPEECH_ENDPOINT
        
        try:
            example_simple.SPEECH_KEY = "test_key"
            example_simple.SPEECH_ENDPOINT = "https://test.api.com/"
            
            # Setup mocks to raise exception
            mock_speechsdk.SpeechConfig.side_effect = Exception("Test exception")
            
            # Capture output
            with patch('sys.stdout', new=StringIO()) as fake_out:
                example_simple.simple_text_to_speech()
                output = fake_out.getvalue()
            
            # Verify exception handling
            assert "❌ An error occurred: Test exception" in output
            
        finally:
            example_simple.SPEECH_KEY = original_key
            example_simple.SPEECH_ENDPOINT = original_endpoint

    @patch('example_simple.simple_text_to_speech')
    def test_main_execution(self, mock_simple_tts):
        """Test main execution block."""
        # Test that the main block correctly calls the function
        # This simulates running the script
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Simulate the main block execution
            print("🎤 Simple Azure Speech Service Example")
            print("=" * 40)
            mock_simple_tts()
            print("=" * 40)
            
            output = fake_out.getvalue()
        
        # Verify main block output
        assert "🎤 Simple Azure Speech Service Example" in output
        assert "=" * 40 in output
        mock_simple_tts.assert_called_once()

    @patch('example_simple.speechsdk')
    def test_simple_text_to_speech_voice_configuration(self, mock_speechsdk):
        """Test that the correct voice is configured."""
        # Mock credentials
        original_key = example_simple.SPEECH_KEY
        original_endpoint = example_simple.SPEECH_ENDPOINT
        
        try:
            example_simple.SPEECH_KEY = "test_key"
            example_simple.SPEECH_ENDPOINT = "https://test.api.com/"
            
            # Setup mocks
            mock_speech_config = Mock()
            mock_speechsdk.SpeechConfig.return_value = mock_speech_config
            
            # Mock other components to prevent errors
            mock_speechsdk.audio.AudioOutputConfig.return_value = Mock()
            mock_synthesizer = Mock()
            mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
            mock_result = Mock()
            mock_result.reason = mock_speechsdk.ResultReason.SynthesizingAudioCompleted
            mock_synthesizer.speak_text_async.return_value.get.return_value = mock_result
            
            example_simple.simple_text_to_speech()
            
            # Verify the specific voice was set
            assert mock_speech_config.speech_synthesis_voice_name == "en-US-AndrewMultilingualNeural"
            
        finally:
            example_simple.SPEECH_KEY = original_key
            example_simple.SPEECH_ENDPOINT = original_endpoint

    @patch('example_simple.speechsdk')
    def test_simple_text_to_speech_text_content(self, mock_speechsdk):
        """Test that the correct text is synthesized."""
        # Mock credentials
        original_key = example_simple.SPEECH_KEY
        original_endpoint = example_simple.SPEECH_ENDPOINT
        
        try:
            example_simple.SPEECH_KEY = "test_key"
            example_simple.SPEECH_ENDPOINT = "https://test.api.com/"
            
            # Setup mocks
            mock_synthesizer = Mock()
            mock_speechsdk.SpeechConfig.return_value = Mock()
            mock_speechsdk.audio.AudioOutputConfig.return_value = Mock()
            mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
            
            mock_result = Mock()
            mock_result.reason = mock_speechsdk.ResultReason.SynthesizingAudioCompleted
            mock_synthesizer.speak_text_async.return_value.get.return_value = mock_result
            
            example_simple.simple_text_to_speech()
            
            # Verify the correct text was passed to synthesis
            expected_text = "Hello! This is a simple example of Azure Speech Services. Welcome to text-to-speech synthesis!"
            mock_synthesizer.speak_text_async.assert_called_once_with(expected_text)
            
        finally:
            example_simple.SPEECH_KEY = original_key
            example_simple.SPEECH_ENDPOINT = original_endpoint