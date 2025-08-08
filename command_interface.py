#!/usr/bin/env python3
"""
🔥 Glenn.AI Command Interface
Entry point for CLI command routing

This module serves as the main entry point for Glenn.AI, routing commands
to the appropriate skill modules and handling the overall execution flow.
"""

import sys
import argparse
import logging
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for Glenn.AI command interface."""
    parser = argparse.ArgumentParser(
        description="Glenn.AI - Your Digital Twin Assistant",
        prog="glenn"
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Audit command
    audit_parser = subparsers.add_parser('audit', help='System audit and diagnostics')
    
    # Memory command
    memory_parser = subparsers.add_parser('memory', help='Memory management operations')
    memory_parser.add_argument('action', choices=['sync', 'backup', 'restore'], help='Memory action')
    
    # Kunda command
    kunda_parser = subparsers.add_parser('kunda', help='Kunda AI operations')
    
    # Tasky command
    tasky_parser = subparsers.add_parser('tasky', help='Task management')
    tasky_parser.add_argument('task_action', nargs='?', help='Task action')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='System status')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Interactive chat mode')
    
    # Awareness command  
    awareness_parser = subparsers.add_parser('awareness', help='Self-awareness and identity check')
    
    # Voice command
    voice_parser = subparsers.add_parser('voice', help='Voice assistant shell')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        logger.info(f"Executing command: {args.command}")
        
        # Dynamic import and execution
        if args.command == 'audit':
            from commands import audit
            audit.execute(args)
        elif args.command == 'memory':
            from commands import memory
            memory.execute(args)
        elif args.command == 'kunda':
            from commands import kunda
            kunda.execute(args)
        elif args.command == 'tasky':
            from commands import tasky
            tasky.execute(args)
        elif args.command == 'status':
            from commands import status
            status.execute(args)
        elif args.command == 'chat':
            from commands import chat
            chat.execute(args)
        elif args.command == 'awareness':
            from commands import awareness
            awareness.execute(args)
        elif args.command == 'voice':
            from commands import voice
            voice.execute(args)
        else:
            print(f"Unknown command: {args.command}")
            
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
