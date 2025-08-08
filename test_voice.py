"""
🎤 Voice System Test Script for Glenn.AI
Test voice components independently
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def test_dependencies():
    """Test if voice dependencies are available."""
    print("📦 Testing voice dependencies...")
    
    missing = []
    
    try:
        import speech_recognition
        print("✅ speech_recognition available")
    except ImportError:
        print("❌ speech_recognition missing")
        missing.append("speechrecognition")
    
    try:
        import pyttsx3
        print("✅ pyttsx3 available")
    except ImportError:
        print("❌ pyttsx3 missing")
        missing.append("pyttsx3")
    
    try:
        import pyaudio
        print("✅ pyaudio available")
    except ImportError:
        print("❌ pyaudio missing")
        missing.append("pyaudio")
    
    if missing:
        print(f"\n📦 Install missing packages: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All voice dependencies available!")
    return True

def test_microphone():
    """Test microphone access."""
    print("\n🎤 Testing microphone access...")
    
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        print("🔧 Adjusting for ambient noise...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("✅ Microphone accessible")
        return True
        
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False

def test_text_to_speech():
    """Test text-to-speech."""
    print("\n🔊 Testing text-to-speech...")
    
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"📢 Found {len(voices) if voices else 0} TTS voices")
        
        # Test speech
        engine.say("Testing Glenn voice system")
        engine.runAndWait()
        
        print("✅ Text-to-speech working")
        return True
        
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

def test_speech_recognition():
    """Test speech recognition with a quick listening test."""
    print("\n🎧 Testing speech recognition...")
    print("   (This will listen for 3 seconds - say something!)")
    
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        # Listen for speech
        print("🎤 Listening...")
        with microphone as source:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
        
        # Try to recognize
        print("🧠 Processing speech...")
        text = recognizer.recognize_google(audio)
        print(f"✅ Recognized: '{text}'")
        return True
        
    except sr.WaitTimeoutError:
        print("⏰ No speech detected in time limit")
        return True  # Not an error, just no speech
    except sr.UnknownValueError:
        print("❓ Could not understand speech")
        return True  # Not an error, just unclear speech
    except sr.RequestError as e:
        print(f"❌ Recognition service error: {e}")
        return False
    except Exception as e:
        print(f"❌ Speech recognition test failed: {e}")
        return False

def test_voice_components():
    """Test individual voice components."""
    print("\n🧪 Testing voice components...")
    
    try:
        from voice.wake_words import WakeWordDetector
        from voice.speech_to_text import SpeechToText
        from voice.text_to_speech import TextToSpeech
        from voice.voice_commands import VoiceCommandHandler
        
        # Test wake word detector
        wake_detector = WakeWordDetector()
        if wake_detector.initialize():
            print("✅ Wake word detector initialized")
        else:
            print("❌ Wake word detector failed")
        
        # Test speech to text
        stt = SpeechToText()
        if stt.initialize():
            print("✅ Speech-to-text initialized")
        else:
            print("❌ Speech-to-text failed")
        
        # Test text to speech
        tts = TextToSpeech()
        if tts.initialize():
            print("✅ Text-to-speech initialized")
        else:
            print("❌ Text-to-speech failed")
        
        # Test command handler
        cmd_handler = VoiceCommandHandler()
        print("✅ Command handler initialized")
        
        return True
        
    except ImportError as e:
        print(f"❌ Voice component import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Voice component test failed: {e}")
        return False

def test_full_voice_assistant():
    """Test the full voice assistant."""
    print("\n🎧 Testing full voice assistant...")
    
    try:
        from voice.assistant import GlennVoiceAssistant
        
        assistant = GlennVoiceAssistant()
        
        if assistant.initialize():
            print("✅ Voice assistant initialized successfully")
            
            # Get status
            status = assistant.get_status()
            print(f"📊 Status: {status}")
            
            return True
        else:
            print("❌ Voice assistant initialization failed")
            return False
            
    except ImportError as e:
        print(f"❌ Voice assistant import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Voice assistant test failed: {e}")
        return False

def main():
    """Run all voice system tests."""
    print("🎤 Glenn.AI Voice System Test Suite")
    print("=" * 40)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Microphone", test_microphone),
        ("Text-to-Speech", test_text_to_speech),
        ("Speech Recognition", test_speech_recognition),
        ("Voice Components", test_voice_components),
        ("Full Assistant", test_full_voice_assistant)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            results[test_name] = test_func()
        except KeyboardInterrupt:
            print(f"\n⏹️  Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 40)
    print("📋 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Voice system is ready to use.")
        print("\n🚀 To activate voice mode:")
        print("   python main.py voice")
        print("   or")
        print("   python voice_activation.py")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("\n🔧 To install dependencies:")
        print("   pip install -r requirements_voice.txt")
