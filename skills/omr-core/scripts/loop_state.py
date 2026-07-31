#!/usr/bin/env python3
"""
Loop state helper for OmniResearch Loop pattern / Gate L.

Artifact-bound state lives at <workspace>/.omr/loop-state.json.
Skills present Gate L only when Loop pattern is active OR this file has
active: true.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

LOOP_STATE_FILENAME = "loop-state.json"
VALID_MODES = ("idea-dev", "deep-analyze")


def loop_state_path(workspace_root: Path) -> Path:
    """Return path to .omr/loop-state.json."""
    return Path(workspace_root) / ".omr" / LOOP_STATE_FILENAME


def default_state(
    mode: str = "deep-analyze",
    focus_question: str = "",
    exit_target: str = "omr-decision",
) -> Dict[str, Any]:
    """Create a fresh loop-state document."""
    if mode not in VALID_MODES:
        raise ValueError(f"mode must be one of {VALID_MODES}, got {mode!r}")
    return {
        "active": True,
        "mode": mode,
        "iteration": 0,
        "focus_question": focus_question,
        "last_delta": "",
        "exit_target": exit_target,
        "gaps": [],
        "history": [],
        "updated_at": _now_iso(),
    }


def load_loop_state(workspace_root: Path) -> Optional[Dict[str, Any]]:
    """Load loop state if present; return None if missing."""
    path = loop_state_path(workspace_root)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_loop_state(workspace_root: Path, state: Dict[str, Any]) -> Path:
    """Write loop state; ensures .omr/ exists."""
    path = loop_state_path(workspace_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    state = dict(state)
    state["updated_at"] = _now_iso()
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return path


def is_loop_active(workspace_root: Path, pattern_name: Optional[str] = None) -> bool:
    """
    True when Gate L should be presented.

    Active if pattern_name is Loop (case-insensitive) OR loop-state.active is True.
    """
    if pattern_name and pattern_name.strip().lower() == "loop":
        return True
    state = load_loop_state(workspace_root)
    return bool(state and state.get("active"))


def activate_loop(
    workspace_root: Path,
    mode: str,
    focus_question: str = "",
    exit_target: Optional[str] = None,
) -> Dict[str, Any]:
    """Start or restart a Loop with the given mode."""
    if exit_target is None:
        exit_target = "omr-decision"
    state = default_state(
        mode=mode, focus_question=focus_question, exit_target=exit_target
    )
    save_loop_state(workspace_root, state)
    return state


def record_iteration(
    workspace_root: Path,
    *,
    focus_question: Optional[str] = None,
    last_delta: str = "",
    gaps: Optional[List[str]] = None,
    action: str = "iterate",
) -> Dict[str, Any]:
    """
    Increment iteration and append a history entry (Gate L → Iterate).

    Does not deactivate the loop.
    """
    state = load_loop_state(workspace_root) or default_state()
    state["active"] = True
    state["iteration"] = int(state.get("iteration", 0)) + 1
    if focus_question is not None:
        state["focus_question"] = focus_question
    if last_delta:
        state["last_delta"] = last_delta
    if gaps is not None:
        state["gaps"] = list(gaps)

    history = list(state.get("history") or [])
    history.append(
        {
            "iteration": state["iteration"],
            "action": action,
            "focus_question": state.get("focus_question", ""),
            "last_delta": last_delta,
            "at": _now_iso(),
        }
    )
    state["history"] = history
    save_loop_state(workspace_root, state)
    return state


def advance_loop(
    workspace_root: Path,
    *,
    last_delta: str = "Gate L advance",
) -> Dict[str, Any]:
    """
    Exit the loop (Gate L → Advance). Sets active=False; keeps history.
    """
    state = load_loop_state(workspace_root) or default_state()
    state["active"] = False
    state["last_delta"] = last_delta
    history = list(state.get("history") or [])
    history.append(
        {
            "iteration": int(state.get("iteration", 0)),
            "action": "advance",
            "focus_question": state.get("focus_question", ""),
            "last_delta": last_delta,
            "exit_target": state.get("exit_target", "omr-decision"),
            "at": _now_iso(),
        }
    )
    state["history"] = history
    save_loop_state(workspace_root, state)
    return state


def park_loop(
    workspace_root: Path,
    *,
    last_delta: str = "Gate L stop/park",
) -> Dict[str, Any]:
    """Park the loop without unlocking next stage (Gate L → Stop/park)."""
    state = load_loop_state(workspace_root) or default_state()
    state["active"] = False
    state["last_delta"] = last_delta
    history = list(state.get("history") or [])
    history.append(
        {
            "iteration": int(state.get("iteration", 0)),
            "action": "park",
            "focus_question": state.get("focus_question", ""),
            "last_delta": last_delta,
            "at": _now_iso(),
        }
    )
    state["history"] = history
    save_loop_state(workspace_root, state)
    return state


def get_gaps(workspace_root: Path) -> List[str]:
    """Return current evidence/idea gaps listed in loop state."""
    state = load_loop_state(workspace_root)
    if not state:
        return []
    return list(state.get("gaps") or [])


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> None:
    """CLI: loop_state.py <workspace> [--status|--activate MODE|--iterate|--advance|--park]"""
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: loop_state.py <workspace> "
            "[--status | --activate <mode> | --iterate | --advance | --park]"
        )
        sys.exit(1)

    workspace = Path(sys.argv[1])
    args = sys.argv[2:]

    if not args or args[0] == "--status":
        state = load_loop_state(workspace)
        if state is None:
            print("No loop-state.json (inactive)")
        else:
            print(json.dumps(state, indent=2))
        return

    if args[0] == "--activate":
        mode = args[1] if len(args) > 1 else "deep-analyze"
        focus = args[2] if len(args) > 2 else ""
        state = activate_loop(workspace, mode=mode, focus_question=focus)
        print(f"✓ Loop activated ({mode})")
        print(json.dumps(state, indent=2))
        return

    if args[0] == "--iterate":
        state = record_iteration(workspace, last_delta="CLI iterate")
        print(f"✓ Iteration {state['iteration']}")
        return

    if args[0] == "--advance":
        state = advance_loop(workspace)
        print(f"✓ Advanced → {state.get('exit_target')}")
        return

    if args[0] == "--park":
        park_loop(workspace)
        print("✓ Loop parked")
        return

    print(f"Unknown option: {args[0]}")
    sys.exit(1)


if __name__ == "__main__":
    main()
