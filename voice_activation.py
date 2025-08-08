"""
🎤 Voice Command Integration for Glenn.AI
Integrates voice assistant with main command system
"""

import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def activate_voice_shell():
    """Activate Glenn's voice assistant shell."""
    print("🎧 Activating Glenn's Voice Assistant...")
    
    try:
        # Import and start voice assistant
        from voice.assistant import GlennVoiceAssistant
        
        assistant = GlennVoiceAssistant()
        
        # Check if voice dependencies are available
        status = assistant.get_status()
        
        # Try to initialize if not already done
        if not status['wake_detector_available']:
            print("🔧 Initializing voice components...")
            if not assistant.initialize():
                print("❌ Speech recognition not available. Please install voice dependencies:")
                print("   pip install -r requirements_voice.txt")
                return False
        
        # Check status again after initialization
        status = assistant.get_status()
        if not status['wake_detector_available']:
            print("❌ Speech recognition not available. Please install voice dependencies:")
            print("   pip install -r requirements_voice.txt")
            return False
        
        # Start voice assistant
        print("🎤 Starting voice recognition...")
        assistant.start_blocking()
        
        return True
        
    except ImportError as e:
        print(f"❌ Voice system import error: {e}")
        print("📦 Please install voice dependencies:")
        print("   pip install -r requirements_voice.txt")
        return False
    
    except Exception as e:
        print(f"❌ Voice activation error: {e}")
        return False

def check_voice_dependencies():
    """Check if voice dependencies are installed."""
    try:
        import speechrecognition
        import pyttsx3
        import pyaudio
        return True
    except ImportError:
        return False

def install_voice_dependencies():
    """Install voice dependencies."""
    import subprocess
    
    print("📦 Installing voice dependencies...")
    
    try:
        # Install from requirements file
        requirements_file = Path(__file__).parent / "requirements_voice.txt"
        
        if requirements_file.exists():
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "-r", str(requirements_file)
            ])
        else:
            # Fallback to individual packages
            packages = [
                "speechrecognition>=3.10.0",
                "pyttsx3>=2.90", 
                "pyaudio>=0.2.11"
            ]
            
            for package in packages:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ])
        
        print("✅ Voice dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("\n🔧 Manual installation steps:")
        print("1. pip install speechrecognition")
        print("2. pip install pyttsx3")
        print("3. pip install pyaudio")
        print("\n⚠️  PyAudio may require system dependencies:")
        print("   Windows: Visual C++ Build Tools")
        print("   macOS: brew install portaudio")
        print("   Linux: sudo apt-get install python3-pyaudio")
        return False

if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "install":
            install_voice_dependencies()
        elif command == "check":
            if check_voice_dependencies():
                print("✅ Voice dependencies are installed")
            else:
                print("❌ Voice dependencies missing")
        else:
            print("Usage: python voice_activation.py [install|check]")
    else:
        # Default: activate voice assistant
        activate_voice_shell()
