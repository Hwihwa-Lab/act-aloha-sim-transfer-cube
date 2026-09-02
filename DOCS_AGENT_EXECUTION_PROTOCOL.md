# Agent Execution Protocol - Aloha 14-DOF

## Execution Pipeline

1. **Step 1: Environment Instantiation**
   - Initialize `AlohaEnv()`.
   - Validate camera renderers and physics time-step.

2. **Step 2: Policy & Metric Binding**
   - Bind `ACTPolicyRunner()` with 50-step chunk horizon.
   - Initialize `MetricsTracker()` and reset episode states.

3. **Step 3: Rollout Loop Execution**
   - Execute 50Hz control loop (10 MuJoCo sub-steps per cycle).
   - Render HUD at 60fps with telemetry overlay.

4. **Step 4: Benchmark Aggregation**
   - Compute cumulative success rate, time-to-success, and torque jerk smoothness.
   - Print final research report to console.
