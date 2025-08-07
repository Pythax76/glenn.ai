"""
🧠 Glenn.AI Chat Module
Interactive conversational interface for Glenn.AI
"""

import logging
import json
import sqlite3
from pathlib import Path
from typing import Optional, Any

logger = logging.getLogger(__name__)

def execute(args: Optional[Any] = None):
    """
    Execute interactive chat session.
    
    Args:
        args: Command line arguments or parameters
    """
    logger.info("Starting Glenn.AI chat session")
    
    print("🤖 Glenn.AI Interactive Mode")
    print("=" * 40)
    print("Type 'exit' or 'quit' to end session\n")
    
    # Load twin configuration
    twin = load_twin_config()
    if not twin:
        print("❌ Failed to load twin configuration")
        return
        
    # Initialize memory logging
    init_memory_table()
    
    # Chat loop
    while True:
        try:
            command = input("[You]: ").strip()
            if command.lower() in ('exit', 'quit', 'bye'):
                print("[Glenn]: Shutting down. Be safe out there.")
                break
                
            if not command:
                continue
                
            response = route_command(command, twin)
            print(f"[Glenn]: {response}")
            log_interaction(command, twin['default'], response)
            
        except KeyboardInterrupt:
            print("\n[Glenn]: Chat session interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Chat error: {e}")
            print(f"[Glenn]: Sorry, I encountered an error: {e}")

def load_twin_config():
    """Load twin configuration from manifest."""
    project_root = Path(__file__).parent.parent
    manifest_path = project_root / "manifests" / "glenn_manifest.json"
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
            
        twin = {
            'id': manifest.get('twinID'),
            'personas': manifest.get('personas'),
            'default': manifest.get('defaultPersona')
        }
        logger.info(f"Loaded twin: {twin['id']}")
        return twin
        
    except FileNotFoundError:
        logger.error("Manifest file not found")
        return None
    except Exception as e:
        logger.error(f"Failed to load twin config: {e}")
        return None

def route_command(command: str, twin: dict) -> str:
    """Route command to appropriate handler."""
    command_lower = command.lower()
    
    # Command routing logic
    if any(word in command_lower for word in ['task', 'todo', 'remind']):
        return handle_task_command(command)
    elif any(word in command_lower for word in ['memory', 'remember', 'recall']):
        return handle_memory_command(command)
    elif any(word in command_lower for word in ['status', 'health', 'how are you']):
        return handle_status_command()
    elif any(word in command_lower for word in ['hello', 'hi', 'hey']):
        return f"Hello! I'm {twin['default']}, your digital twin. How can I assist you today?"
    elif 'echo' in command_lower or 'glenn' in command_lower:
        return f"Echo here. You said: '{command}'"
    else:
        return f"I heard you, but I don't yet know how to handle: '{command}'. Try asking about tasks, memory, or status."

def handle_task_command(command: str) -> str:
    """Handle task-related commands."""
    if 'add' in command.lower() or 'create' in command.lower():
        return "To add a task, use: python command_interface.py tasky add:'your task description'"
    elif 'list' in command.lower() or 'show' in command.lower():
        return "To list tasks, use: python command_interface.py tasky"
    else:
        return "I can help with tasks! Try 'add task' or 'list tasks'."

def handle_memory_command(command: str) -> str:
    """Handle memory-related commands."""
    if 'backup' in command.lower():
        return "To backup memory, use: python command_interface.py memory backup"
    elif 'sync' in command.lower():
        return "To sync memory, use: python command_interface.py memory sync"
    else:
        return "I can help with memory operations! Try 'backup memory' or 'sync memory'."

def handle_status_command() -> str:
    """Handle status commands."""
    return "I'm online and ready! For detailed status, use: python command_interface.py status"

def init_memory_table():
    """Initialize memory logging table."""
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_input TEXT NOT NULL,
                persona TEXT NOT NULL,
                response TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to initialize memory table: {e}")

def log_interaction(user_input: str, persona: str, response: str):
    """Log interaction to memory database."""
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO memory_log (user_input, persona, response)
            VALUES (?, ?, ?)
        """, (user_input, persona, response))
        conn.commit()
        conn.close()
        logger.debug("Interaction logged to memory")
    except Exception as e:
        logger.error(f"Memory log error: {e}")

def get_db_path():
    """Get the database path."""
    project_root = Path(__file__).parent.parent
    return project_root / "data" / "glenn_memory.db"

if __name__ == "__main__":
    # For standalone testing
    execute()
