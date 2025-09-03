#!/usr/bin/env python3
"""
Simple Example - Azure Speech Service Text-to-Speech

This is a minimal example showing how to use the Azure Speech Service
for text-to-speech conversion. Perfect for quick testing and learning.

Usage:
    python example_simple.py
"""

import azure.cognitiveservices.speech as speechsdk

def simple_text_to_speech():
    """
    Simple text-to-speech example.
    Replace the credentials with your actual values.
    """
    
    # TODO: Replace with your actual credentials
    SPEECH_KEY = "YOUR_SPEECH_SERVICE_KEY_HERE"
    SPEECH_ENDPOINT = "https://YOUR_REGION.api.cognitive.microsoft.com/"
    
    if SPEECH_KEY == "YOUR_SPEECH_SERVICE_KEY_HERE":
        print("❌ Please configure your Azure Speech Service credentials")
        print("Edit this file and replace SPEECH_KEY and SPEECH_ENDPOINT")
        return
    
    # Configure speech service
    speech_config = speechsdk.SpeechConfig(
        subscription=SPEECH_KEY,
        endpoint=SPEECH_ENDPOINT
    )
    
    # Set voice (optional)
    speech_config.speech_synthesis_voice_name = "en-US-AndrewMultilingualNeural"
    
    # Configure audio output to default speakers
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    
    # Create synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, 
        audio_config=audio_config
    )
    
    # Text to convert
    text = "Hello! This is a simple example of Azure Speech Services. Welcome to text-to-speech synthesis!"
    
    print(f"🔄 Converting text to speech: '{text}'")
    
    # Perform synthesis
    try:
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("✅ Speech synthesis completed successfully!")
        elif result.reason == speechsdk.ResultReason.Canceled:
            print(f"❌ Speech synthesis was canceled: {result.cancellation_details.reason}")
            if result.cancellation_details.error_details:
                print(f"Error details: {result.cancellation_details.error_details}")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    print("🎤 Simple Azure Speech Service Example")
    print("=" * 40)
    simple_text_to_speech()
    print("=" * 40)
