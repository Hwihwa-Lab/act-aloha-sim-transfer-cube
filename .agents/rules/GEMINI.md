# Agentic & Gemini Coding Protocol for Aloha LeRobot

## Guidelines for AI Assistants & Autonomous Agents

1. **Architecture Integrity**:
   - `aloha_env.py`: Pure physics simulation & sensor rendering.
   - `policy_runner.py`: ACT inference & action chunking.
   - `metrics_tracker.py`: Benchmark metrics calculation.
   - `telemetry_hud.py`: 60fps HUD visualization.
   - `run_aloha_sim.py`: Main interactive loop.

2. **Low-Resource PC Protection**:
   - Keep memory usage under 500MB RAM.
   - Use direct buffer sharing between MuJoCo offscreen renderers and OpenCV canvases.

3. **Benchmarking Standard**:
   - Success criterion: 6D cube placement & stable handover into target zone.
   - Jerk smoothness metric: Root mean square of actuator force delta.
