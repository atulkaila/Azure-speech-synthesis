# Azure Speech Service - Text-to-Speech Synthesis

A simple Python application that converts text to speech using Azure Cognitive Services Speech API. This tool supports both audio playback through speakers and saving audio to WAV files.

## 🎯 Features

- **Text-to-Speech Conversion**: Convert any text to natural-sounding speech
- **Multiple Output Options**: Play through speakers or save to WAV file
- **Neural Voice Support**: Uses high-quality neural voices with multilingual capabilities
- **Custom Voice Options**: Choose from 6 different voice personalities
- **Voice Styles & Emotions**: Apply different emotional styles (cheerful, sad, excited, etc.)
- **Speed Control**: Adjust speech speed from extra slow to extra fast
- **SSML Support**: Advanced speech control with Speech Synthesis Markup Language
- **User-Friendly Interface**: Simple command-line interface with clear prompts
- **Error Handling**: Comprehensive error handling with helpful messages
- **Easy Setup**: Automated setup script for quick configuration

## 📋 Requirements

- **Python 3.7+**
- **Azure Speech Service subscription**
- **Internet connection** for API calls

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install azure-cognitiveservices-speech
```

### 2. Create Azure Speech Service Resource

1. Go to the [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Speech"
4. Select "Speech" service
5. Fill in the required details:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Region**: Choose a region close to you (e.g., East US)
   - **Name**: Give your resource a unique name
   - **Pricing Tier**: F0 (Free) or S0 (Standard)
6. Click "Review + Create" then "Create"

### 3. Get Your Credentials

1. Go to your Speech resource in Azure Portal
2. Click on "Keys and Endpoint" in the left menu
3. Copy **Key 1** and **Endpoint**

### 4. Configure the Script

1. Open `speech_synthesis.py`
2. Replace the placeholder values:

```python
# Replace these with your actual values
SPEECH_KEY = 'your-speech-service-key-here'
SPEECH_ENDPOINT = 'https://your-region.api.cognitive.microsoft.com/'
```

### 5. Run the Application

```bash
python speech_synthesis.py
```

## 💡 Usage

### Option 1: Quick Setup (Recommended)
```bash
python setup.py
```
This will guide you through the entire setup process automatically.

### Option 2: Manual Setup

1. **Run the basic version**: `python speech_synthesis.py`
2. **Run the advanced version with custom voices**: `python speech_synthesis_custom_voice.py`
3. **Run the simple example**: `python example_simple.py`

### Usage Flow:

1. **Choose your script**:
   - `speech_synthesis.py` - Basic version with standard options
   - `speech_synthesis_custom_voice.py` - Advanced version with voice customization
   - `example_simple.py` - Minimal example for testing

2. **Select voice options** (advanced version):
   - Choose from 6 different voice personalities
   - Select emotional style (cheerful, excited, sad, etc.)
   - Adjust speech speed (slow to fast)

3. **Choose output method**:
   - Option 1: Play through speakers
   - Option 2: Save to audio file

4. **Enter your text** and enjoy the results!

## 🎙️ Available Voices

The advanced script (`speech_synthesis_custom_voice.py`) supports multiple neural voices:

### Male Voices:
- **en-US-AndrewMultilingualNeural** - Warm, friendly with multilingual support
- **en-US-BrianMultilingualNeural** - Professional, clear with multilingual support  
- **en-US-GuyNeural** - Professional, authoritative

### Female Voices:
- **en-US-AvaMultilingualNeural** - Natural, pleasant with multilingual support
- **en-US-EmmaMultilingualNeural** - Expressive, versatile with multilingual support
- **en-US-JennyNeural** - Conversational, natural

### Voice Styles Available:
- **Default** - Natural voice tone
- **Emotional Styles**: cheerful, excited, friendly, hopeful, sad, terrified, unfriendly
- **Communication Styles**: whispering, shouting
- **Professional Styles**: assistant, chat, customerservice, newscast (select voices)

### Speed Options:
- Extra Slow, Slow, Normal, Fast, Extra Fast

To change the voice in the basic script, modify the `DEFAULT_VOICE` variable:

```python
DEFAULT_VOICE = 'en-US-AvaMultilingualNeural'  # Female voice
```

## 📝 Example Output

```
🎤 Azure Speech Service - Text-to-Speech Synthesis
============================================================

==================================================
Azure Speech Synthesis - Output Options
==================================================
1. Play through speakers
2. Save to audio file
--------------------------------------------------
Enter your choice (1 or 2): 2
Enter filename (without extension): hello_world
✓ Audio will be saved to: hello_world.wav

--------------------------------------------------
Enter text for speech synthesis:
--------------------------------------------------
> Hello, welcome to Azure Speech Services!

🔄 Synthesizing speech for: 'Hello, welcome to Azure Speech Services!'
✅ Speech synthesized and saved to file: hello_world.wav
📄 Text: 'Hello, welcome to Azure Speech Services!'

============================================================
Thank you for using Azure Speech Service!
```

## 🔧 Customization

### Custom Voices

You can explore more voices by checking the [Azure Speech Service documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#neural-voices). To use a different voice:

1. Find the voice name from the documentation
2. Update the `DEFAULT_VOICE` variable
3. Run the script

### Custom Voice with SSML

For advanced voice customization, you can modify the script to use SSML (Speech Synthesis Markup Language):

```python
# Example SSML for custom voice effects
ssml_text = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-AndrewMultilingualNeural">
        <prosody rate="medium" pitch="medium">
            Hello, this is a customized voice!
        </prosody>
    </voice>
</speak>
"""
```

## 🛠️ Troubleshooting

### Common Issues

**1. Authentication Errors**
```
Error: Invalid subscription key or endpoint
```
- Solution: Verify your `SPEECH_KEY` and `SPEECH_ENDPOINT` are correct
- Check that your Azure Speech resource is active

**2. Network Connection Issues**
```
Error: Failed to connect to service
```
- Solution: Check your internet connection
- Verify the endpoint URL is correct for your region

**3. Package Installation Issues**
```
ModuleNotFoundError: No module named 'azure.cognitiveservices.speech'
```
- Solution: Install the package: `pip install azure-cognitiveservices-speech`

**4. File Permission Issues**
```
Error: Cannot write to file
```
- Solution: Ensure you have write permissions in the current directory
- Try running with administrator privileges if needed

## 📚 Additional Resources

- [Azure Speech Service Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [Supported Languages and Voices](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support)
- [Python SDK Reference](https://docs.microsoft.com/en-us/python/api/overview/azure/cognitiveservices-speech-readme)
- [SSML Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup)

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## 📄 License

This project is open source. Feel free to use and modify as needed.

## � Project Structure

```
Azure-Speech-Synthesis/
├── speech_synthesis.py              # Main script with basic features
├── speech_synthesis_custom_voice.py # Advanced script with voice customization
├── example_simple.py                # Simple example for quick testing
├── setup.py                        # Automated setup script
├── requirements.txt                 # Python dependencies
├── config_template.py               # Configuration template
├── README.md                       # This file
├── .gitignore                      # Git ignore file
└── output/                         # Generated audio files (created automatically)
```

## �🔮 Future Enhancements

- [ ] Support for SSML (Speech Synthesis Markup Language) ✅ **COMPLETED**
- [ ] Batch processing of multiple text files
- [ ] GUI interface using tkinter
- [ ] Voice customization options ✅ **COMPLETED**
- [ ] Support for multiple output formats (MP3, OGG)
- [ ] Real-time text-to-speech from clipboard

---

**Happy coding! 🎉**
