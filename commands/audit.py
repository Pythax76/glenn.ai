"""
🧠 Glenn.AI Audit Module
System audit and diagnostics for Glenn.AI
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def execute(args: Optional[Dict[str, Any]] = None):
    """
    Execute system audit and diagnostics.
    
    Args:
        args: Command line arguments or parameters
    """
    logger.info("Starting system audit")
    
    print("🔍 Glenn.AI System Audit")
    print("=" * 40)
    
    audit_python_environment()
    audit_project_structure()
    audit_data_files()
    audit_logs()
    
    print("\n✅ Audit complete")

def audit_python_environment():
    """Audit Python environment."""
    print("\n🐍 Python Environment:")
    print(f"  Version: {sys.version}")
    print(f"  Executable: {sys.executable}")
    print(f"  Platform: {sys.platform}")

def audit_project_structure():
    """Audit project structure."""
    print("\n📁 Project Structure:")
    project_root = Path(__file__).parent.parent
    
    expected_dirs = ["commands", "data", "logs", "core"]
    expected_files = ["command_interface.py", "README.md"]
    
    for directory in expected_dirs:
        dir_path = project_root / directory
        status = "✅" if dir_path.exists() else "❌"
        print(f"  {status} {directory}/")
    
    for file in expected_files:
        file_path = project_root / file
        status = "✅" if file_path.exists() else "❌"
        print(f"  {status} {file}")

def audit_data_files():
    """Audit data files."""
    print("\n📦 Data Files:")
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    
    if data_dir.exists():
        for file in data_dir.iterdir():
            if file.is_file():
                size = file.stat().st_size
                print(f"  ✅ {file.name} ({size} bytes)")
    else:
        print("  ❌ Data directory not found")

def audit_logs():
    """Audit log files."""
    print("\n🪵 Log Files:")
    project_root = Path(__file__).parent.parent
    logs_dir = project_root / "logs"
    
    if logs_dir.exists():
        for file in logs_dir.iterdir():
            if file.is_file():
                size = file.stat().st_size
                print(f"  ✅ {file.name} ({size} bytes)")
    else:
        print("  ❌ Logs directory not found")

if __name__ == "__main__":
    # For standalone testing
    execute()
