# System Architecture - Aloha 14-DOF LeRobot Simulation

```mermaid
graph TD
    subgraph Physics_Engine [MuJoCo 3.x Physics Engine]
        MJCF[Aloha MJCF XML Definition] --> Sim[Physical World Step 500Hz]
        Sim --> Render[Multi-camera Offscreen Renderers]
        Sim --> Sensors[Joint Positions & Torques]
    end

    subgraph Perception_And_Policy [AI Policy Pipeline]
        Sensors --> Obs[Observation Dict]
        Render --> Obs
        Obs --> ACT[Action Chunking Transformer Policy]
        ACT --> Temporal[Temporal Ensembling 50-Horizon]
        Temporal --> Act14[14-DOF Target Angles]
    end

    subgraph Benchmark_Metrics [Quantitative Evaluation Tracker]
        Sim --> Contact[Cube Handover & Zone Detection]
        Sensors --> Jerk[Torque Delta Smoothness Metric]
        Contact --> Success[Task Success & Milestone Tracker]
    end

    subgraph Low_Overhead_HUD [60fps OpenCV Telemetry HUD]
        Render --> FrameCanvas[1280x720 Dark Canvas]
        Sensors --> Gauges[14 Joint Gauge Bars & Torque]
        Success --> AIPanel[Milestones & Success Rate]
        Jerk --> AIPanel
    end

    Act14 --> Sim
```

## Module Responsibility
1. `aloha_env.py`: Encapsulates MuJoCo XML, kinematics, contacts, and multi-camera views.
2. `policy_runner.py`: Implements ACT Action Chunking and Temporal Ensembling.
3. `metrics_tracker.py`: Computes research-grade metrics (Success, Time, Jerk).
4. `telemetry_hud.py`: Delivers 60fps real-time visualization with zero memory leak.
5. `run_aloha_sim.py`: Manages the overall execution loop and CLI options.
