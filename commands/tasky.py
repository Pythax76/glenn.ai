"""
🧠 Glenn.AI Task Management Module
Task management operations for Glenn.AI
"""

import logging
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

def execute(args: Optional[Any] = None):
    """
    Execute task management operations.
    
    Args:
        args: Command line arguments or parameters
    """
    logger.info("Executing task management operation")
    
    action = None
    if args and hasattr(args, 'task_action') and args.task_action:
        action = args.task_action
        
    if action:
        if action.startswith('add:'):
            task_desc = action[4:].strip()
            add_task(task_desc)
        elif action.startswith('complete:'):
            task_id = action[9:].strip()
            complete_task(task_id)
        elif action.startswith('remove:'):
            task_id = action[7:].strip()
            remove_task(task_id)
        else:
            logger.info(f"Task action: {action}")
            list_tasks()
    else:
        list_tasks()

def get_db_path():
    """Get the database path."""
    project_root = Path(__file__).parent.parent
    return project_root / "data" / "glenn_memory.db"

def init_tasks_table():
    """Initialize the tasks table if it doesn't exist."""
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to initialize tasks table: {e}")

def list_tasks():
    """List all current tasks."""
    init_tasks_table()
    db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, description, status, created_at FROM tasks WHERE status != 'completed' ORDER BY created_at")
        tasks = cursor.fetchall()
        conn.close()
        
        print("📋 Current Tasks:")
        if not tasks:
            print("  - No active tasks found")
        else:
            for task_id, desc, status, created in tasks:
                status_icon = "⏳" if status == "pending" else "🔄"
                print(f"  {status_icon} [{task_id}] {desc} (created: {created[:10]})")
                
    except Exception as e:
        logger.error(f"Failed to list tasks: {e}")
        print("❌ Failed to retrieve tasks")
    
def add_task(task_description: str):
    """Add a new task."""
    init_tasks_table()
    db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (description) VALUES (?)", (task_description,))
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Adding task: {task_description}")
        print(f"✅ Added task [{task_id}]: {task_description}")
        
    except Exception as e:
        logger.error(f"Failed to add task: {e}")
        print(f"❌ Failed to add task: {task_description}")
    
def complete_task(task_id: str):
    """Mark a task as complete."""
    init_tasks_table()
    db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?", 
            (task_id,)
        )
        if cursor.rowcount > 0:
            conn.commit()
            logger.info(f"Completing task: {task_id}")
            print(f"✅ Task {task_id} completed")
        else:
            print(f"❌ Task {task_id} not found")
        conn.close()
        
    except Exception as e:
        logger.error(f"Failed to complete task: {e}")
        print(f"❌ Failed to complete task {task_id}")
    
def remove_task(task_id: str):
    """Remove a task."""
    init_tasks_table()
    db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount > 0:
            conn.commit()
            logger.info(f"Removing task: {task_id}")
            print(f"🗑️ Task {task_id} removed")
        else:
            print(f"❌ Task {task_id} not found")
        conn.close()
        
    except Exception as e:
        logger.error(f"Failed to remove task: {e}")
        print(f"❌ Failed to remove task {task_id}")

if __name__ == "__main__":
    # For standalone testing
    execute()
