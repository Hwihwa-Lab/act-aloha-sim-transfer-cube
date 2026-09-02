"""Quantitative Metrics Tracker for AI Robotics Benchmarking.

Tracks:
- Task Success Rate (Cumulative & Episode-wise)
- Phase Milestones (Grasp -> Align -> Transfer -> Placement)
- Time-to-Success (Seconds and Step count)
- Energy & Jerk Metrics (Joint torque smoothness, derivative of force)
"""

import numpy as np
import time

class MetricsTracker:
    def __init__(self):
        self.total_episodes = 0
        self.successful_episodes = 0
        self.current_episode = 0
        self.episode_start_time = 0.0
        self.time_to_success = None
        self.step_to_success = None
        self.prev_torques = None
        self.jerk_accum = 0.0
        self.jerk_count = 0
        self.phase_milestones = {
            "PHASE 1: LEFT ARM GRASPED": False,
            "PHASE 2: BIMANUAL ALIGNMENT": False,
            "PHASE 3: HANDOVER TO RIGHT ARM": False,
            "PHASE 4: PLACED IN TARGET": False,
        }

    def start_episode(self, episode_idx):
        self.current_episode = episode_idx
        self.episode_start_time = time.time()
        self.time_to_success = None
        self.step_to_success = None
        self.prev_torques = None
        self.jerk_accum = 0.0
        self.jerk_count = 0
        for k in self.phase_milestones:
            self.phase_milestones[k] = False

    def update(self, step, obs, info):
        # Update milestone
        phase = info.get("phase", "")
        if phase in self.phase_milestones:
            self.phase_milestones[phase] = True

        # Check success
        if info.get("success", False) and self.time_to_success is None:
            self.time_to_success = time.time() - self.episode_start_time
            self.step_to_success = step

        # Compute Jerk / Smoothness (Delta Torque)
        torques = obs["torques"]
        if self.prev_torques is not None:
            dt_torque = np.linalg.norm(torques - self.prev_torques)
            self.jerk_accum += dt_torque
            self.jerk_count += 1
        self.prev_torques = torques.copy()

    def end_episode(self, success):
        self.total_episodes += 1
        if success:
            self.successful_episodes += 1

    def get_summary(self):
        success_rate = (self.successful_episodes / max(1, self.total_episodes)) * 100.0
        avg_jerk = self.jerk_accum / max(1, self.jerk_count)
        elapsed = time.time() - self.episode_start_time
        return {
            "total_episodes": self.total_episodes,
            "successful_episodes": self.successful_episodes,
            "success_rate": success_rate,
            "time_to_success": self.time_to_success if self.time_to_success else elapsed,
            "step_to_success": self.step_to_success,
            "avg_jerk": avg_jerk,
            "milestones": self.phase_milestones,
        }
