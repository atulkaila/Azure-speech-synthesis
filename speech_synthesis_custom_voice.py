#!/usr/bin/env python3
"""
Azure Speech Service Text-to-Speech Synthesis with Custom Voice Options

This enhanced script provides additional voice customization options including:
- Multiple voice selection
- Custom voice styles and emotions
- SSML support for advanced speech control
- Voice preview functionality

Features:
- Multiple neural voice options
- Voice style and emotion customization
- SSML (Speech Synthesis Markup Language) support
- Voice preview before synthesis
- Enhanced audio output options

Requirements:
- Python 3.7+
- azure-cognitiveservices-speech package
- Valid Azure Speech Service subscription

Author: Your Name
Date: September 3, 2025
Version: 2.0 - Enhanced with Custom Voice Options
"""

import os
import azure.cognitiveservices.speech as speechsdk

# Configuration Constants
# TODO: Replace these with your actual Azure Speech Service credentials
SPEECH_KEY = 'YOUR_SPEECH_SERVICE_KEY_HERE'
SPEECH_ENDPOINT = 'https://YOUR_REGION.api.cognitive.microsoft.com/'

# Available voices with their characteristics
AVAILABLE_VOICES = {
    '1': {
        'name': 'en-US-AndrewMultilingualNeural',
        'gender': 'Male',
        'description': 'Warm, friendly male voice with multilingual support',
        'styles': ['default', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering']
    },
    '2': {
        'name': 'en-US-AvaMultilingualNeural', 
        'gender': 'Female',
        'description': 'Natural, pleasant female voice with multilingual support',
        'styles': ['default', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering']
    },
    '3': {
        'name': 'en-US-BrianMultilingualNeural',
        'gender': 'Male',
        'description': 'Professional, clear male voice with multilingual support',
        'styles': ['default', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering']
    },
    '4': {
        'name': 'en-US-EmmaMultilingualNeural',
        'gender': 'Female', 
        'description': 'Expressive, versatile female voice with multilingual support',
        'styles': ['default', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering']
    },
    '5': {
        'name': 'en-US-JennyNeural',
        'gender': 'Female',
        'description': 'Conversational, natural female voice',
        'styles': ['default', 'assistant', 'chat', 'customerservice', 'newscast', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering']
    },
    '6': {
        'name': 'en-US-GuyNeural',
        'gender': 'Male',
        'description': 'Professional, authoritative male voice',
        'styles': ['default', 'newscast', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering']
    }
}

def setup_speech_config():
    """
    Initialize Azure Speech Service configuration.
    
    Returns:
        speechsdk.SpeechConfig: Configured speech service instance
        
    Raises:
        ValueError: If credentials are not properly configured
    """
    if SPEECH_KEY == 'YOUR_SPEECH_SERVICE_KEY_HERE':
        raise ValueError("Please configure your Azure Speech Service credentials in the script")
    
    speech_config = speechsdk.SpeechConfig(
        subscription=SPEECH_KEY,
        endpoint=SPEECH_ENDPOINT
    )
    
    return speech_config

def display_voice_options():
    """Display available voice options to the user."""
    print("\n" + "="*70)
    print("🎙️  AVAILABLE VOICE OPTIONS")
    print("="*70)
    
    for key, voice in AVAILABLE_VOICES.items():
        print(f"{key}. {voice['name']}")
        print(f"   Gender: {voice['gender']}")
        print(f"   Description: {voice['description']}")
        print(f"   Available Styles: {len(voice['styles'])} options")
        print("-" * 70)

def get_voice_selection():
    """
    Get user's voice selection.
    
    Returns:
        dict: Selected voice information
    """
    display_voice_options()
    
    while True:
        choice = input("\nSelect a voice (1-6): ").strip()
        if choice in AVAILABLE_VOICES:
            selected_voice = AVAILABLE_VOICES[choice]
            print(f"\n✓ Selected: {selected_voice['name']} ({selected_voice['gender']})")
            return selected_voice
        print("Invalid choice. Please select a number from 1-6.")

def get_voice_style(voice_info):
    """
    Get user's voice style selection.
    
    Args:
        voice_info (dict): Selected voice information
    
    Returns:
        str: Selected voice style
    """
    styles = voice_info['styles']
    
    print(f"\n🎨 VOICE STYLES for {voice_info['name']}")
    print("="*50)
    
    for i, style in enumerate(styles, 1):
        print(f"{i}. {style.title()}")
    
    print("\n💡 Tip: 'Default' provides the natural voice tone")
    print("🎭 Emotional styles: cheerful, excited, sad, friendly, etc.")
    
    while True:
        try:
            choice = input(f"\nSelect a style (1-{len(styles)}) or press Enter for default: ").strip()
            
            if not choice:  # Default selection
                return 'default'
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(styles):
                selected_style = styles[choice_idx]
                print(f"✓ Selected style: {selected_style.title()}")
                return selected_style
            else:
                print(f"Invalid choice. Please select a number from 1-{len(styles)}.")
        except ValueError:
            print("Please enter a valid number.")

def get_voice_speed():
    """
    Get user's preferred voice speed.
    
    Returns:
        str: Voice speed setting
    """
    speed_options = {
        '1': ('x-slow', 'Extra Slow'),
        '2': ('slow', 'Slow'),  
        '3': ('medium', 'Normal Speed'),
        '4': ('fast', 'Fast'),
        '5': ('x-fast', 'Extra Fast')
    }
    
    print(f"\n⚡ VOICE SPEED OPTIONS")
    print("="*30)
    
    for key, (speed, description) in speed_options.items():
        print(f"{key}. {description}")
    
    while True:
        choice = input("\nSelect speed (1-5) or press Enter for normal: ").strip()
        
        if not choice:  # Default selection
            return 'medium'
        
        if choice in speed_options:
            speed, description = speed_options[choice]
            print(f"✓ Selected speed: {description}")
            return speed
        
        print("Invalid choice. Please select a number from 1-5.")

def create_ssml_text(text, voice_name, style='default', speed='medium'):
    """
    Create SSML (Speech Synthesis Markup Language) text with custom voice settings.
    
    Args:
        text (str): Text to synthesize
        voice_name (str): Voice model name
        style (str): Voice style
        speed (str): Voice speed
    
    Returns:
        str: SSML formatted text
    """
    # Clean the text for SSML
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    ssml = f'''
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
           xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="{voice_name}">
    '''
    
    # Add style if not default
    if style != 'default':
        ssml += f'<mstts:express-as style="{style}">'
    
    # Add speed control
    ssml += f'<prosody rate="{speed}">{text}</prosody>'
    
    # Close style tag if used
    if style != 'default':
        ssml += '</mstts:express-as>'
    
    ssml += '''
        </voice>
    </speak>
    '''
    
    return ssml.strip()

def preview_voice_settings(voice_info, style, speed):
    """
    Show a preview of the selected voice settings.
    
    Args:
        voice_info (dict): Selected voice information
        style (str): Selected voice style
        speed (str): Selected voice speed
    """
    print("\n" + "🔍 VOICE PREVIEW")
    print("="*40)
    print(f"Voice: {voice_info['name']}")
    print(f"Gender: {voice_info['gender']}")
    print(f"Style: {style.title()}")
    print(f"Speed: {speed.title()}")
    print(f"Description: {voice_info['description']}")
    print("="*40)

def get_user_output_preference():
    """
    Prompt user for output preference (speakers or file).
    
    Returns:
        tuple: (choice, filename) where choice is '1' or '2', 
               and filename is provided if choice is '2'
    """
    print("\n" + "="*50)
    print("📤 OUTPUT OPTIONS")
    print("="*50)
    print("1. Play through speakers")
    print("2. Save to audio file")
    print("-"*50)
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    filename = None
    if choice == "2":
        while True:
            filename = input("Enter filename (without extension): ").strip()
            if filename:
                filename = filename + ".wav"
                break
            print("Filename cannot be empty.")
    
    return choice, filename

def setup_audio_config(choice, filename=None):
    """
    Configure audio output based on user preference.
    
    Args:
        choice (str): User's choice ('1' for speakers, '2' for file)
        filename (str, optional): Output filename for choice '2'
    
    Returns:
        speechsdk.audio.AudioOutputConfig: Configured audio output
    """
    if choice == "2" and filename:
        audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
        print(f"✓ Audio will be saved to: {filename}")
    else:
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        print("✓ Audio will play through speakers")
    
    return audio_config

def get_text_input():
    """
    Get text input from user for speech synthesis.
    
    Returns:
        str: Text to be converted to speech
    """
    print("\n" + "📝 TEXT INPUT")
    print("="*30)
    print("Enter your text for speech synthesis:")
    print("(Press Enter twice to finish, or type 'quit' to exit)")
    print("-"*30)
    
    lines = []
    while True:
        line = input("> ")
        if line.lower() == 'quit':
            return None
        if line == '' and lines:  # Empty line and we have some content
            break
        if line:  # Non-empty line
            lines.append(line)
    
    text = ' '.join(lines).strip()
    
    if not text:
        print("No text provided. Using default text.")
        text = "Hello! This is a demonstration of Azure Speech Services with custom voice options."
    
    return text

def synthesize_speech_with_ssml(speech_config, audio_config, ssml_text):
    """
    Perform text-to-speech synthesis using SSML.
    
    Args:
        speech_config (speechsdk.SpeechConfig): Speech service configuration
        audio_config (speechsdk.audio.AudioOutputConfig): Audio output configuration
        ssml_text (str): SSML formatted text to synthesize
    
    Returns:
        bool: True if synthesis was successful, False otherwise
    """
    try:
        # Create speech synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, 
            audio_config=audio_config
        )
        
        print(f"\n🔄 Synthesizing speech with custom voice settings...")
        
        # Perform synthesis using SSML
        speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_text).get()
        
        # Check results
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return True
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print(f"❌ Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print(f"Error details: {cancellation_details.error_details}")
                    print("💡 Check your voice settings and credentials")
            return False
        else:
            print(f"❌ Unexpected result: {speech_synthesis_result.reason}")
            return False
            
    except Exception as e:
        print(f"❌ An error occurred during synthesis: {e}")
        return False

def main():
    """
    Main function that orchestrates the text-to-speech process with custom voice options.
    """
    print("🎤 Azure Speech Service - Advanced Text-to-Speech with Custom Voices")
    print("=" * 80)
    
    try:
        # Setup speech configuration
        speech_config = setup_speech_config()
        
        # Get voice selection
        voice_info = get_voice_selection()
        
        # Get voice style
        voice_style = get_voice_style(voice_info)
        
        # Get voice speed
        voice_speed = get_voice_speed()
        
        # Show preview
        preview_voice_settings(voice_info, voice_style, voice_speed)
        
        # Confirm settings
        confirm = input("\nProceed with these settings? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes', '']:
            print("Voice setup cancelled.")
            return
        
        # Get output preferences
        choice, filename = get_user_output_preference()
        
        # Setup audio configuration
        audio_config = setup_audio_config(choice, filename)
        
        # Get text input
        text = get_text_input()
        if text is None:
            print("Process cancelled by user.")
            return
        
        # Create SSML with custom voice settings
        ssml_text = create_ssml_text(text, voice_info['name'], voice_style, voice_speed)
        
        # Show SSML preview (optional)
        show_ssml = input("\nShow SSML preview? (y/n): ").strip().lower()
        if show_ssml in ['y', 'yes']:
            print("\n📋 Generated SSML:")
            print("-" * 40)
            print(ssml_text)
            print("-" * 40)
        
        # Perform synthesis
        success = synthesize_speech_with_ssml(speech_config, audio_config, ssml_text)
        
        # Display results
        if success:
            if choice == "2":
                print(f"✅ Custom voice speech synthesized and saved to: {filename}")
            else:
                print(f"✅ Custom voice speech synthesized and played through speakers")
            
            print(f"🎙️  Voice: {voice_info['name']} ({voice_info['gender']})")
            print(f"🎨 Style: {voice_style.title()}")
            print(f"⚡ Speed: {voice_speed.title()}")
            print(f"📄 Text: '{text[:100]}{'...' if len(text) > 100 else ''}'")
        else:
            print("❌ Speech synthesis failed. Please check your configuration and try again.")
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Setup Instructions:")
        print("1. Create an Azure Speech Service resource in Azure Portal")
        print("2. Copy your subscription key and endpoint")
        print("3. Replace the placeholder values in this script")
        
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 Thank you for using Azure Speech Service with Custom Voices!")

if __name__ == "__main__":
    main()
