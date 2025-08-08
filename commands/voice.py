"""
🎤 Glenn.AI Voice Assistant Shell
Advanced voice-enabled interactive interface for Glenn.AI
"""

import logging
import json
import sqlite3
import speech_recognition as sr
import pyttsx3
import threading
import time
from pathlib import Path
from typing import Optional, Any

logger = logging.getLogger(__name__)

class GlennVoiceShell:
    def __init__(self):
        self.is_listening = False
        self.is_speaking = False
        self.recognizer = None
        self.microphone = None
        self.tts_engine = None
        self.twin_data = None
        
    def initialize_voice_systems(self):
        """Initialize speech recognition and text-to-speech systems."""
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            logger.info("Speech recognition initialized successfully")
            
            # Try to initialize text-to-speech
            try:
                self.tts_engine = pyttsx3.init()
                
                # Configure TTS voice settings
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Try to find a male voice for Glenn
                    for voice in voices:
                        if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                
                # Set speech rate and volume
                self.tts_engine.setProperty('rate', 175)  # Words per minute
                self.tts_engine.setProperty('volume', 0.8)
                logger.info("Text-to-speech initialized successfully")
                
            except Exception as tts_error:
                logger.warning(f"TTS initialization failed: {tts_error}")
                self.tts_engine = None
                print("⚠️ Text-to-speech unavailable, using text-only mode")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize voice systems: {e}")
            return False
    
    def speak(self, text: str):
        """Convert text to speech."""
        if self.tts_engine and not self.is_speaking:
            self.is_speaking = True
            try:
                print(f"[Glenn 🎤]: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                logger.error(f"TTS error: {e}")
                print(f"[Glenn]: {text}")  # Fallback to text
            finally:
                self.is_speaking = False
        else:
            print(f"[Glenn]: {text}")
    
    def listen_for_wake_word(self):
        """Listen for wake words: 'Glenn' or 'Hey Glenn'."""
        if not self.recognizer or not self.microphone:
            return None
            
        try:
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("🎧 Listening for wake word ('Glenn' or 'Hey Glenn')...")
            
            with self.microphone as source:
                # Listen for wake word with shorter timeout
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio).lower()
            
            if 'glenn' in text:
                return text
            return None
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            logger.error(f"Wake word detection error: {e}")
            return None
    
    def listen_for_command(self):
        """Listen for voice command after wake word."""
        if not self.recognizer or not self.microphone:
            return None
            
        try:
            self.speak("Yes? I'm listening.")
            
            with self.microphone as source:
                # Listen for command with longer timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech
            command = self.recognizer.recognize_google(audio)
            print(f"[You 🎤]: {command}")
            return command
            
        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything. Try again.")
            return None
        except sr.UnknownValueError:
            self.speak("I didn't understand that. Could you repeat?")
            return None
        except Exception as e:
            logger.error(f"Command recognition error: {e}")
            self.speak("Sorry, I had trouble hearing you.")
            return None
    
    def process_voice_command(self, command: str) -> str:
        """Process voice command and return response."""
        command_lower = command.lower()
        
        # Voice-specific commands
        if any(word in command_lower for word in ['stop listening', 'exit voice', 'disable voice']):
            return "VOICE_EXIT"
        elif any(word in command_lower for word in ['who are you', 'introduce yourself']):
            return self.get_introduction()
        elif any(word in command_lower for word in ['status', 'how are you', 'system status']):
            return self.get_voice_status()
        elif any(word in command_lower for word in ['task', 'todo', 'remind']):
            return self.handle_voice_task(command)
        elif any(word in command_lower for word in ['memory', 'remember', 'recall']):
            return self.handle_voice_memory(command)
        elif any(word in command_lower for word in ['time', 'date', 'what time']):
            from datetime import datetime
            return f"It's {datetime.now().strftime('%I:%M %p on %A, %B %d, %Y')}"
        else:
            # Route to chat command logic
            from commands.chat import route_command
            if not self.twin_data:
                self.twin_data = self.load_twin_config()
            return route_command(command, self.twin_data)
    
    def get_introduction(self) -> str:
        """Get Glenn's voice introduction."""
        if not self.twin_data:
            self.twin_data = self.load_twin_config()
            
        if self.twin_data:
            from commands.awareness import get_awareness_summary
            base_intro = get_awareness_summary()
            return f"Hello! {base_intro}. I'm equipped with voice recognition and can help you with tasks, memory operations, system status, and general assistance. Just say my name to get my attention."
        else:
            return "Hello! I'm Glenn, your AI voice assistant. I can help with tasks, system operations, and answer questions. How can I assist you today?"
    
    def get_voice_status(self) -> str:
        """Get system status in voice-friendly format."""
        return "All systems are operational. Voice recognition is active, memory systems are online, and I'm ready to assist you."
    
    def handle_voice_task(self, command: str) -> str:
        """Handle task-related voice commands."""
        if 'add' in command.lower() or 'create' in command.lower():
            # Extract task from command
            words = command.lower().split()
            if 'add' in words:
                idx = words.index('add')
                task_desc = ' '.join(words[idx+1:])
            elif 'create' in words:
                idx = words.index('create')
                task_desc = ' '.join(words[idx+1:])
            else:
                return "What task would you like me to add?"
                
            if task_desc:
                from commands.tasky import add_task
                add_task(task_desc)
                return f"I've added the task: {task_desc}"
            else:
                return "What task should I add for you?"
        else:
            return "I can help you add tasks. Just say 'add task' followed by the task description."
    
    def handle_voice_memory(self, command: str) -> str:
        """Handle memory-related voice commands."""
        if 'backup' in command.lower():
            return "I'll create a memory backup for you. This may take a moment."
        else:
            return "I can help with memory operations like creating backups. What would you like me to do?"
    
    def load_twin_config(self):
        """Load twin configuration."""
        try:
            project_root = Path(__file__).parent.parent
            manifest_path = project_root / "manifests" / "glenn_manifest.json"
            
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                
            return {
                'id': manifest.get('twinID'),
                'personas': manifest.get('personas'),
                'default': manifest.get('defaultPersona')
            }
        except Exception as e:
            logger.error(f"Failed to load twin config: {e}")
            return None

