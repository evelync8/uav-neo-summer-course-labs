"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2 · Module 4 — Downward Camera (Gate Detection) — Main orchestrator

Runs every step in sequence against the simulator:
    drone sim module4_downward/main.py
Run a single step directly instead:
    drone sim tasks/<step_file>.py
"""

# -- Course setup: makes the shared `neo_lab` helper importable (don't edit). --
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.realpath(__file__))
while _os.path.basename(_d) != "labs" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
import neo_lab

from tasks import (
    step1_find_contours,
    step2_largest_object,
    step3_track_object,
)

neo_lab.run_module("Week 2 · Module 4 — Downward Camera (Gate Detection)", [
    ("Step 1: Find Gate Contours", step1_find_contours),
    ("Step 2: Largest Gate", step2_largest_object),
    ("Step 3: Center Over the Gate", step3_track_object),
])
