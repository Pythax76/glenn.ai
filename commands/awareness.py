"""
🧠 Glenn.AI Self-Awareness Module
Advanced self-awareness and state management for Glenn.AI
"""

import logging
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

def execute(args: Optional[Any] = None):
    """
    Execute self-awareness operations.
    
    Args:
        args: Command line arguments or parameters
    """
    logger.info("Executing self-awareness check")
    
    print("🧠 Glenn.AI Self-Awareness Report")
    print("=" * 45)
    
    # Load and display twin identity
    twin_data = load_twin_identity()
    if twin_data:
        display_identity_summary(twin_data)
        display_persona_status(twin_data)
        display_capabilities(twin_data)
        display_current_state()
    else:
        print("❌ Unable to load self-awareness data")

def load_twin_identity():
    """Load complete twin identity from digital_twin.json."""
    project_root = Path(__file__).parent.parent
    twin_path = project_root / "data" / "digital_twin.json"
    
    try:
        with open(twin_path, 'r', encoding='utf-8') as f:
            twin_data = json.load(f)
        logger.info("Twin identity loaded successfully")
        return twin_data
    except FileNotFoundError:
        logger.error("Digital twin profile not found")
        return None
    except Exception as e:
        logger.error(f"Failed to load twin identity: {e}")
        return None

def display_identity_summary(twin_data: Dict):
    """Display core identity information."""
    print("\n👤 Core Identity:")
    
    personal = twin_data.get('personal', {})
    professional = twin_data.get('professional', {})
    
    print(f"  Name: {personal.get('fullName', 'Unknown')}")
    print(f"  Twin ID: {twin_data.get('id', 'Unknown')}")
    print(f"  Professional Role: {professional.get('title', 'Unknown')}")
    print(f"  Company: {professional.get('currentEmployer', 'Unknown')}")
    
    # Show key skills
    skills = twin_data.get('skills', [])
    ai_skills = [skill for skill in skills if any(word in skill.lower() for word in ['ai', 'digital', 'synthetic', 'automation'])]
    if ai_skills:
        print(f"  AI Specializations: {', '.join(ai_skills[:3])}")

def display_persona_status(twin_data: Dict):
    """Display AI persona status."""
    print("\n🎭 AI Persona Matrix:")
    
    personas = twin_data.get('ai_personas', {})
    for persona, description in personas.items():
        status = "🟢 Active" if persona in ['Echo', 'Tasky'] else "🟡 Standby"
        print(f"  {persona}: {description} - {status}")

def display_capabilities(twin_data: Dict):
    """Display current system capabilities."""
    print("\n⚡ System Capabilities:")
    
    # Check command interface status
    cmd_interface = twin_data.get('commandInterface', {})
    if cmd_interface.get('status') == 'active':
        print("  ✅ Command Interface: Online")
        routes = cmd_interface.get('routes', [])
        print(f"  📍 Active Routes: {len(routes)}")
    else:
        print("  ❌ Command Interface: Offline")
    
    # Check data systems
    project_root = Path(__file__).parent.parent
    data_files = {
        "Memory Database": project_root / "data" / "glenn_memory.db",
        "Twin Profile": project_root / "data" / "digital_twin.json",
        "Manifest": project_root / "manifests" / "glenn_manifest.json"
    }
    
    for name, path in data_files.items():
        status = "✅ Online" if path.exists() else "❌ Missing"
        print(f"  {name}: {status}")

def display_current_state():
    """Display current operational state."""
    print("\n🔄 Current State:")
    
    # Check recent activity
    project_root = Path(__file__).parent.parent
    db_path = project_root / "data" / "glenn_memory.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check for recent interactions
        cursor.execute("SELECT COUNT(*) FROM memory_log WHERE date(timestamp) = date('now')")
        today_interactions = cursor.fetchone()[0]
        
        # Check for recent tasks
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE date(created_at) = date('now')")
        today_tasks = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"  💬 Today's Interactions: {today_interactions}")
        print(f"  📋 Today's Tasks Created: {today_tasks}")
        
    except Exception as e:
        logger.error(f"Failed to check current state: {e}")
        print("  ⚠️ Unable to access activity data")
    
    # Show system uptime context
    print(f"  🕐 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  🌟 Status: Fully Operational")

def get_awareness_summary():
    """Get a brief awareness summary for other modules."""
    twin_data = load_twin_identity()
    if not twin_data:
        return "Self-awareness data unavailable"
    
    personal = twin_data.get('personal', {})
    name = personal.get('fullName', 'Unknown')
    role = twin_data.get('professional', {}).get('title', 'Unknown')
    
    return f"I am {name}'s digital twin, operating as {role}"

if __name__ == "__main__":
    # For standalone testing
    execute()
