"""
🎤 Glenn.AI Voice Commands
Pre-built spoken command handling and routing
"""

import logging
from typing import Dict, Optional, Any, Callable
import re

logger = logging.getLogger(__name__)

class VoiceCommandHandler:
    """Handles voice command parsing and routing."""
    
    def __init__(self):
        """Initialize voice command handler."""
        self.command_patterns = {}
        self.command_handlers = {}
        self._setup_default_patterns()
    
    def _setup_default_patterns(self):
        """Setup default voice command patterns."""
        # System commands
        self.register_pattern("status", [
            r"(?:what's your|how's your|system) status",
            r"how are you",
            r"are you (?:okay|working|online)",
            r"system check"
        ])
        
        self.register_pattern("identity", [
            r"who are you",
            r"introduce yourself",
            r"what's your name",
            r"tell me about yourself"
        ])
        
        # Task management
        self.register_pattern("add_task", [
            r"add (?:a )?task (.+)",
            r"create (?:a )?task (.+)",
            r"remind me to (.+)",
            r"I need to (.+)"
        ])
        
        self.register_pattern("list_tasks", [
            r"(?:show|list) (?:my )?tasks",
            r"what (?:tasks|do I) have",
            r"task list"
        ])
        
        # Memory operations
        self.register_pattern("memory_backup", [
            r"backup (?:my )?memory",
            r"create (?:a )?(?:memory )?backup",
            r"save my data"
        ])
        
        self.register_pattern("memory_status", [
            r"memory status",
            r"check (?:my )?memory",
            r"how's (?:my )?memory"
        ])
        
        # Time and date
        self.register_pattern("time", [
            r"what time is it",
            r"what's the time",
            r"current time"
        ])
        
        self.register_pattern("date", [
            r"what(?:'s the)? date",
            r"today's date",
            r"current date"
        ])
        
        # Exit commands
        self.register_pattern("exit", [
            r"(?:stop|exit|quit) listening",
            r"(?:disable|turn off) voice",
            r"goodbye",
            r"see you later"
        ])
        
        # Help
        self.register_pattern("help", [
            r"help",
            r"what can you do",
            r"list commands",
            r"voice commands"
        ])
    
    def register_pattern(self, command_name: str, patterns: list):
        """
        Register voice command patterns.
        
        Args:
            command_name: Name of the command
            patterns: List of regex patterns to match
        """
        compiled_patterns = []
        for pattern in patterns:
            try:
                compiled_patterns.append(re.compile(pattern, re.IGNORECASE))
            except re.error as e:
                logger.error(f"Invalid regex pattern '{pattern}': {e}")
        
        self.command_patterns[command_name] = compiled_patterns
        logger.info(f"Registered {len(compiled_patterns)} patterns for command '{command_name}'")
    
    def register_handler(self, command_name: str, handler: Callable):
        """
        Register a handler function for a command.
        
        Args:
            command_name: Name of the command
            handler: Function to handle the command
        """
        self.command_handlers[command_name] = handler
        logger.info(f"Registered handler for command '{command_name}'")
    
    def parse_command(self, spoken_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse spoken text to identify commands.
        
        Args:
            spoken_text: The recognized speech text
            
        Returns:
            Command information dict or None
        """
        if not spoken_text:
            return None
        
        spoken_text = spoken_text.strip().lower()
        logger.info(f"Parsing command: '{spoken_text}'")
        
        # Check each command pattern
        for command_name, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = pattern.search(spoken_text)
                if match:
                    # Extract any captured groups as parameters
                    params = list(match.groups()) if match.groups() else []
                    
                    command_info = {
                        'command': command_name,
                        'original_text': spoken_text,
                        'matched_pattern': pattern.pattern,
                        'parameters': params,
                        'confidence': 1.0  # Could be enhanced with fuzzy matching
                    }
                    
                    logger.info(f"Command matched: {command_name}")
                    return command_info
        
        # No pattern matched
        logger.info("No command pattern matched")
        return None
    
    def execute_command(self, command_info: Dict[str, Any]) -> str:
        """
        Execute a parsed command.
        
        Args:
            command_info: Command information from parse_command
            
        Returns:
            Response text
        """
        if not command_info:
            return "I didn't understand that command."
        
        command_name = command_info.get('command')
        parameters = command_info.get('parameters', [])
        
        # Check if we have a registered handler
        if command_name in self.command_handlers:
            try:
                return self.command_handlers[command_name](command_info)
            except Exception as e:
                logger.error(f"Handler error for {command_name}: {e}")
                return f"Sorry, I had trouble executing that command."
        
        # Default responses for built-in commands
        return self._handle_builtin_command(command_name, parameters)
    
    def _handle_builtin_command(self, command_name: str, parameters: list) -> str:
        """Handle built-in commands with default responses."""
        
        if command_name == "status":
            return "All systems operational. Voice recognition active and ready for commands."
        
        elif command_name == "identity":
            return "I am Glenn, your AI voice assistant. I can help with tasks, system operations, and answer questions."
        
        elif command_name == "add_task":
            if parameters:
                task_description = parameters[0]
                # This would integrate with the actual task system
                return f"I'll add the task: {task_description}. Task management integration needed."
            else:
                return "What task would you like me to add?"
        
        elif command_name == "list_tasks":
            return "Task listing functionality needs integration with the task management system."
        
        elif command_name == "memory_backup":
            return "I'll create a memory backup for you. This feature needs integration with the memory system."
        
        elif command_name == "memory_status":
            return "Memory systems are operational. Detailed status needs integration."
        
        elif command_name == "time":
            from datetime import datetime
            return f"It's {datetime.now().strftime('%I:%M %p')}"
        
        elif command_name == "date":
            from datetime import datetime
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"
        
        elif command_name == "exit":
            return "VOICE_EXIT"  # Special response to trigger exit
        
        elif command_name == "help":
            return self._get_help_text()
        
        else:
            return f"I recognized the command '{command_name}' but don't know how to handle it yet."
    
    def _get_help_text(self) -> str:
        """Get help text listing available commands."""
        commands = list(self.command_patterns.keys())
        help_text = "I can help you with these voice commands: " + ", ".join(commands)
        help_text += ". Try saying 'status', 'add task', or 'what time is it'."
        return help_text
    
    def get_command_list(self) -> list:
        """Get list of available commands."""
        return list(self.command_patterns.keys())
    
    def add_custom_command(self, name: str, patterns: list, handler: Optional[Callable] = None):
        """
        Add a custom voice command.
        
        Args:
            name: Command name
            patterns: List of regex patterns
            handler: Optional handler function
        """
        self.register_pattern(name, patterns)
        if handler:
            self.register_handler(name, handler)
        
        logger.info(f"Added custom command: {name}")
    
    def test_pattern(self, pattern: str, test_text: str) -> bool:
        """
        Test if a pattern matches text.
        
        Args:
            pattern: Regex pattern to test
            test_text: Text to test against
            
        Returns:
            True if pattern matches
        """
        try:
            compiled_pattern = re.compile(pattern, re.IGNORECASE)
            return bool(compiled_pattern.search(test_text))
        except re.error:
            return False
    
    def get_pattern_examples(self) -> Dict[str, list]:
        """Get example patterns for each command."""
        examples = {}
        for command_name, patterns in self.command_patterns.items():
            examples[command_name] = [pattern.pattern for pattern in patterns]
        return examples
