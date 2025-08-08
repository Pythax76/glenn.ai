
GLENN.AI

## 🧠 Overview

**Glenn.AI** is a modular digital twin built to extend the capabilities of Jason Lawrence (J-Law), a cybersecurity and systems automation professional. It blends identity, memory, task routing, and synthetic AI personas to create a persistent, evolving co-pilot across both professional and personal contexts.

This repository serves as the home for Glenn's configuration, codebase, memory engine, persona modules, and **voice assistant capabilities**.

---

## ⚙️ Core Capabilities

- **Persona-Oriented AI Routing**: Modular sub-agents (Echo, Tasky, API_Guy, Spock, BUB0, Kunda_AI) handle specialized functions via command delegation.
- **Persistent Profile**: Glenn operates with a live JSON-based profile and memory system, versioned and synced locally.
- **Voice Assistant**: Complete voice interface with wake word detection, speech-to-text, text-to-speech, and natural language command processing.
- **Compliance Ready**: Engineered with ISO 27001, CMMC, and NIST 800-53 alignment via the Spock persona.
- **Multi-Interface Control**: Supports CLI interfaces, Flask integration, and voice command control.

---

## 🧩 Structure

```shell
glenn/
├── manifests/             # Activation schema + routing manifest
│   └── glenn_manifest.json
├── profiles/              # Core identity and skillset
│   └── digital_twin.json
├── core/                  # Routing, memory sync, twin loader
│   ├── twin_loader.py
│   ├── memory_sync.py
│   ├── persona_router.py
│   └── logger.py
├── agents/                # Specialized personas (AI modules)
│   ├── echo.py
│   ├── tasky.py
│   ├── spock.py
│   └── api_guy.py
├── voice/                 # Voice assistant system
│   ├── __init__.py
│   ├── assistant.py       # Main voice orchestrator
│   ├── wake_words.py      # Wake word detection
│   ├── speech_to_text.py  # Speech recognition
│   ├── text_to_speech.py  # Speech synthesis
│   └── voice_commands.py  # Command parsing & routing
├── storage/               # Local memory DB and logs
│   └── glenn_memory.db
├── voice_activation.py    # Voice system integration
├── test_voice.py          # Voice system test suite
├── requirements_voice.txt # Voice dependencies
├── README.md
└── main.py                # System entry point
```

---

## 🎤 Voice Assistant

Glenn.AI includes a complete voice assistant system with:

### Features
- **Wake Word Detection**: Responds to "Glenn", "Hey Glenn", etc.
- **Speech Recognition**: Converts speech to text using Google Speech API with offline fallback
- **Text-to-Speech**: Natural voice responses with configurable voice personalities
- **Command Processing**: Natural language command parsing with pattern matching
- **System Integration**: Seamlessly integrates with all existing Glenn.AI personas and functions

### Voice Commands
- **"status"** - Get system status
- **"who are you"** - Identity and awareness summary
- **"add task [description]"** - Add tasks to the task system
- **"what time is it"** - Current time
- **"stop listening"** - Exit voice mode

### Quick Start - Voice Mode

1. **Install voice dependencies:**
   ```bash
   pip install -r requirements_voice.txt
   ```

2. **Test voice system:**
   ```bash
   python test_voice.py
   ```

3. **Activate voice assistant:**
   ```bash
   python main.py voice
   # or
   python voice_activation.py
   ```

4. **Use voice commands:**
   - Say "Glenn" or "Hey Glenn" to activate
   - Speak your command when prompted
   - Say "stop listening" to exit

### Voice System Architecture

The voice system is built with a modular architecture:

- **`voice/assistant.py`**: Main orchestrator handling the voice loop
- **`voice/wake_words.py`**: Detects wake words to activate listening
- **`voice/speech_to_text.py`**: Converts spoken audio to text
- **`voice/text_to_speech.py`**: Converts responses to spoken audio
- **`voice/voice_commands.py`**: Parses and routes voice commands

### System Requirements

**Voice Dependencies:**
- `speechrecognition>=3.10.0` - Speech recognition framework
- `pyttsx3>=2.90` - Text-to-speech engine
- `pyaudio>=0.2.11` - Audio processing

**Platform-Specific Setup:**
- **Windows**: Requires Microsoft Visual C++ 14.0+ Build Tools
- **macOS**: `brew install portaudio`
- **Linux**: `sudo apt-get install python3-pyaudio portaudio19-dev espeak`

---

## 🚀 Quick Start - Text Mode

1. **Clone the repository:**
   ```bash
   git clone [repository-url]
   cd glenn
   ```

2. **Run Glenn.AI:**
   ```bash
   python main.py
   ```

3. **Start chatting:**
   ```
   [You]: status
   [Glenn]: All systems operational. Digital twin active and ready for commands.
   
   [You]: add task review security documentation
   [Glenn]: Task added successfully: review security documentation
   
   [You]: voice
   🎧 Switching to voice mode...
   ```

---
