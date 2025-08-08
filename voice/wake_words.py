"""
🎧 Glenn.AI Wake Word Detection
Handles wake word detection for voice activation
"""

import logging
import speech_recognition as sr
from typing import Optional, List

logger = logging.getLogger(__name__)

class WakeWordDetector:
    """Detects wake words to activate voice assistant."""
    
    def __init__(self, wake_words: Optional[List[str]] = None):
        """
        Initialize wake word detector.
        
        Args:
            wake_words: List of wake words to detect
        """
        self.wake_words = wake_words or ["glenn", "hey glenn", "ok glenn"]
        self.recognizer = None
        self.microphone = None
        self.is_listening = False
        
    def initialize(self) -> bool:
        """Initialize speech recognition components."""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
            logger.info("Wake word detector initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize wake word detector: {e}")
            return False
    
    def listen_for_wake_word(self, timeout: float = 1.0) -> Optional[str]:
        """
        Listen for wake words.
        
        Args:
            timeout: Timeout in seconds for listening
            
        Returns:
            Detected wake word or None
        """
        if not self.recognizer or not self.microphone:
            return None
            
        try:
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
            
            # Try to recognize speech
            try:
                text = self.recognizer.recognize_google(audio, language='en-US').lower()
                
                # Check if any wake word is detected
                for wake_word in self.wake_words:
                    if wake_word in text:
                        logger.info(f"Wake word detected: {wake_word}")
                        return wake_word
                        
                return None
                
            except sr.UnknownValueError:
                # Speech was unintelligible
                return None
                
        except sr.WaitTimeoutError:
            # No speech detected within timeout
            return None
        except Exception as e:
            logger.error(f"Wake word detection error: {e}")
            return None
    
    def is_wake_word(self, text: str) -> bool:
        """
        Check if text contains a wake word.
        
        Args:
            text: Text to check
            
        Returns:
            True if wake word found
        """
        text_lower = text.lower()
        return any(wake_word in text_lower for wake_word in self.wake_words)
    
    def get_wake_words(self) -> List[str]:
        """Get list of configured wake words."""
        return self.wake_words.copy()
    
    def add_wake_word(self, wake_word: str):
        """Add a new wake word."""
        if wake_word.lower() not in self.wake_words:
            self.wake_words.append(wake_word.lower())
            logger.info(f"Added wake word: {wake_word}")
    
    def remove_wake_word(self, wake_word: str):
        """Remove a wake word."""
        wake_word_lower = wake_word.lower()
        if wake_word_lower in self.wake_words:
            self.wake_words.remove(wake_word_lower)
            logger.info(f"Removed wake word: {wake_word}")
    
    def start_listening(self):
        """Start continuous listening mode."""
        self.is_listening = True
        logger.info("Started continuous wake word listening")
    
    def stop_listening(self):
        """Stop continuous listening mode."""
        self.is_listening = False
        logger.info("Stopped wake word listening")
