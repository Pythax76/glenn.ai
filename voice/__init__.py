"""
🎤 Glenn.AI Voice Module
Modular voice assistant system for Glenn.AI
"""

__version__ = "1.0.0"
__all__ = ["assistant", "wake_words", "speech_to_text", "text_to_speech", "voice_commands"]

from .assistant import GlennVoiceAssistant
from .wake_words import WakeWordDetector
from .speech_to_text import SpeechToText
from .text_to_speech import TextToSpeech
from .voice_commands import VoiceCommandHandler
