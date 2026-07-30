#!/usr/bin/env python3
"""
Runtime Utilities Proxy — delegates to canonical module in omr-core/scripts/

Domain skills carry this thin proxy instead of a full 294-line copy.
The proxy locates omr-core/scripts/runtime_utils.py and re-exports all
public functions, so calling code remains unchanged:

    from runtime_utils import load_infrastructure
    infra = load_infrastructure(workspace_root)
"""

import importlib.util
import sys
from pathlib import Path


def _load_canonical():
    """Find and load the canonical runtime_utils from omr-core/scripts/"""
    search_paths = []

    # 1. Relative to this file (sibling skill in workspace or repo)
    #    Works for scripts/ and utils/ subdirectories alike
    search_paths.append(
        Path(__file__).resolve().parent.parent.parent / 'omr-core' / 'scripts'
    )

    # 2. Workspace installation: walk up from cwd to find skills/omr-core/scripts/
    cwd = Path.cwd()
    for _ in range(10):
        search_paths.append(cwd / 'skills' / 'omr-core' / 'scripts')
        if cwd.parent == cwd:
            break
        cwd = cwd.parent

    # 3. Global marketplace installation
    search_paths.append(Path.home() / '.claude' / 'skills' / 'omr-core' / 'scripts')

    for scripts_dir in search_paths:
        target = scripts_dir / 'runtime_utils.py'
        if target.exists():
            spec = importlib.util.spec_from_file_location(
                'omr_core_runtime_utils', target
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

    raise ImportError(
        "OmniResearch infrastructure not found. "
        "Install omr-core skill first, then initialize workspace with omr-bootstrap.\n"
        "  1. /find-skills omr-core\n"
        "  2. /omr-bootstrap <project-name> <research-question>"
    )


# Load canonical module and re-export all public functions
_rt = _load_canonical()
load_infrastructure = _rt.load_infrastructure
check_skill_dependency = _rt.check_skill_dependency
update_skill_tree = _rt.update_skill_tree
get_skill_tree_visualization = _rt.get_skill_tree_visualization
validate_contract = _rt.validate_contract
load_global_infrastructure = _rt.load_global_infrastructure

if __name__ == "__main__":
    import runpy
    runpy.run_path(str(Path(_rt.__file__).resolve()), run_name="__main__")
