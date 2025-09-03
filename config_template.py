# Azure Speech Service Configuration Template
# Copy this file to config.py and fill in your actual values

# Azure Speech Service Credentials
SPEECH_KEY = "your-speech-service-key-here"
SPEECH_ENDPOINT = "https://your-region.api.cognitive.microsoft.com/"

# Voice Configuration
DEFAULT_VOICE = "en-US-AndrewMultilingualNeural"

# Available voices:
# Male voices:
# - en-US-AndrewMultilingualNeural
# - en-US-BrianMultilingualNeural
# 
# Female voices:
# - en-US-AvaMultilingualNeural
# - en-US-EmmaMultilingualNeural

# Output Settings
DEFAULT_OUTPUT_FOLDER = "output"  # Folder for saved audio files
DEFAULT_FILENAME_PREFIX = "speech_output"  # Prefix for generated files
