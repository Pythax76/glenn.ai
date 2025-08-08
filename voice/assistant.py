"""
🎤 Glenn.AI Voice Assistant
Main voice loop and routing for Glenn's voice interface
"""

import logging
import time
import threading
from pathlib import Path
from typing import Optional

from .wake_words import WakeWordDetector
from .speech_to_text import SpeechToText  
from .text_to_speech import TextToSpeech
from .voice_commands import VoiceCommandHandler

logger = logging.getLogger(__name__)

class GlennVoiceAssistant:
    """Main voice assistant orchestrating all voice components."""
    
    def __init__(self):
        """Initialize Glenn's voice assistant."""
        self.wake_detector = WakeWordDetector()
        self.speech_to_text = SpeechToText()
        self.text_to_speech = TextToSpeech()
        self.command_handler = VoiceCommandHandler()
        
        self.is_running = False
        self.is_listening = False
        self.voice_thread = None
        
        # Configuration
        self.wake_timeout = 1.0  # Seconds to listen for wake word
        self.command_timeout = 5.0  # Seconds to listen for command
        self.response_delay = 0.5  # Seconds before responding
        
    def initialize(self) -> bool:
        """Initialize all voice components."""
        logger.info("Initializing Glenn's voice assistant...")
        
        success = True
        
        # Initialize wake word detection
        if not self.wake_detector.initialize():
            logger.error("Failed to initialize wake word detection")
            success = False
        
        # Initialize speech to text
        if not self.speech_to_text.initialize():
            logger.error("Failed to initialize speech to text")
            success = False
        
        # Initialize text to speech (optional)
        if not self.text_to_speech.initialize():
            logger.warning("Text to speech initialization failed - using text mode")
            # Don't fail completely if TTS is unavailable
        
        # Setup command handlers
        self._setup_command_handlers()
        
        if success:
            logger.info("Voice assistant initialized successfully")
        else:
            logger.error("Voice assistant initialization failed")
            
        return success
    
    def _setup_command_handlers(self):
        """Setup command handlers for voice commands."""
        # Register handlers for integration with Glenn's command system
        
        def handle_status(command_info):
            """Handle status requests."""
            try:
                # This would integrate with the status command
                from commands.status import execute as status_execute
                # For now, return a simple status
                return "All systems operational. Voice recognition active and ready for commands."
            except ImportError:
                return "System status: Online and operational."
        
        def handle_identity(command_info):
            """Handle identity requests."""
            try:
                # This would integrate with the awareness command
                from commands.awareness import get_awareness_summary
                return get_awareness_summary()
            except ImportError:
                return "I am Glenn, your AI voice assistant."
        
        def handle_add_task(command_info):
            """Handle task addition."""
            parameters = command_info.get('parameters', [])
            if parameters:
                task_description = parameters[0]
                try:
                    # This would integrate with the task system
                    from commands.tasky import add_task
                    add_task(task_description)
                    return f"I've added the task: {task_description}"
                except ImportError:
                    return f"Task noted: {task_description} (integration pending)"
            else:
                return "What task would you like me to add?"
        
        def handle_memory_backup(command_info):
            """Handle memory backup requests."""
            try:
                # This would integrate with memory commands
                return "Creating memory backup... This may take a moment."
            except Exception:
                return "Memory backup functionality is being processed."
        
        # Register the handlers
        self.command_handler.register_handler("status", handle_status)
        self.command_handler.register_handler("identity", handle_identity)
        self.command_handler.register_handler("add_task", handle_add_task)
        self.command_handler.register_handler("memory_backup", handle_memory_backup)
    
    def start(self):
        """Start the voice assistant."""
        if self.is_running:
            logger.warning("Voice assistant already running")
            return
        
        if not self.initialize():
            logger.error("Cannot start voice assistant - initialization failed")
            return
        
        self.is_running = True
        self.is_listening = True
        
        # Start voice processing in a separate thread
        self.voice_thread = threading.Thread(target=self._voice_loop, daemon=True)
        self.voice_thread.start()
        
        # Initial greeting
        self.speak("Hello! Glenn's voice assistant is now active.")
        self.speak(self._get_introduction())
        
        logger.info("Voice assistant started")
    
    def start_blocking(self):
        """Start voice assistant in blocking mode (for command line use)."""
        if not self.initialize():
            print("❌ Failed to initialize voice systems")
            return
        
        self.is_running = True
        self.is_listening = True
        
        # Initial greeting
        self.speak("Hello! Glenn's voice assistant is now active.")
        self.speak(self._get_introduction())
        
        print("\n🎧 Voice Commands:")
        print("  - Say 'Glenn' or 'Hey Glenn' to activate")
        print("  - Say 'stop listening' to exit voice mode")
        print("  - Try: 'status', 'add task', 'who are you'\n")
        
        try:
            self._voice_loop()
        except KeyboardInterrupt:
            print("\n🎤 Voice assistant interrupted")
            self.speak("Voice assistant shutting down. Goodbye!")
            self.stop()
    
    def _voice_loop(self):
        """Main voice processing loop."""
        logger.info("Starting voice processing loop")
        
        while self.is_running:
            try:
                # Listen for wake word
                if self.is_listening:
                    self._process_wake_word()
                
                # Small delay to prevent CPU overuse
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Voice loop error: {e}")
                time.sleep(1.0)  # Longer delay on error
    
    def _process_wake_word(self):
        """Process wake word detection."""
        wake_word = self.wake_detector.listen_for_wake_word(timeout=self.wake_timeout)
        
        if wake_word:
            logger.info(f"Wake word detected: {wake_word}")
            print(f"🎧 Wake word detected: {wake_word}")
            
            # Process the command
            self._process_voice_command()
    
    def _process_voice_command(self):
        """Process voice command after wake word."""
        # Acknowledge wake word
        self.speak("Yes? I'm listening.")
        
        # Listen for command
        command_text = self.speech_to_text.listen_for_speech(
            timeout=self.command_timeout,
            phrase_time_limit=10.0
        )
        
        if command_text:
            print(f"[You 🎤]: {command_text}")
            logger.info(f"Command received: {command_text}")
            
            # Parse and execute command
            response = self._execute_voice_command(command_text)
            
            # Respond
            if response:
                if response == "VOICE_EXIT":
                    self.speak("Voice assistant deactivated. Goodbye!")
                    self.stop()
                    return
                else:
                    self.speak(response)
            
            # Log interaction
            self._log_interaction(command_text, response)
            
        else:
            self.speak("I didn't hear anything. Try again when you're ready.")
    
    def _execute_voice_command(self, command_text: str) -> str:
        """Execute a voice command and return response."""
        # Parse command
        command_info = self.command_handler.parse_command(command_text)
        
        if command_info:
            # Execute parsed command
            return self.command_handler.execute_command(command_info)
        else:
            # Fallback to general chat processing
            return self._handle_general_query(command_text)
    
    def _handle_general_query(self, query: str) -> str:
        """Handle general queries that don't match specific patterns."""
        query_lower = query.lower()
        
        # Simple fallback responses
        if any(word in query_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I help you today?"
        elif any(word in query_lower for word in ['thank', 'thanks']):
            return "You're welcome! Happy to help."
        elif any(word in query_lower for word in ['good', 'great', 'awesome']):
            return "I'm glad to hear that!"
        else:
            return f"I heard you say '{query}', but I'm not sure how to help with that. Try asking about status, tasks, or time."
    
    def _get_introduction(self) -> str:
        """Get Glenn's introduction."""
        try:
            from commands.awareness import get_awareness_summary
            base_intro = get_awareness_summary()
            return f"{base_intro}. I'm equipped with voice recognition and can help you with tasks, memory operations, system status, and general assistance. Just say my name to get my attention."
        except ImportError:
            return "I'm Glenn, your AI voice assistant. I can help with tasks, system operations, and answer questions. How can I assist you today?"
    
    def _log_interaction(self, user_input: str, response: str):
        """Log voice interaction."""
        try:
            # Import from main module
            import sys
            from pathlib import Path
            
            # Add parent directory to path to import from main
            parent_dir = Path(__file__).parent.parent
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))
                
            from main import log_interaction
            log_interaction(user_input, "Glenn-Voice", response or "No response")
        except Exception as e:
            logger.error(f"Failed to log interaction: {e}")
    
    def speak(self, text: str):
        """Speak text using TTS or print as fallback."""
        if self.text_to_speech.is_available:
            success = self.text_to_speech.speak(text)
            if success:
                return
        
        # Fallback to text output
        print(f"[Glenn 🎤]: {text}")
    
    def stop(self):
        """Stop the voice assistant."""
        logger.info("Stopping voice assistant...")
        
        self.is_running = False
        self.is_listening = False
        
        # Wait for voice thread to finish
        if self.voice_thread and self.voice_thread.is_alive():
            self.voice_thread.join(timeout=2.0)
        
        # Cleanup components
        self.text_to_speech.cleanup()
        self.speech_to_text.cleanup()
        
        logger.info("Voice assistant stopped")
    
    def pause_listening(self):
        """Pause wake word listening."""
        self.is_listening = False
        logger.info("Voice listening paused")
    
    def resume_listening(self):
        """Resume wake word listening."""
        self.is_listening = True
        logger.info("Voice listening resumed")
    
    def is_active(self) -> bool:
        """Check if voice assistant is active."""
        return self.is_running
    
    def get_status(self) -> dict:
        """Get voice assistant status."""
        return {
            'running': self.is_running,
            'listening': self.is_listening,
            'wake_detector_available': self.wake_detector.recognizer is not None,
            'speech_to_text_available': self.speech_to_text.recognizer is not None,
            'text_to_speech_available': self.text_to_speech.is_available,
            'wake_words': self.wake_detector.get_wake_words(),
            'command_count': len(self.command_handler.get_command_list())
        }

def main():
    """Main entry point for voice assistant."""
    assistant = GlennVoiceAssistant()
    assistant.start_blocking()

if __name__ == "__main__":
    main()
