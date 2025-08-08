"""
🎤 Glenn.AI Speech to Text
Converts spoken audio to text
"""

import logging
import speech_recognition as sr
from typing import Optional

logger = logging.getLogger(__name__)

class SpeechToText:
    """Converts speech to text using various recognition engines."""
    
    def __init__(self):
        """Initialize speech to text system."""
        self.recognizer = None
        self.microphone = None
        
    def initialize(self) -> bool:
        """Initialize speech recognition components."""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
            logger.info("Speech to text initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize speech to text: {e}")
            return False
    
    def listen_for_speech(self, timeout: float = 5.0, phrase_time_limit: float = 10.0) -> Optional[str]:
        """
        Listen for speech and convert to text.
        
        Args:
            timeout: Maximum time to wait for speech start
            phrase_time_limit: Maximum time for a complete phrase
            
        Returns:
            Recognized text or None if failed
        """
        if not self.recognizer or not self.microphone:
            logger.error("Speech recognition not initialized")
            return None
            
        try:
            logger.info("Listening for speech...")
            
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            logger.info("Processing speech...")
            
            # Try Google Speech Recognition first
            try:
                text = self.recognizer.recognize_google(audio, language='en-US')
                logger.info(f"Recognized (Google): {text}")
                return text
                
            except sr.UnknownValueError:
                logger.warning("Google Speech Recognition could not understand audio")
                
            except sr.RequestError as e:
                logger.warning(f"Google Speech Recognition error: {e}")
                
                # Fallback to offline recognition if available
                try:
                    text = self.recognizer.recognize_sphinx(audio)
                    logger.info(f"Recognized (Sphinx): {text}")
                    return text
                    
                except sr.UnknownValueError:
                    logger.warning("Sphinx could not understand audio")
                except sr.RequestError as e:
                    logger.warning(f"Sphinx error: {e}")
            
            return None
            
        except sr.WaitTimeoutError:
            logger.info("No speech detected within timeout period")
            return None
            
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    def recognize_from_audio_data(self, audio_data) -> Optional[str]:
        """
        Recognize speech from audio data.
        
        Args:
            audio_data: Audio data to process
            
        Returns:
            Recognized text or None
        """
        if not self.recognizer:
            return None
            
        try:
            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(audio_data, language='en-US')
            return text
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
            
        except sr.RequestError as e:
            logger.error(f"Recognition service error: {e}")
            return None
    
    def test_microphone(self) -> bool:
        """Test if microphone is working."""
        if not self.microphone:
            return False
            
        try:
            with self.microphone as source:
                logger.info("Testing microphone... Say something!")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=3)
                
            # Try to recognize the test audio
            try:
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Microphone test successful: {text}")
                return True
                
            except sr.UnknownValueError:
                logger.info("Microphone working but speech not recognized")
                return True  # Mic is working, just didn't understand
                
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return False
    
    def get_available_microphones(self) -> list:
        """Get list of available microphones."""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            logger.info(f"Available microphones: {mic_list}")
            return mic_list
            
        except Exception as e:
            logger.error(f"Failed to get microphone list: {e}")
            return []
    
    def set_microphone(self, device_index: Optional[int] = None):
        """Set specific microphone device."""
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            logger.info(f"Set microphone to device index: {device_index}")
            
        except Exception as e:
            logger.error(f"Failed to set microphone: {e}")
            
    def cleanup(self):
        """Clean up resources."""
        self.recognizer = None
        self.microphone = None
        logger.info("Speech to text cleaned up")
