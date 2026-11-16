#!/usr/bin/env python3
"""
⚡ MCP Creator — Connect Anything: 1-Click Skill Installer (`install_skill.py`)
==============================================================================
Installs the `mcp-creator-connect-anything` Skill globally across:
  - Google Antigravity (`~/.gemini/config/skills/mcp-creator-connect-anything/`)
  - Claude Code (`~/.claude/skills/mcp-creator-connect-anything/`)
  - Cursor (`~/.cursor/skills/mcp-creator-connect-anything/`)
"""

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SKILL_SRC = BASE_DIR / "SKILL.md"
TEMPLATES_SRC = BASE_DIR / "templates"
CREATE_MCP_SRC = BASE_DIR / "create_mcp.py"


def main():
    print("=" * 72)
    print("  ⚡ INSTALLING SKILL: MCP CREATOR — CONNECT ANYTHING")
    print("=" * 72)

    home = Path.home()
    targets = [
        home / ".gemini" / "config" / "skills" / "mcp-creator-connect-anything",
        home / ".gemini" / "antigravity" / "skills" / "mcp-creator-connect-anything",
        home / ".claude" / "skills" / "mcp-creator-connect-anything",
        home / ".cursor" / "skills" / "mcp-creator-connect-anything",
    ]

    for dest in targets:
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SKILL_SRC, dest / "SKILL.md")
        shutil.copy2(CREATE_MCP_SRC, dest / "create_mcp.py")
        if TEMPLATES_SRC.exists():
            dest_tpl = dest / "templates"
            dest_tpl.mkdir(parents=True, exist_ok=True)
            for item in TEMPLATES_SRC.iterdir():
                if item.is_file():
                    shutil.copy2(item, dest_tpl / item.name)
        print(f"  [OK] Installed in: {dest}")

    print("\n✅ Skill `mcp-creator-connect-anything` installed successfully!")
    print("   Now just tell your AI Agent: 'Crie um MCP para o site X usando o MCP Creator!'")


if __name__ == "__main__":
    main()
