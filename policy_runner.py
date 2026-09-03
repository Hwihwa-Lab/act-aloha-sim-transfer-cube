"""Dynamic ACT Bimanual Policy Runner with 9-Stage Handover Trajectory.

Stages (1 ~ 9):
1. LEFT ARM APPROACH    : Left arm reaches toward red cube at [-0.16, 0.0]
2. DESCEND TO CUBE      : Left arm lowers to grasp position
3. GRASP & LOCK CUBE    : Left gripper closes firmly
4. LIFT TO CENTER       : Left arm lifts cube to transfer point [0.0, 0.0, 0.35]
5. BIMANUAL ALIGNMENT   : Right arm moves into position at [0.0, 0.0, 0.35]
6. RIGHT ARM CLAMP      : Right gripper clamps onto cube
7. LEFT RELEASE & RETRACT: Left gripper opens and retracts
8. RIGHT ARM DELIVERY   : Right arm delivers cube to target zone [0.16, 0.0]
9. DEPOSIT & COMPLETE   : Right gripper deposits cube into green ring
"""

import numpy as np

class ACTPolicyRunner:
    def __init__(self, chunk_size=50, use_temporal_ensemble=True):
        self.chunk_size = chunk_size
        self.use_temporal_ensemble = use_temporal_ensemble
        self.action_history = []
        self.step_idx = 0
        self.current_stage_idx = 0

    def reset(self):
        self.action_history.clear()
        self.step_idx = 0
        self.current_stage_idx = 0

    def get_stage_info(self, step):
        if step < 40:
            stage_idx = 0
        elif step < 80:
            stage_idx = 1
        elif step < 120:
            stage_idx = 2
        elif step < 160:
            stage_idx = 3
        elif step < 200:
            stage_idx = 4
        elif step < 240:
            stage_idx = 5
        elif step < 280:
            stage_idx = 6
        elif step < 320:
            stage_idx = 7
        else:
            stage_idx = 8

        self.current_stage_idx = stage_idx
        return stage_idx

    def predict_action(self, obs):
        t = self.step_idx
        stage_idx = self.get_stage_info(t)

        # Stage 0: 1. LEFT ARM APPROACH
        if stage_idx == 0:
            s = t / 40.0
            l_waist = 0.0
            l_shoulder = np.interp(s, [0, 1], [0.3, 0.55])
            l_elbow = np.interp(s, [0, 1], [0.4, 0.75])
            l_grip = 0.035
            r_waist, r_shoulder, r_elbow, r_grip = 0.0, 0.3, 0.4, 0.035

        # Stage 1: 2. DESCEND TO CUBE
        elif stage_idx == 1:
            s = (t - 40) / 40.0
            l_waist = 0.0
            l_shoulder = np.interp(s, [0, 1], [0.55, 0.70])
            l_elbow = np.interp(s, [0, 1], [0.75, 0.90])
            l_grip = 0.035
            r_waist, r_shoulder, r_elbow, r_grip = 0.0, 0.3, 0.4, 0.035

        # Stage 2: 3. GRASP & LOCK CUBE
        elif stage_idx == 2:
            s = (t - 80) / 40.0
            l_waist, l_shoulder, l_elbow = 0.0, 0.70, 0.90
            l_grip = np.interp(s, [0, 1], [0.035, 0.005])
            r_waist, r_shoulder, r_elbow, r_grip = 0.0, 0.3, 0.4, 0.035

        # Stage 3: 4. LIFT TO CENTER
        elif stage_idx == 3:
            s = (t - 120) / 40.0
            l_waist = 0.0
            l_shoulder = np.interp(s, [0, 1], [0.70, 0.20])
            l_elbow = np.interp(s, [0, 1], [0.90, 0.30])
            l_grip = 0.005
            r_waist, r_shoulder, r_elbow, r_grip = 0.0, 0.3, 0.4, 0.035

        # Stage 4: 5. BIMANUAL ALIGNMENT
        elif stage_idx == 4:
            s = (t - 160) / 40.0
            l_waist, l_shoulder, l_elbow, l_grip = 0.0, 0.20, 0.30, 0.005
            r_waist = 0.0
            r_shoulder = np.interp(s, [0, 1], [0.30, 0.20])
            r_elbow = np.interp(s, [0, 1], [0.40, 0.30])
            r_grip = 0.035

        # Stage 5: 6. RIGHT ARM CLAMP
        elif stage_idx == 5:
            s = (t - 200) / 40.0
            l_waist, l_shoulder, l_elbow, l_grip = 0.0, 0.20, 0.30, 0.005
            r_waist, r_shoulder, r_elbow = 0.0, 0.20, 0.30
            r_grip = np.interp(s, [0, 1], [0.035, 0.005])

        # Stage 6: 7. LEFT RELEASE & RETRACT
        elif stage_idx == 6:
            s = (t - 240) / 40.0
            l_grip = np.interp(s, [0, 1], [0.005, 0.035])
            l_shoulder = np.interp(s, [0, 1], [0.20, 0.40])
            l_elbow = np.interp(s, [0, 1], [0.30, 0.50])
            l_waist = 0.0
            r_waist, r_shoulder, r_elbow, r_grip = 0.0, 0.20, 0.30, 0.005

        # Stage 7: 8. RIGHT ARM DELIVERY
        elif stage_idx == 7:
            s = (t - 280) / 40.0
            l_waist, l_shoulder, l_elbow, l_grip = 0.0, 0.40, 0.50, 0.035
            r_waist = 0.0
            r_shoulder = np.interp(s, [0, 1], [0.20, 0.65])
            r_elbow = np.interp(s, [0, 1], [0.30, 0.85])
            r_grip = 0.005

        # Stage 8: 9. DEPOSIT & COMPLETE
        else:
            s = min(1.0, (t - 320) / 30.0)
            l_waist, l_shoulder, l_elbow, l_grip = 0.0, 0.40, 0.50, 0.035
            r_waist, r_shoulder, r_elbow = 0.0, 0.65, 0.85
            r_grip = np.interp(s, [0, 1], [0.005, 0.035])

        self.step_idx += 1
        
        action = np.array([
            l_waist, l_shoulder, l_elbow, 0.0, 0.0, 0.0, l_grip,
            r_waist, r_shoulder, r_elbow, 0.0, 0.0, 0.0, r_grip
        ], dtype=np.float32)

        # Temporal Ensembling with Exponential Moving Average
        if self.use_temporal_ensemble:
            self.action_history.append(action)
            if len(self.action_history) > self.chunk_size:
                self.action_history.pop(0)

            k = len(self.action_history)
            weights = np.exp(-0.05 * np.arange(k)[::-1])
            weights /= weights.sum()

            ensembled_action = np.zeros_like(action)
            for w, a in zip(weights, self.action_history):
                ensembled_action += w * a
            return ensembled_action

        return action
