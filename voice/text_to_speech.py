"""
🔊 Glenn.AI Text to Speech
Converts text to spoken audio
"""

import logging
import pyttsx3
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

class TextToSpeech:
    """Converts text to speech using various TTS engines."""
    
    def __init__(self):
        """Initialize text to speech system."""
        self.engine = None
        self.is_available = False
        self.voice_properties = {}
        
    def initialize(self) -> bool:
        """Initialize TTS engine."""
        try:
            self.engine = pyttsx3.init()
            
            # Configure voice properties
            self._configure_voice()
            
            self.is_available = True
            logger.info("Text to speech initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
            self.is_available = False
            return False
    
    def _configure_voice(self):
        """Configure voice properties for Glenn's personality."""
        if not self.engine:
            return
            
        try:
            # Get available voices
            voices = self.engine.getProperty('voices')
            
            # Try to find a suitable male voice
            selected_voice = None
            if voices:
                for voice in voices:
                    voice_name = getattr(voice, 'name', '').lower()
                    # Look for male voices or specific good voices
                    if any(term in voice_name for term in ['male', 'david', 'mark', 'daniel']):
                        selected_voice = voice.id
                        logger.info(f"Selected voice: {voice.name}")
                        break
                
                # Set the voice if found
                if selected_voice:
                    self.engine.setProperty('voice', selected_voice)
            
            # Configure speech rate (words per minute)
            self.engine.setProperty('rate', 175)  # Slightly slower for clarity
            
            # Configure volume (0.0 to 1.0)
            self.engine.setProperty('volume', 0.8)
            
            # Store current properties
            self.voice_properties = {
                'rate': self.engine.getProperty('rate'),
                'volume': self.engine.getProperty('volume'),
                'voice': self.engine.getProperty('voice')
            }
            
            logger.info(f"Voice configured: {self.voice_properties}")
            
        except Exception as e:
            logger.warning(f"Voice configuration failed: {e}")
    
    def speak(self, text: str, blocking: bool = True) -> bool:
        """
        Convert text to speech.
        
        Args:
            text: Text to speak
            blocking: Whether to wait for speech to complete
            
        Returns:
            True if successful
        """
        if not self.is_available or not self.engine:
            logger.warning("TTS not available, falling back to text output")
            print(f"[Glenn 🔊]: {text}")
            return False
            
        try:
            logger.info(f"Speaking: {text[:50]}{'...' if len(text) > 50 else ''}")
            
            self.engine.say(text)
            
            if blocking:
                self.engine.runAndWait()
            
            return True
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            # Fallback to text output
            print(f"[Glenn]: {text}")
            return False
    
    def speak_async(self, text: str) -> bool:
        """Speak text asynchronously (non-blocking)."""
        return self.speak(text, blocking=False)
    
    def set_rate(self, rate: int):
        """
        Set speech rate.
        
        Args:
            rate: Words per minute (typically 100-300)
        """
        if self.engine:
            try:
                self.engine.setProperty('rate', rate)
                self.voice_properties['rate'] = rate
                logger.info(f"Speech rate set to {rate} WPM")
                
            except Exception as e:
                logger.error(f"Failed to set speech rate: {e}")
    
    def set_volume(self, volume: float):
        """
        Set speech volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if self.engine:
            try:
                volume = max(0.0, min(1.0, volume))  # Clamp to valid range
                self.engine.setProperty('volume', volume)
                self.voice_properties['volume'] = volume
                logger.info(f"Speech volume set to {volume}")
                
            except Exception as e:
                logger.error(f"Failed to set speech volume: {e}")
    
    def get_available_voices(self) -> List[Dict]:
        """Get list of available voices."""
        if not self.engine:
            return []
            
        try:
            voices = self.engine.getProperty('voices')
            voice_list = []
            
            for voice in voices or []:
                voice_info = {
                    'id': getattr(voice, 'id', 'unknown'),
                    'name': getattr(voice, 'name', 'Unknown'),
                    'language': getattr(voice, 'languages', ['unknown'])[0] if getattr(voice, 'languages', None) else 'unknown',
                    'gender': 'unknown'
                }
                
                # Try to determine gender from name
                name_lower = voice_info['name'].lower()
                if any(term in name_lower for term in ['male', 'david', 'mark', 'daniel', 'george']):
                    voice_info['gender'] = 'male'
                elif any(term in name_lower for term in ['female', 'susan', 'zira', 'hazel', 'samantha']):
                    voice_info['gender'] = 'female'
                
                voice_list.append(voice_info)
            
            return voice_list
            
        except Exception as e:
            logger.error(f"Failed to get available voices: {e}")
            return []
    
    def set_voice_by_name(self, voice_name: str) -> bool:
        """
        Set voice by name.
        
        Args:
            voice_name: Name of the voice to use
            
        Returns:
            True if voice was set successfully
        """
        if not self.engine:
            return False
            
        try:
            voices = self.engine.getProperty('voices')
            for voice in voices or []:
                if voice_name.lower() in getattr(voice, 'name', '').lower():
                    self.engine.setProperty('voice', voice.id)
                    self.voice_properties['voice'] = voice.id
                    logger.info(f"Voice set to: {voice.name}")
                    return True
            
            logger.warning(f"Voice '{voice_name}' not found")
            return False
            
        except Exception as e:
            logger.error(f"Failed to set voice: {e}")
            return False
    
    def test_speech(self) -> bool:
        """Test TTS functionality."""
        test_message = "Glenn's text to speech system is operational."
        return self.speak(test_message)
    
    def stop(self):
        """Stop current speech."""
        if self.engine:
            try:
                self.engine.stop()
                logger.info("Speech stopped")
                
            except Exception as e:
                logger.error(f"Failed to stop speech: {e}")
    
    def cleanup(self):
        """Clean up TTS resources."""
        if self.engine:
            try:
                self.engine.stop()
                self.engine = None
                self.is_available = False
                logger.info("TTS cleaned up")
                
            except Exception as e:
                logger.error(f"TTS cleanup error: {e}")
    
    def get_status(self) -> Dict:
        """Get TTS system status."""
        return {
            'available': self.is_available,
            'engine': 'pyttsx3' if self.engine else None,
            'properties': self.voice_properties.copy(),
            'voices_count': len(self.get_available_voices())
        }
