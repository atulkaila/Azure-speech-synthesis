"""
Unit tests for speech_synthesis_custom_voice.py module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Import the module under test
import speech_synthesis_custom_voice

class TestSpeechSynthesisCustomVoice:
    """Test class for speech_synthesis_custom_voice module."""

    def test_setup_speech_config_with_placeholder_credentials(self):
        """Test setup_speech_config raises ValueError with placeholder credentials."""
        with pytest.raises(ValueError, match="Please configure your Azure Speech Service credentials"):
            speech_synthesis_custom_voice.setup_speech_config()

    @patch('speech_synthesis_custom_voice.speechsdk')
    def test_setup_speech_config_success(self, mock_speechsdk):
        """Test successful speech configuration setup."""
        # Mock credentials
        original_key = speech_synthesis_custom_voice.SPEECH_KEY
        original_endpoint = speech_synthesis_custom_voice.SPEECH_ENDPOINT
        
        try:
            speech_synthesis_custom_voice.SPEECH_KEY = 'test_key_123'
            speech_synthesis_custom_voice.SPEECH_ENDPOINT = 'https://test.api.cognitive.microsoft.com/'
            
            # Mock SpeechConfig
            mock_config = Mock()
            mock_speechsdk.SpeechConfig.return_value = mock_config
            
            result = speech_synthesis_custom_voice.setup_speech_config()
            
            # Verify SpeechConfig was called with correct parameters
            mock_speechsdk.SpeechConfig.assert_called_once_with(
                subscription='test_key_123',
                endpoint='https://test.api.cognitive.microsoft.com/'
            )
            
            assert result == mock_config
            
        finally:
            # Restore original values
            speech_synthesis_custom_voice.SPEECH_KEY = original_key
            speech_synthesis_custom_voice.SPEECH_ENDPOINT = original_endpoint

    def test_display_voice_options(self):
        """Test display_voice_options function outputs correct information."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis_custom_voice.display_voice_options()
            output = fake_out.getvalue()
        
        # Check that all voices are displayed
        assert "🎙️  AVAILABLE VOICE OPTIONS" in output
        assert "en-US-AndrewMultilingualNeural" in output
        assert "en-US-AvaMultilingualNeural" in output
        assert "en-US-BrianMultilingualNeural" in output
        assert "en-US-EmmaMultilingualNeural" in output
        assert "en-US-JennyNeural" in output
        assert "en-US-GuyNeural" in output

    @patch('builtins.input')
    def test_get_voice_selection_valid_choice(self, mock_input):
        """Test getting valid voice selection."""
        mock_input.return_value = '1'
        
        with patch('speech_synthesis_custom_voice.display_voice_options'):
            result = speech_synthesis_custom_voice.get_voice_selection()
        
        expected_voice = speech_synthesis_custom_voice.AVAILABLE_VOICES['1']
        assert result == expected_voice

    @patch('builtins.input')
    def test_get_voice_selection_invalid_then_valid(self, mock_input):
        """Test getting invalid then valid voice selection."""
        mock_input.side_effect = ['7', '0', '2']
        
        with patch('speech_synthesis_custom_voice.display_voice_options'):
            result = speech_synthesis_custom_voice.get_voice_selection()
        
        expected_voice = speech_synthesis_custom_voice.AVAILABLE_VOICES['2']
        assert result == expected_voice

    @patch('builtins.input')
    def test_get_voice_style_default(self, mock_input):
        """Test getting default voice style."""
        mock_input.return_value = ''  # Empty input for default
        
        voice_info = speech_synthesis_custom_voice.AVAILABLE_VOICES['1']
        result = speech_synthesis_custom_voice.get_voice_style(voice_info)
        
        assert result == 'default'

    @patch('builtins.input')
    def test_get_voice_style_valid_choice(self, mock_input):
        """Test getting valid voice style choice."""
        mock_input.return_value = '2'  # Second style option
        
        voice_info = speech_synthesis_custom_voice.AVAILABLE_VOICES['1']
        result = speech_synthesis_custom_voice.get_voice_style(voice_info)
        
        expected_style = voice_info['styles'][1]  # Second style (index 1)
        assert result == expected_style

    @patch('builtins.input')
    def test_get_voice_style_invalid_then_valid(self, mock_input):
        """Test getting invalid then valid voice style."""
        mock_input.side_effect = ['99', 'abc', '1']
        
        voice_info = speech_synthesis_custom_voice.AVAILABLE_VOICES['1']
        result = speech_synthesis_custom_voice.get_voice_style(voice_info)
        
        expected_style = voice_info['styles'][0]  # First style
        assert result == expected_style

    @patch('builtins.input')
    def test_get_voice_speed_default(self, mock_input):
        """Test getting default voice speed."""
        mock_input.return_value = ''  # Empty input for default
        
        result = speech_synthesis_custom_voice.get_voice_speed()
        
        assert result == 'medium'

    @patch('builtins.input')
    def test_get_voice_speed_valid_choices(self, mock_input):
        """Test getting valid voice speed choices."""
        # Test all valid speed options
        speed_tests = [
            ('1', 'x-slow'),
            ('2', 'slow'),
            ('3', 'medium'),
            ('4', 'fast'),
            ('5', 'x-fast')
        ]
        
        for input_val, expected_speed in speed_tests:
            mock_input.return_value = input_val
            result = speech_synthesis_custom_voice.get_voice_speed()
            assert result == expected_speed

    @patch('builtins.input')
    def test_get_voice_speed_invalid_then_valid(self, mock_input):
        """Test getting invalid then valid voice speed."""
        mock_input.side_effect = ['6', '0', 'abc', '3']
        
        result = speech_synthesis_custom_voice.get_voice_speed()
        
        assert result == 'medium'

    def test_create_ssml_text_basic(self):
        """Test creating basic SSML text."""
        text = "Hello world"
        voice_name = "en-US-AndrewMultilingualNeural"
        
        result = speech_synthesis_custom_voice.create_ssml_text(text, voice_name)
        
        assert f'<voice name="{voice_name}">' in result
        assert f'<prosody rate="medium">{text}</prosody>' in result
        assert '<speak version="1.0"' in result

    def test_create_ssml_text_with_style(self):
        """Test creating SSML text with custom style."""
        text = "Hello world"
        voice_name = "en-US-AndrewMultilingualNeural"
        style = "cheerful"
        
        result = speech_synthesis_custom_voice.create_ssml_text(text, voice_name, style)
        
        assert f'<mstts:express-as style="{style}">' in result
        assert '</mstts:express-as>' in result

    def test_create_ssml_text_with_speed(self):
        """Test creating SSML text with custom speed."""
        text = "Hello world"
        voice_name = "en-US-AndrewMultilingualNeural"
        speed = "fast"
        
        result = speech_synthesis_custom_voice.create_ssml_text(text, voice_name, speed=speed)
        
        assert f'<prosody rate="{speed}">' in result

    def test_create_ssml_text_with_special_characters(self):
        """Test creating SSML text with special characters that need escaping."""
        text = "Hello & goodbye <test> XML"
        voice_name = "en-US-AndrewMultilingualNeural"
        
        result = speech_synthesis_custom_voice.create_ssml_text(text, voice_name)
        
        assert "Hello &amp; goodbye &lt;test&gt; XML" in result

    def test_create_ssml_text_complete(self):
        """Test creating SSML text with all options."""
        text = "Hello world"
        voice_name = "en-US-AvaMultilingualNeural"
        style = "excited"
        speed = "x-fast"
        
        result = speech_synthesis_custom_voice.create_ssml_text(text, voice_name, style, speed)
        
        assert f'<voice name="{voice_name}">' in result
        assert f'<mstts:express-as style="{style}">' in result
        assert f'<prosody rate="{speed}">{text}</prosody>' in result
        assert '</mstts:express-as>' in result

    def test_preview_voice_settings(self):
        """Test preview_voice_settings function outputs correct information."""
        voice_info = speech_synthesis_custom_voice.AVAILABLE_VOICES['1']
        style = "cheerful"
        speed = "fast"
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis_custom_voice.preview_voice_settings(voice_info, style, speed)
            output = fake_out.getvalue()
        
        assert "🔍 VOICE PREVIEW" in output
        assert voice_info['name'] in output
        assert voice_info['gender'] in output
        assert "Cheerful" in output  # Style should be title-cased
        assert "Fast" in output  # Speed should be title-cased
        assert voice_info['description'] in output

    @patch('builtins.input')
    def test_get_user_output_preference_speakers(self, mock_input):
        """Test getting user preference for speakers output."""
        mock_input.return_value = '1'
        
        choice, filename = speech_synthesis_custom_voice.get_user_output_preference()
        
        assert choice == '1'
        assert filename is None

    @patch('builtins.input')
    def test_get_user_output_preference_file(self, mock_input):
        """Test getting user preference for file output."""
        mock_input.side_effect = ['2', 'test_output']
        
        choice, filename = speech_synthesis_custom_voice.get_user_output_preference()
        
        assert choice == '2'
        assert filename == 'test_output.wav'

    @patch('speech_synthesis_custom_voice.speechsdk')
    def test_setup_audio_config_speakers(self, mock_speechsdk):
        """Test setting up audio config for speakers."""
        mock_audio_config = Mock()
        mock_speechsdk.audio.AudioOutputConfig.return_value = mock_audio_config
        
        result = speech_synthesis_custom_voice.setup_audio_config('1')
        
        mock_speechsdk.audio.AudioOutputConfig.assert_called_once_with(use_default_speaker=True)
        assert result == mock_audio_config

    @patch('speech_synthesis_custom_voice.speechsdk')
    def test_setup_audio_config_file(self, mock_speechsdk):
        """Test setting up audio config for file output."""
        mock_audio_config = Mock()
        mock_speechsdk.audio.AudioOutputConfig.return_value = mock_audio_config
        
        result = speech_synthesis_custom_voice.setup_audio_config('2', 'test.wav')
        
        mock_speechsdk.audio.AudioOutputConfig.assert_called_once_with(filename='test.wav')
        assert result == mock_audio_config

    @patch('builtins.input')
    def test_get_text_input_single_line(self, mock_input):
        """Test getting single line text input."""
        mock_input.side_effect = ['Hello world!', '']
        
        result = speech_synthesis_custom_voice.get_text_input()
        
        assert result == 'Hello world!'

    @patch('builtins.input')
    def test_get_text_input_multiple_lines(self, mock_input):
        """Test getting multiple lines text input."""
        mock_input.side_effect = ['Hello', 'world!', '']
        
        result = speech_synthesis_custom_voice.get_text_input()
        
        assert result == 'Hello world!'

    @patch('builtins.input')
    def test_get_text_input_quit(self, mock_input):
        """Test quitting text input."""
        mock_input.return_value = 'quit'
        
        result = speech_synthesis_custom_voice.get_text_input()
        
        assert result is None

    @patch('builtins.input')
    def test_get_text_input_empty_uses_default(self, mock_input):
        """Test empty text input uses default text."""
        mock_input.return_value = ''
        
        result = speech_synthesis_custom_voice.get_text_input()
        
        assert result == "Hello! This is a demonstration of Azure Speech Services with custom voice options."

    @patch('speech_synthesis_custom_voice.speechsdk')
    def test_synthesize_speech_with_ssml_success(self, mock_speechsdk):
        """Test successful speech synthesis with SSML."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_audio_config = Mock()
        mock_synthesizer = Mock()
        mock_result = Mock()
        
        mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
        mock_synthesizer.speak_ssml_async.return_value.get.return_value = mock_result
        mock_result.reason = mock_speechsdk.ResultReason.SynthesizingAudioCompleted
        
        ssml_text = "<speak>Hello world</speak>"
        
        result = speech_synthesis_custom_voice.synthesize_speech_with_ssml(
            mock_speech_config, 
            mock_audio_config, 
            ssml_text
        )
        
        # Verify synthesizer was created correctly
        mock_speechsdk.SpeechSynthesizer.assert_called_once_with(
            speech_config=mock_speech_config,
            audio_config=mock_audio_config
        )
        
        # Verify SSML synthesis was called
        mock_synthesizer.speak_ssml_async.assert_called_once_with(ssml_text)
        
        assert result is True

    @patch('speech_synthesis_custom_voice.speechsdk')
    def test_synthesize_speech_with_ssml_canceled(self, mock_speechsdk):
        """Test speech synthesis with SSML canceled."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_audio_config = Mock()
        mock_synthesizer = Mock()
        mock_result = Mock()
        mock_cancellation_details = Mock()
        
        mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
        mock_synthesizer.speak_ssml_async.return_value.get.return_value = mock_result
        mock_result.reason = mock_speechsdk.ResultReason.Canceled
        mock_result.cancellation_details = mock_cancellation_details
        mock_cancellation_details.reason = mock_speechsdk.CancellationReason.Error
        mock_cancellation_details.error_details = "Test error"
        
        result = speech_synthesis_custom_voice.synthesize_speech_with_ssml(
            mock_speech_config, 
            mock_audio_config, 
            "<speak>Hello</speak>"
        )
        
        assert result is False

    @patch('speech_synthesis_custom_voice.speechsdk')
    def test_synthesize_speech_with_ssml_exception(self, mock_speechsdk):
        """Test speech synthesis with SSML with exception."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_audio_config = Mock()
        
        mock_speechsdk.SpeechSynthesizer.side_effect = Exception("Test exception")
        
        result = speech_synthesis_custom_voice.synthesize_speech_with_ssml(
            mock_speech_config, 
            mock_audio_config, 
            "<speak>Hello</speak>"
        )
        
        assert result is False

    @patch('builtins.input')
    @patch('speech_synthesis_custom_voice.synthesize_speech_with_ssml')
    @patch('speech_synthesis_custom_voice.create_ssml_text')
    @patch('speech_synthesis_custom_voice.get_text_input')
    @patch('speech_synthesis_custom_voice.setup_audio_config')
    @patch('speech_synthesis_custom_voice.get_user_output_preference')
    @patch('speech_synthesis_custom_voice.preview_voice_settings')
    @patch('speech_synthesis_custom_voice.get_voice_speed')
    @patch('speech_synthesis_custom_voice.get_voice_style')
    @patch('speech_synthesis_custom_voice.get_voice_selection')
    @patch('speech_synthesis_custom_voice.setup_speech_config')
    def test_main_complete_success(self, mock_setup_speech, mock_get_voice, 
                                  mock_get_style, mock_get_speed, mock_preview,
                                  mock_get_preference, mock_setup_audio, 
                                  mock_get_text, mock_create_ssml, 
                                  mock_synthesize, mock_input):
        """Test main function with complete successful execution."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_voice_info = speech_synthesis_custom_voice.AVAILABLE_VOICES['1']
        mock_audio_config = Mock()
        
        mock_setup_speech.return_value = mock_speech_config
        mock_get_voice.return_value = mock_voice_info
        mock_get_style.return_value = 'cheerful'
        mock_get_speed.return_value = 'fast'
        mock_get_preference.return_value = ('1', None)
        mock_setup_audio.return_value = mock_audio_config
        mock_get_text.return_value = "Test text"
        mock_create_ssml.return_value = "<speak>Test SSML</speak>"
        mock_synthesize.return_value = True
        
        # Mock input for confirmation and SSML preview
        mock_input.side_effect = ['y', 'n']  # Proceed with settings, no SSML preview
        
        # Capture stdout to verify output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis_custom_voice.main()
            output = fake_out.getvalue()
        
        # Verify all functions were called
        mock_setup_speech.assert_called_once()
        mock_get_voice.assert_called_once()
        mock_get_style.assert_called_once_with(mock_voice_info)
        mock_get_speed.assert_called_once()
        mock_preview.assert_called_once_with(mock_voice_info, 'cheerful', 'fast')
        mock_get_preference.assert_called_once()
        mock_setup_audio.assert_called_once_with('1', None)
        mock_get_text.assert_called_once()
        mock_create_ssml.assert_called_once_with("Test text", mock_voice_info['name'], 'cheerful', 'fast')
        mock_synthesize.assert_called_once_with(mock_speech_config, mock_audio_config, "<speak>Test SSML</speak>")
        
        # Verify success output
        assert "✅ Custom voice speech synthesized and played through speakers" in output

    @patch('builtins.input')
    @patch('speech_synthesis_custom_voice.get_voice_selection')
    @patch('speech_synthesis_custom_voice.setup_speech_config')
    def test_main_user_cancels_settings(self, mock_setup_speech, mock_get_voice, mock_input):
        """Test main function when user cancels settings."""
        mock_setup_speech.return_value = Mock()
        mock_get_voice.return_value = speech_synthesis_custom_voice.AVAILABLE_VOICES['1']
        
        # Mock other functions
        with patch('speech_synthesis_custom_voice.get_voice_style', return_value='default'):
            with patch('speech_synthesis_custom_voice.get_voice_speed', return_value='medium'):
                with patch('speech_synthesis_custom_voice.preview_voice_settings'):
                    mock_input.return_value = 'n'  # User cancels
                    
                    with patch('sys.stdout', new=StringIO()) as fake_out:
                        speech_synthesis_custom_voice.main()
                        output = fake_out.getvalue()
                    
                    assert "Voice setup cancelled." in output

    @patch('builtins.input')
    @patch('speech_synthesis_custom_voice.get_text_input')
    @patch('speech_synthesis_custom_voice.setup_audio_config')
    @patch('speech_synthesis_custom_voice.get_user_output_preference')
    @patch('speech_synthesis_custom_voice.preview_voice_settings')
    @patch('speech_synthesis_custom_voice.get_voice_speed')
    @patch('speech_synthesis_custom_voice.get_voice_style')
    @patch('speech_synthesis_custom_voice.get_voice_selection')
    @patch('speech_synthesis_custom_voice.setup_speech_config')
    def test_main_user_quits_text_input(self, mock_setup_speech, mock_get_voice, 
                                       mock_get_style, mock_get_speed, mock_preview,
                                       mock_get_preference, mock_setup_audio, 
                                       mock_get_text, mock_input):
        """Test main function when user quits during text input."""
        # Setup mocks
        mock_setup_speech.return_value = Mock()
        mock_get_voice.return_value = speech_synthesis_custom_voice.AVAILABLE_VOICES['1']
        mock_get_style.return_value = 'default'
        mock_get_speed.return_value = 'medium'
        mock_get_preference.return_value = ('1', None)
        mock_setup_audio.return_value = Mock()
        mock_get_text.return_value = None  # User quits
        
        mock_input.return_value = 'y'  # Proceed with settings
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis_custom_voice.main()
            output = fake_out.getvalue()
        
        assert "Process cancelled by user." in output

    @patch('speech_synthesis_custom_voice.setup_speech_config')
    def test_main_configuration_error(self, mock_setup_speech):
        """Test main function with configuration error."""
        mock_setup_speech.side_effect = ValueError("Configuration error")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis_custom_voice.main()
            output = fake_out.getvalue()
        
        assert "❌ Configuration Error: Configuration error" in output
        assert "💡 Setup Instructions:" in output

    @patch('speech_synthesis_custom_voice.setup_speech_config')
    def test_main_unexpected_error(self, mock_setup_speech):
        """Test main function with unexpected error."""
        mock_setup_speech.side_effect = RuntimeError("Unexpected error")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis_custom_voice.main()
            output = fake_out.getvalue()
        
        assert "❌ An unexpected error occurred: Unexpected error" in output

    @patch('builtins.input')
    @patch('speech_synthesis_custom_voice.synthesize_speech_with_ssml')
    @patch('speech_synthesis_custom_voice.create_ssml_text')
    @patch('speech_synthesis_custom_voice.get_text_input')
    @patch('speech_synthesis_custom_voice.setup_audio_config')
    @patch('speech_synthesis_custom_voice.get_user_output_preference')
    @patch('speech_synthesis_custom_voice.preview_voice_settings')
    @patch('speech_synthesis_custom_voice.get_voice_speed')
    @patch('speech_synthesis_custom_voice.get_voice_style')
    @patch('speech_synthesis_custom_voice.get_voice_selection')
    @patch('speech_synthesis_custom_voice.setup_speech_config')
    def test_main_with_ssml_preview(self, mock_setup_speech, mock_get_voice, 
                                   mock_get_style, mock_get_speed, mock_preview,
                                   mock_get_preference, mock_setup_audio, 
                                   mock_get_text, mock_create_ssml, 
                                   mock_synthesize, mock_input):
        """Test main function with SSML preview enabled."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_voice_info = speech_synthesis_custom_voice.AVAILABLE_VOICES['1']
        
        mock_setup_speech.return_value = mock_speech_config
        mock_get_voice.return_value = mock_voice_info
        mock_get_style.return_value = 'default'
        mock_get_speed.return_value = 'medium'
        mock_get_preference.return_value = ('2', 'test.wav')
        mock_setup_audio.return_value = Mock()
        mock_get_text.return_value = "Test text"
        mock_create_ssml.return_value = "<speak>Test SSML</speak>"
        mock_synthesize.return_value = True
        
        # Mock input for confirmation and SSML preview
        mock_input.side_effect = ['y', 'y']  # Proceed with settings, show SSML preview
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis_custom_voice.main()
            output = fake_out.getvalue()
        
        # Verify SSML preview is shown
        assert "📋 Generated SSML:" in output
        assert "<speak>Test SSML</speak>" in output
        assert "✅ Custom voice speech synthesized and saved to: test.wav" in output

    @patch('builtins.input')
    @patch('speech_synthesis_custom_voice.synthesize_speech_with_ssml')
    @patch('speech_synthesis_custom_voice.create_ssml_text')
    @patch('speech_synthesis_custom_voice.get_text_input')
    @patch('speech_synthesis_custom_voice.setup_audio_config')
    @patch('speech_synthesis_custom_voice.get_user_output_preference')
    @patch('speech_synthesis_custom_voice.preview_voice_settings')
    @patch('speech_synthesis_custom_voice.get_voice_speed')
    @patch('speech_synthesis_custom_voice.get_voice_style')
    @patch('speech_synthesis_custom_voice.get_voice_selection')
    @patch('speech_synthesis_custom_voice.setup_speech_config')
    def test_main_synthesis_failure(self, mock_setup_speech, mock_get_voice, 
                                   mock_get_style, mock_get_speed, mock_preview,
                                   mock_get_preference, mock_setup_audio, 
                                   mock_get_text, mock_create_ssml, 
                                   mock_synthesize, mock_input):
        """Test main function with synthesis failure."""
        # Setup mocks
        mock_speech_config = Mock()
        mock_voice_info = speech_synthesis_custom_voice.AVAILABLE_VOICES['1']
        
        mock_setup_speech.return_value = mock_speech_config
        mock_get_voice.return_value = mock_voice_info
        mock_get_style.return_value = 'default'
        mock_get_speed.return_value = 'medium'
        mock_get_preference.return_value = ('1', None)
        mock_setup_audio.return_value = Mock()
        mock_get_text.return_value = "Test text"
        mock_create_ssml.return_value = "<speak>Test SSML</speak>"
        mock_synthesize.return_value = False  # Synthesis fails
        
        mock_input.side_effect = ['y', 'n']  # Proceed with settings, no SSML preview
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            speech_synthesis_custom_voice.main()
            output = fake_out.getvalue()
        
        assert "❌ Speech synthesis failed" in output

    def test_available_voices_structure(self):
        """Test that AVAILABLE_VOICES has the correct structure."""
        voices = speech_synthesis_custom_voice.AVAILABLE_VOICES
        
        # Should have 6 voices
        assert len(voices) == 6
        
        # Check each voice has required fields
        for key, voice in voices.items():
            assert 'name' in voice
            assert 'gender' in voice
            assert 'description' in voice
            assert 'styles' in voice
            assert isinstance(voice['styles'], list)
            assert len(voice['styles']) > 0
            assert 'default' in voice['styles']

    def test_long_text_truncation_in_main(self):
        """Test that long text is properly truncated in main function output."""
        long_text = "A" * 150  # 150 character text
        
        with patch('builtins.input') as mock_input:
            with patch('speech_synthesis_custom_voice.synthesize_speech_with_ssml', return_value=True):
                with patch('speech_synthesis_custom_voice.create_ssml_text', return_value="<speak>Test</speak>"):
                    with patch('speech_synthesis_custom_voice.get_text_input', return_value=long_text):
                        with patch('speech_synthesis_custom_voice.setup_audio_config', return_value=Mock()):
                            with patch('speech_synthesis_custom_voice.get_user_output_preference', return_value=('1', None)):
                                with patch('speech_synthesis_custom_voice.preview_voice_settings'):
                                    with patch('speech_synthesis_custom_voice.get_voice_speed', return_value='medium'):
                                        with patch('speech_synthesis_custom_voice.get_voice_style', return_value='default'):
                                            with patch('speech_synthesis_custom_voice.get_voice_selection', return_value=speech_synthesis_custom_voice.AVAILABLE_VOICES['1']):
                                                with patch('speech_synthesis_custom_voice.setup_speech_config', return_value=Mock()):
                                                    mock_input.side_effect = ['y', 'n']  # Proceed, no SSML preview
                                                    
                                                    with patch('sys.stdout', new=StringIO()) as fake_out:
                                                        speech_synthesis_custom_voice.main()
                                                        output = fake_out.getvalue()
                                                    
                                                    # Verify text is truncated with ellipsis
                                                    assert "A" * 100 + "..." in output