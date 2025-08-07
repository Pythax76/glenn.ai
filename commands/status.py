"""
🧠 Glenn.AI Status Module
System status monitoring for Glenn.AI
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

def execute(args: Optional[Dict[str, Any]] = None):
    """
    Execute system status check.
    
    Args:
        args: Command line arguments or parameters
    """
    logger.info("Executing system status check")
    
    print("📊 Glenn.AI System Status")
    print("=" * 40)
    
    show_system_info()
    show_component_status()
    show_recent_activity()
    
def show_system_info():
    """Show basic system information."""
    print("\n💻 System Information:")
    print(f"  Python Version: {sys.version.split()[0]}")
    print(f"  Platform: {sys.platform}")
    print(f"  Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
def show_component_status():
    """Show status of Glenn.AI components."""
    print("\n🔧 Component Status:")
    
    project_root = Path(__file__).parent.parent
    
    components = {
        "Command Interface": project_root / "command_interface.py",
        "Core Logger": project_root / "core" / "logger.py",
        "Memory System": project_root / "core" / "memory_sync.py",
        "Persona Router": project_root / "core" / "persona_router.py",
        "Twin Loader": project_root / "core" / "twin_loader.py"
    }
    
    for name, path in components.items():
        status = "🟢 Online" if path.exists() else "🔴 Offline"
        print(f"  {name}: {status}")
        
def show_recent_activity():
    """Show recent system activity."""
    print("\n📈 Recent Activity:")
    
    project_root = Path(__file__).parent.parent
    logs_dir = project_root / "logs"
    
    if logs_dir.exists() and (logs_dir / "glenn.log").exists():
        log_file = logs_dir / "glenn.log"
        modified = datetime.fromtimestamp(log_file.stat().st_mtime)
        print(f"  Last Log Entry: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("  No recent activity logs found")
        
    # Show memory database activity
    data_dir = project_root / "data"
    if data_dir.exists() and (data_dir / "glenn_memory.db").exists():
        db_file = data_dir / "glenn_memory.db"
        modified = datetime.fromtimestamp(db_file.stat().st_mtime)
        print(f"  Memory Last Updated: {modified.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # For standalone testing
    execute()
