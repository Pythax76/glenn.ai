import json
import sqlite3
import sys
from core.twin_loader import load_twin
from core.persona_router import route_command

DB_PATH = 'glenn_memory.db'

def log_interaction(user_input, persona, response):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_input TEXT,
                persona TEXT,
                response TEXT
            )
        """)
        
        cursor.execute("""
            INSERT INTO memory_log (user_input, persona, response)
            VALUES (?, ?, ?)
        """, (user_input, persona, response))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[MemoryLog ERROR] {e}")

def main():
    # Check for voice activation command line argument
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['voice', '--voice', '-v']:
        print("🎧 Activating voice mode...")
        try:
            from voice_activation import activate_voice_shell
            activate_voice_shell()
            return
        except ImportError:
            print("❌ Voice system not available. Starting text mode...")
    
    # Regular text-based interface
    manifest_path = 'manifests/glenn_manifest.json'
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        print("Glenn.Ai is online. Type 'exit' to quit or 'voice' for voice mode.\n")
        twin = load_twin(manifest)
        
        while True:
            command = input("[You]: ").strip()
            
            if command.lower() in ('exit', 'quit'):
                print("[Glenn]: Shutting down. Be safe out there.")
                break
            
            # Check for voice activation during text mode
            if command.lower() == 'voice':
                print("🎧 Switching to voice mode...")
                try:
                    from voice_activation import activate_voice_shell
                    activate_voice_shell()
                    break  # Exit text mode
                except ImportError:
                    print("❌ Voice system not available. Continuing in text mode...")
                    continue
            
            response = route_command(command, twin)
            print(f"[Glenn]: {response}")
            log_interaction(command, twin['default'], response)
            
    except FileNotFoundError:
        print("[ERROR] Manifest file not found.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    main()
