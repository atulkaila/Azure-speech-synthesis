"""
Unit tests for speech_synthesis.py module.
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Import the module under test
import speech_synthesis

class TestSpeechSynthesis:
    """Test class for speech_synthesis module."""

    def test_setup_speech_config_with_placeholder_credentials(self):
        """Test setup_speech_config raises ValueError with placeholder credentials."""
        with pytest.raises(ValueError, match="Please configure your Azure Speech Service credentials"):
            speech_synthesis.setup_speech_config()

    @patch('speech_synthesis.speechsdk')
    def test_setup_speech_config_success(self, mock_speechsdk):
        """Test successful speech configuration setup."""
        # Mock credentials
        original_key = speech_synthesis.SPEECH_KEY
        original_endpoint = speech_synthesis.SPEECH_ENDPOINT
        original_voice = speech_synthesis.DEFAULT_VOICE
        
        try:
            speech_synthesis.SPEECH_KEY = 'test_key_123'
            speech_synthesis.SPEECH_ENDPOINT = 'https://test.api.cognitive.microsoft.com/'
            speech_synthesis.DEFAULT_VOICE = 'en-US-TestVoice'
            
            # Mock SpeechConfig
            mock_config = Mock()
            mock_speechsdk.SpeechConfig.return_value = mock_config
            
            result = speech_synthesis.setup_speech_config()
            
            # Verify SpeechConfig was called with correct parameters
            mock_speechsdk.SpeechConfig.assert_called_once_with(
                subscription='test_key_123',
                endpoint='https://test.api.cognitive.microsoft.com/'
            )
            
            # Verify voice was set
            assert mock_config.speech_synthesis_voice_name == 'en-US-TestVoice'
            assert result == mock_config
            
        finally:
            # Restore original values
            speech_synthesis.SPEECH_KEY = original_key
            speech_synthesis.SPEECH_ENDPOINT = original_endpoint
            speech_synthesis.DEFAULT_VOICE = original_voice

    @patch('builtins.input')
    def test_get_user_output_preference_speakers(self, mock_input):
        """Test getting user preference for speakers output."""
        mock_input.return_value = '1'
        
        choice, filename = speech_synthesis.get_user_output_preference()
        
        assert choice == '1'
        assert filename is None

    @patch('builtins.input')
    def test_get_user_output_preference_file(self, mock_input):
        """Test getting user preference for file output."""
        mock_input.side_effect = ['2', 'test_output']
        
        choice, filename = speech_synthesis.get_user_output_preference()
        
        assert choice == '2'
        assert filename == 'test_output.wav'

    @patch('builtins.input')
    def test_get_user_output_preference_invalid_then_valid(self, mock_input):
        """Test handling invalid choice then valid choice."""
        mock_input.side_effect = ['3', '0', '1']
        
        choice, filename = speech_synthesis.get_user_output_preference()
        
        assert choice == '1'
        assert filename is None

    @patch('builtins.input')
    def test_get_user_output_preference_empty_filename_then_valid(self, mock_input):
        """Test handling empty filename then valid filename."""
        mock_input.side_effect = ['2', '', '  ', 'valid_filename']
        
        choice, filename = speech_synthesis.get_user_output_preference()
        
        assert choice == '2'
        assert filename == 'valid_filename.wav'

    @patch('speech_synthesis.speechsdk')
    def test_setup_audio_config_speakers(self, mock_speechsdk):
        """Test setting up audio config for speakers."""
        mock_audio_config = Mock()
        mock_speechsdk.audio.AudioOutputConfig.return_value = mock_audio_config
        
        result = speech_synthesis.setup_audio_config('1')
        
        mock_speechsdk.audio.AudioOutputConfig.assert_called_once_with(use_default_speaker=True)
        assert result == mock_audio_config

    @patch('speech_synthesis.speechsdk')
    def test_setup_audio_config_file(self, mock_speechsdk):
        """Test setting up audio config for file output."""
        mock_audio_config = Mock()
        mock_speechsdk.audio.AudioOutputConfig.return_value = mock_audio_config
        
        result = speech_synthesis.setup_audio_config('2', 'test.wav')
        
        mock_speechsdk.audio.AudioOutputConfig.assert_called_once_with(filename='test.wav')
        assert result == mock_audio_config

    @patch('speech_synthesis.speechsdk')
    def test_setup_audio_config_file_no_filename(self, mock_speechsdk):
        """Test setting up audio config for file output without filename defaults to speakers."""
        mock_audio_config = Mock()
        mock_speechsdk.audio.AudioOutputConfig.return_value = mock_audio_config
        
        result = speech_synthesis.setup_audio_config('2')
        
        mock_speechsdk.audio.AudioOutputConfig.assert_called_once_with(use_default_speaker=True)
        assert result == mock_audio_config

    @patch('builtins.input')
    def test_get_text_input_with_text(self, mock_input):
        """Test getting text input from user."""
        mock_input.return_value = 'Hello world!'
        
        result = speech_synthesis.get_text_input()
        
        assert result == 'Hello world!'

    @patch('builtins.input')
    def test_get_text_input_empty_uses_default(self, mock_input):
        """Test getting empty text input uses default text."""
        mock_input.return_value = ''
        
        result = speech_synthesis.get_text_input()
        
        assert result == "Hello! This is a test of Azure Speech Services."

    @patch('builtins.input')
    def test_get_text_input_whitespace_uses_default(self, mock_input):
        """Test getting whitespace-only text input uses default text."""
        mock_input.return_value = '   '
        
        result = speech_synthesis.get_text_input()
        
        assert result == "Hello! This is a test of Azure Speech Services."

    @patch('speech_synthesis.speechsdk')
    def test_synthesize_speech_success(self, mock_speechsdk):
        """Test successful speech synthesis."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_audio_config = Mock()
        mock_synthesizer = Mock()
        mock_result = Mock()
        
        mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
        mock_synthesizer.speak_text_async.return_value.get.return_value = mock_result
        mock_result.reason = mock_speechsdk.ResultReason.SynthesizingAudioCompleted
        
        result = speech_synthesis.synthesize_speech(
            mock_speech_config, 
            mock_audio_config, 
            "Test text"
        )
        
        # Verify synthesizer was created correctly
        mock_speechsdk.SpeechSynthesizer.assert_called_once_with(
            speech_config=mock_speech_config,
            audio_config=mock_audio_config
        )
        
        # Verify synthesis was called
        mock_synthesizer.speak_text_async.assert_called_once_with("Test text")
        
        assert result is True

    @patch('speech_synthesis.speechsdk')
    def test_synthesize_speech_canceled(self, mock_speechsdk):
        """Test speech synthesis canceled."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_audio_config = Mock()
        mock_synthesizer = Mock()
        mock_result = Mock()
        mock_cancellation_details = Mock()
        
        mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
        mock_synthesizer.speak_text_async.return_value.get.return_value = mock_result
        mock_result.reason = mock_speechsdk.ResultReason.Canceled
        mock_result.cancellation_details = mock_cancellation_details
        mock_cancellation_details.reason = mock_speechsdk.CancellationReason.Error
        mock_cancellation_details.error_details = "Test error"
        
        result = speech_synthesis.synthesize_speech(
            mock_speech_config, 
            mock_audio_config, 
            "Test text"
        )
        
        assert result is False

    @patch('speech_synthesis.speechsdk')
    def test_synthesize_speech_unexpected_result(self, mock_speechsdk):
        """Test speech synthesis with unexpected result."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_audio_config = Mock()
        mock_synthesizer = Mock()
        mock_result = Mock()
        
        mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
        mock_synthesizer.speak_text_async.return_value.get.return_value = mock_result
        mock_result.reason = "UnexpectedReason"
        
        result = speech_synthesis.synthesize_speech(
            mock_speech_config, 
            mock_audio_config, 
            "Test text"
        )
        
        assert result is False

    @patch('speech_synthesis.speechsdk')
    def test_synthesize_speech_exception(self, mock_speechsdk):
        """Test speech synthesis with exception."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_audio_config = Mock()
        
        mock_speechsdk.SpeechSynthesizer.side_effect = Exception("Test exception")
        
        result = speech_synthesis.synthesize_speech(
            mock_speech_config, 
            mock_audio_config, 
            "Test text"
        )
        
        assert result is False

    @patch('speech_synthesis.synthesize_speech')
    @patch('speech_synthesis.get_text_input')
    @patch('speech_synthesis.setup_audio_config')
    @patch('speech_synthesis.get_user_output_preference')
    @patch('speech_synthesis.setup_speech_config')
    def test_main_success_speakers(self, mock_setup_speech, mock_get_preference, 
                                  mock_setup_audio, mock_get_text, mock_synthesize):
        """Test main function with successful execution for speakers."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_audio_config = Mock()
        
        mock_setup_speech.return_value = mock_speech_config
        mock_get_preference.return_value = ('1', None)
        mock_setup_audio.return_value = mock_audio_config
        mock_get_text.return_value = "Test text"
        mock_synthesize.return_value = True
        
        # Capture stdout to verify output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis.main()
            output = fake_out.getvalue()
        
        # Verify all functions were called
        mock_setup_speech.assert_called_once()
        mock_get_preference.assert_called_once()
        mock_setup_audio.assert_called_once_with('1', None)
        mock_get_text.assert_called_once()
        mock_synthesize.assert_called_once_with(mock_speech_config, mock_audio_config, "Test text")
        
        # Verify success output
        assert "✅ Speech synthesized and played through speakers" in output

    @patch('speech_synthesis.synthesize_speech')
    @patch('speech_synthesis.get_text_input')
    @patch('speech_synthesis.setup_audio_config')
    @patch('speech_synthesis.get_user_output_preference')
    @patch('speech_synthesis.setup_speech_config')
    def test_main_success_file(self, mock_setup_speech, mock_get_preference, 
                              mock_setup_audio, mock_get_text, mock_synthesize):
        """Test main function with successful execution for file output."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_audio_config = Mock()
        
        mock_setup_speech.return_value = mock_speech_config
        mock_get_preference.return_value = ('2', 'test.wav')
        mock_setup_audio.return_value = mock_audio_config
        mock_get_text.return_value = "Test text"
        mock_synthesize.return_value = True
        
        # Capture stdout to verify output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis.main()
            output = fake_out.getvalue()
        
        # Verify success output for file
        assert "✅ Speech synthesized and saved to file: test.wav" in output

    @patch('speech_synthesis.setup_speech_config')
    def test_main_configuration_error(self, mock_setup_speech):
        """Test main function with configuration error."""
        mock_setup_speech.side_effect = ValueError("Configuration error")
        
        # Capture stdout to verify output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis.main()
            output = fake_out.getvalue()
        
        # Verify error handling
        assert "❌ Configuration Error: Configuration error" in output
        assert "💡 Setup Instructions:" in output

    @patch('speech_synthesis.setup_speech_config')
    def test_main_unexpected_error(self, mock_setup_speech):
        """Test main function with unexpected error."""
        mock_setup_speech.side_effect = RuntimeError("Unexpected error")
        
        # Capture stdout to verify output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis.main()
            output = fake_out.getvalue()
        
        # Verify error handling
        assert "❌ An unexpected error occurred: Unexpected error" in output

    @patch('speech_synthesis.synthesize_speech')
    @patch('speech_synthesis.get_text_input')
    @patch('speech_synthesis.setup_audio_config')
    @patch('speech_synthesis.get_user_output_preference')
    @patch('speech_synthesis.setup_speech_config')
    def test_main_synthesis_failure(self, mock_setup_speech, mock_get_preference, 
                                   mock_setup_audio, mock_get_text, mock_synthesize):
        """Test main function with synthesis failure."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_audio_config = Mock()
        
        mock_setup_speech.return_value = mock_speech_config
        mock_get_preference.return_value = ('1', None)
        mock_setup_audio.return_value = mock_audio_config
        mock_get_text.return_value = "Test text"
        mock_synthesize.return_value = False
        
        # Capture stdout to verify output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis.main()
            output = fake_out.getvalue()
        
        # Verify failure output
        assert "❌ Speech synthesis failed" in output

    def test_long_text_truncation_in_synthesize_speech(self):
        """Test that long text is properly truncated in output messages."""
        with patch('speech_synthesis.speechsdk') as mock_speechsdk:
            # Setup mocks
            mock_speech_config = Mock()
            mock_audio_config = Mock()
            mock_synthesizer = Mock()
            mock_result = Mock()
            
            mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
            mock_synthesizer.speak_text_async.return_value.get.return_value = mock_result
            mock_result.reason = mock_speechsdk.ResultReason.SynthesizingAudioCompleted
            
            long_text = "A" * 100  # 100 character text
            
            # Capture stdout to verify truncation
            with patch('sys.stdout', new=StringIO()) as fake_out:
                speech_synthesis.synthesize_speech(
                    mock_speech_config, 
                    mock_audio_config, 
                    long_text
                )
                output = fake_out.getvalue()
            
            # Verify text is truncated with ellipsis
            assert "A" * 50 + "..." in output