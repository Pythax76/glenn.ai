# command_interface.py
# Drop-in router: argparse, --list/--debug, aliases, safe key=value parsing
# Single catch-all to avoid "unreachable except" warning.

import importlib
import sys
import argparse
from typing import Dict, Any, Tuple

# Central routing table (extend as needed)
COMMAND_ROUTES: Dict[str, str] = {
    "audit.start": "commands.audit",
    "recall.last": "commands.memory",
    "kunda.mode": "commands.kunda",
    "tasky.queue": "commands.tasky",
    "status.report": "commands.status",
}

# Optional short aliases for convenience
ALIASES: Dict[str, str] = {
    "status": "status.report",
    "audit": "audit.start",
    "recall": "recall.last",
    "tasky": "tasky.queue",
    "kunda": "kunda.mode",
}

def resolve_command(name: str) -> str:
    """Resolve aliases and confirm the command exists."""
    route = ALIASES.get(name, name)
    if route not in COMMAND_ROUTES:
        raise KeyError(f"Unknown command '{name}'. Use --list to see options.")
    return route

def parse_kv_pairs(pairs) -> Dict[str, Any]:
    """
    Parse key=value pairs. Values keep '=' if present (split only on first '=').
    Example: foo=bar=baz -> {'foo': 'bar=baz'}
    """
    out: Dict[str, Any] = {}
    for raw in pairs or []:
        if "=" not in raw:
            raise ValueError(f"Invalid param '{raw}'. Expected key=value.")
        k, v = raw.split("=", 1)
        k = k.strip()
        if not k:
            raise ValueError(f"Empty key in '{raw}'.")
        out[k] = v
    return out

def execute_command(command: str, params: Dict[str, Any], debug: bool = False):
    """Import module and run its `run(**kwargs)` entrypoint."""
    module_path = COMMAND_ROUTES[command]
    if debug:
        print(f"[Glenn.AI][debug] route={command} -> module={module_path}; params={params}")
    module = importlib.import_module(module_path)
    if not hasattr(module, "run"):
        raise AttributeError(f"No 'run(**kwargs)' in {module_path}")
    result = module.run(**params)  # modules may print or return data
    if result is not None:
        print(result)

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="command_interface.py",
        description="Glenn.AI Command Router — routes CLI commands to modular skills."
    )
    p.add_argument(
        "command",
        nargs="?",
        help="Command route or alias (e.g., 'status.report' or 'status')."
    )
    p.add_argument(
        "params",
        nargs="*",
        help="Optional key=value arguments passed to the command."
    )
    p.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available commands and aliases."
    )
    p.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug output."
    )
    return p

def print_commands():
    print("Available commands:")
    for route in sorted(COMMAND_ROUTES.keys()):
        print(f"  - {route}")
    if ALIASES:
        print("\nAliases:")
        for short, full in sorted(ALIASES.items()):
            print(f"  - {short} -> {full}")

def main(argv: Tuple[str, ...] | None = None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        print_commands()
        return 0

    if not args.command:
        parser.print_help()
        return 2

    try:
        route = resolve_command(args.command.strip())
        params = parse_kv_pairs(args.params)
        execute_command(route, params, debug=args.debug)
        return 0
    except Exception as e:
        # One catch-all to avoid "unreachable except" warning.
        msg = str(e) or e.__class__.__name__
        if args.debug:
            import traceback; traceback.print_exc()
        print(f"[Glenn.AI] {msg}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
