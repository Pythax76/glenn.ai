
GLENN.AI

## 🧠 Overview

**Glenn.AI** is a modular digital twin built to extend the capabilities of Jason Lawrence (J-Law), a cybersecurity and systems automation professional. It blends identity, memory, task routing, and synthetic AI personas to create a persistent, evolving co-pilot across both professional and personal contexts.

This repository serves as the home for Glenn's configuration, codebase, memory engine, and persona modules.

---

## ⚙️ Core Capabilities

- **Persona-Oriented AI Routing**: Modular sub-agents (Echo, Tasky, API_Guy, Spock, BUB0, Kunda_AI) handle specialized functions via command delegation.
- **Persistent Profile**: Glenn operates with a live JSON-based profile and memory system, versioned and synced locally.
- **Compliance Ready**: Engineered with ISO 27001, CMMC, and NIST 800-53 alignment via the Spock persona.
- **Custom CLI or Web Control**: Modular structure supports CLI interfaces, Flask integration, and future voice-command control.

---

## 🧩 Structure

```shell
glenn/
├── manifests/             # Activation schema + routing manifest
│   └── glenn_manifest.json
├── profiles/              # Core identity and skillset
│   └── digital_twin.json
├── core/                  # Routing, memory sync, twin loader
│   ├── twin_loader.py
│   ├── memory_sync.py
│   ├── persona_router.py
│   └── logger.py
├── agents/                # Specialized personas (AI modules)
│   ├── echo.py
│   ├── tasky.py
│   ├── spock.py
│   └── api_guy.py
├── storage/               # Local memory DB and logs
│   └── glenn_memory.db
├── tests/                 # Test scripts
├── README.md
└── main.py                # System entry point
# glenn.ai