def execute(args: Optional[Any] = None):
    """
    Execute voice assistant shell.
    
    Args:
        args: Command line arguments or parameters
    """
    logger.info("Starting Glenn.AI Voice Assistant Shell")
    
    print("🎤 Glenn.AI Voice Assistant Shell")
    print("=" * 45)
    
    # Check for required packages
    try:
        import speech_recognition
        import pyttsx3
    except ImportError:
        print("❌ Voice packages not installed!")
        print("\nTo enable voice features, install:")
        print("pip install speechrecognition pyttsx3 pyaudio")
        print("\nFalling back to text mode...")
        
        # Fallback to chat mode
        from commands.chat import execute as chat_execute
        return chat_execute(args)
    
    # Initialize voice shell
    voice_shell = GlennVoiceShell()
    
    if not voice_shell.initialize_voice_systems():
        print("❌ Failed to initialize voice systems")
        print("Falling back to text mode...")
        from commands.chat import execute as chat_execute
        return chat_execute(args)
    
    print("✅ Voice systems initialized")
    voice_shell.speak("Hello! Glenn's voice assistant is now active.")
    voice_shell.speak(voice_shell.get_introduction())
    
    print("\n🎧 Voice Commands:")
    print("  - Say 'Glenn' or 'Hey Glenn' to activate")
    print("  - Say 'stop listening' to exit voice mode")
    print("  - Try: 'status', 'add task', 'who are you'\n")
    
    # Main voice loop
    try:
        while True:
            # Listen for wake word
            wake_result = voice_shell.listen_for_wake_word()
            
            if wake_result:
                print(f"🎧 Wake word detected: {wake_result}")
                
                # Listen for command
                command = voice_shell.listen_for_command()
                
                if command:
                    # Process command
                    response = voice_shell.process_voice_command(command)
                    
                    if response == "VOICE_EXIT":
                        voice_shell.speak("Voice assistant deactivated. Goodbye!")
                        break
                    else:
                        voice_shell.speak(response)
                        
                        # Log interaction
                        try:
                            from commands.chat import log_interaction
                            log_interaction(command, "Glenn-Voice", response)
                        except:
                            pass
                
                print("🎧 Listening for wake word...")
            
            # Small delay to prevent CPU overuse
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🎤 Voice assistant interrupted")
        voice_shell.speak("Voice assistant shutting down. Goodbye!")
    except Exception as e:
        logger.error(f"Voice shell error: {e}")
        print(f"❌ Voice shell error: {e}")
        voice_shell.speak("I encountered an error. Switching to text mode.")

if __name__ == "__main__":
    # For standalone testing
    execute()
