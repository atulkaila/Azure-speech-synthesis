#!/usr/bin/env python3
"""
Azure Speech Service Text-to-Speech Synthesis

This script provides a simple interface for converting text to speech using Azure Cognitive Services.
It supports both audio playback through speakers and saving audio to WAV files.

Features:
- Text-to-speech conversion using Azure Speech Services
- Multiple output options (speakers or file)
- Neural voice support with multilingual capabilities
- User-friendly command-line interface

Requirements:
- Python 3.7+
- azure-cognitiveservices-speech package
- Valid Azure Speech Service subscription

Setup Instructions:
1. Install required package: pip install azure-cognitiveservices-speech
2. Create an Azure Speech Service resource in Azure Portal
3. Replace SPEECH_KEY and SPEECH_ENDPOINT with your credentials
4. Run the script: python speech_synthesis.py

Author: Your Name
Date: September 3, 2025
Version: 1.0
"""

import os
import azure.cognitiveservices.speech as speechsdk

# Configuration Constants
# TODO: Replace these with your actual Azure Speech Service credentials
SPEECH_KEY = 'YOUR_SPEECH_SERVICE_KEY_HERE'
SPEECH_ENDPOINT = 'https://YOUR_REGION.api.cognitive.microsoft.com/'
DEFAULT_VOICE = 'en-US-AndrewMultilingualNeural'

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
    
    # Set the voice model
    # Available multilingual voices:
    # - en-US-AndrewMultilingualNeural (male)
    # - en-US-AvaMultilingualNeural (female)
    speech_config.speech_synthesis_voice_name = DEFAULT_VOICE
    
    return speech_config

def get_user_output_preference():
    """
    Prompt user for output preference (speakers or file).
    
    Returns:
        tuple: (choice, filename) where choice is '1' or '2', 
               and filename is provided if choice is '2'
    """
    print("\n" + "="*50)
    print("Azure Speech Synthesis - Output Options")
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
    print("\n" + "-"*50)
    print("Enter text for speech synthesis:")
    print("-"*50)
    text = input("> ").strip()
    
    if not text:
        print("No text provided. Using default text.")
        text = "Hello! This is a test of Azure Speech Services."
    
    return text

def synthesize_speech(speech_config, audio_config, text):
    """
    Perform text-to-speech synthesis.
    
    Args:
        speech_config (speechsdk.SpeechConfig): Speech service configuration
        audio_config (speechsdk.audio.AudioOutputConfig): Audio output configuration
        text (str): Text to synthesize
    
    Returns:
        bool: True if synthesis was successful, False otherwise
    """
    try:
        # Create speech synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, 
            audio_config=audio_config
        )
        
        print(f"\n🔄 Synthesizing speech for: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        # Perform synthesis
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
        
        # Check results
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return True
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print(f"❌ Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print(f"Error details: {cancellation_details.error_details}")
                    print("💡 Did you set the speech resource key and endpoint values?")
            return False
        else:
            print(f"❌ Unexpected result: {speech_synthesis_result.reason}")
            return False
            
    except Exception as e:
        print(f"❌ An error occurred during synthesis: {e}")
        return False

def main():
    """
    Main function that orchestrates the text-to-speech process.
    """
    print("🎤 Azure Speech Service - Text-to-Speech Synthesis")
    print("=" * 60)
    
    try:
        # Setup speech configuration
        speech_config = setup_speech_config()
        
        # Get user preferences
        choice, filename = get_user_output_preference()
        
        # Setup audio configuration
        audio_config = setup_audio_config(choice, filename)
        
        # Get text input
        text = get_text_input()
        
        # Perform synthesis
        success = synthesize_speech(speech_config, audio_config, text)
        
        # Display results
        if success:
            if choice == "2":
                print(f"✅ Speech synthesized and saved to file: {filename}")
                print(f"📄 Text: '{text}'")
            else:
                print(f"✅ Speech synthesized and played through speakers")
                print(f"📄 Text: '{text}'")
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
    
    print("\n" + "=" * 60)
    print("Thank you for using Azure Speech Service!")

if __name__ == "__main__":
    main()
