import json
import sqlite3
from core.twin_loader import load_twin
from core.persona_router import route_command

DB_PATH = 'glenn_memory.db'

def log_interaction(user_input, persona, response):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO memory_log (user_input, persona, response)
            VALUES (?, ?, ?)
        """, (user_input, persona, response))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[MemoryLog ERROR] {e}")

def main():
    manifest_path = 'manifests/glenn_manifest.json'
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        print("Glenn.Ai is online. Type 'exit' to quit.\n")
        twin = load_twin(manifest)
        while True:
            command = input("[You]: ").strip()
            if command.lower() in ('exit', 'quit'):
                print("[Glenn]: Shutting down. Be safe out there.")
                break
            response = route_command(command, twin)
            print(f"[Glenn]: {response}")
            log_interaction(command, twin['default'], response)
    except FileNotFoundError:
        print("[ERROR] Manifest file not found.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    main()
