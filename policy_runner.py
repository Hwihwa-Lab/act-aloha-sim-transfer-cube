"""LeRobot ACT Policy Runner with 9-Stage Fine-Grained Handover Trajectory.

Matches the mentor's 9-stage sequence:
[1] 1. LEFT ARM APPROACH
[2] 2. DESCEND TO CUBE
[3] 3. GRASP & LOCK CUBE
[4] 4. LIFT TO CENTER
[5] 5. BIMANUAL ALIGNMENT
[6] 6. RIGHT ARM CLAMP
[7] 7. LEFT RELEASE & RETRACT
[8] 8. RIGHT ARM DELIVERY
[9] 9. DEPOSIT & COMPLETE
"""

import numpy as np

class ACTPolicyRunner:
    def __init__(self, chunk_size=50, use_temporal_ensemble=True):
        self.chunk_size = chunk_size
        self.use_temporal_ensemble = use_temporal_ensemble
        self.step_idx = 0
        self.current_stage_idx = 0  # 0 to 8 (Stage 1 to 9)

    def reset(self):
        self.step_idx = 0
        self.current_stage_idx = 0

    def get_stage_info(self, step):
        # Stage thresholds (Total 360 steps, ~40 steps per stage)
        if step < 40:
            stage_idx = 0  # 1. LEFT ARM APPROACH
        elif step < 80:
            stage_idx = 1  # 2. DESCEND TO CUBE
        elif step < 120:
            stage_idx = 2  # 3. GRASP & LOCK CUBE
        elif step < 160:
            stage_idx = 3  # 4. LIFT TO CENTER
        elif step < 200:
            stage_idx = 4  # 5. BIMANUAL ALIGNMENT
        elif step < 240:
            stage_idx = 5  # 6. RIGHT ARM CLAMP
        elif step < 280:
            stage_idx = 6  # 7. LEFT RELEASE & RETRACT
        elif step < 320:
            stage_idx = 7  # 8. RIGHT ARM DELIVERY
        else:
            stage_idx = 8  # 9. DEPOSIT & COMPLETE

        self.current_stage_idx = stage_idx
        return stage_idx

    def predict_action(self, obs):
        t = self.step_idx
        stage_idx = self.get_stage_info(t)

        # Left Arm: [waist, shoulder, elbow, f_roll, w_pitch, w_roll, grip]
        # Right Arm: [waist, shoulder, elbow, f_roll, w_pitch, w_roll, grip]
        
        # Stage 0 (t: 0..40): 1. LEFT ARM APPROACH
        if stage_idx == 0:
            s = t / 40.0
            l_waist = np.interp(s, [0, 1], [0.0, 0.25])
            l_shoulder = np.interp(s, [0, 1], [0.3, 0.45])
            l_elbow = np.interp(s, [0, 1], [0.4, 0.65])
            l_grip = 0.035
            r_waist, r_shoulder, r_elbow, r_grip = -0.2, 0.3, 0.4, 0.035

        # Stage 1 (t: 40..80): 2. DESCEND TO CUBE
        elif stage_idx == 1:
            s = (t - 40) / 40.0
            l_waist = 0.25
            l_shoulder = np.interp(s, [0, 1], [0.45, 0.65])
            l_elbow = np.interp(s, [0, 1], [0.65, 0.85])
            l_grip = 0.035
            r_waist, r_shoulder, r_elbow, r_grip = -0.2, 0.3, 0.4, 0.035

        # Stage 2 (t: 80..120): 3. GRASP & LOCK CUBE
        elif stage_idx == 2:
            s = (t - 80) / 40.0
            l_waist, l_shoulder, l_elbow = 0.25, 0.65, 0.85
            l_grip = np.interp(s, [0, 1], [0.035, 0.005])  # Gripper clamp
            r_waist, r_shoulder, r_elbow, r_grip = -0.2, 0.3, 0.4, 0.035

        # Stage 3 (t: 120..160): 4. LIFT TO CENTER
        elif stage_idx == 3:
            s = (t - 120) / 40.0
            l_waist = np.interp(s, [0, 1], [0.25, 0.50])
            l_shoulder = np.interp(s, [0, 1], [0.65, 0.35])
            l_elbow = np.interp(s, [0, 1], [0.85, 0.55])
            l_grip = 0.005
            r_waist = np.interp(s, [0, 1], [-0.2, -0.45])
            r_shoulder = np.interp(s, [0, 1], [0.3, 0.35])
            r_elbow = np.interp(s, [0, 1], [0.4, 0.55])
            r_grip = 0.035

        # Stage 4 (t: 160..200): 5. BIMANUAL ALIGNMENT
        elif stage_idx == 4:
            s = (t - 160) / 40.0
            l_waist, l_shoulder, l_elbow, l_grip = 0.50, 0.35, 0.55, 0.005
            r_waist = np.interp(s, [0, 1], [-0.45, -0.52])
            r_shoulder = 0.35
            r_elbow = 0.55
            r_grip = 0.035

        # Stage 5 (t: 200..240): 6. RIGHT ARM CLAMP
        elif stage_idx == 5:
            s = (t - 200) / 40.0
            l_waist, l_shoulder, l_elbow, l_grip = 0.50, 0.35, 0.55, 0.005
            r_waist, r_shoulder, r_elbow = -0.52, 0.35, 0.55
            r_grip = np.interp(s, [0, 1], [0.035, 0.005])  # Right gripper clamp

        # Stage 6 (t: 240..280): 7. LEFT RELEASE & RETRACT
        elif stage_idx == 6:
            s = (t - 240) / 40.0
            l_grip = np.interp(s, [0, 1], [0.005, 0.035])  # Left release
            l_waist = np.interp(s, [0, 1], [0.50, 0.15])
            l_shoulder = np.interp(s, [0, 1], [0.35, 0.25])
            l_elbow = 0.4
            r_waist, r_shoulder, r_elbow, r_grip = -0.52, 0.35, 0.55, 0.005

        # Stage 7 (t: 280..320): 8. RIGHT ARM DELIVERY
        elif stage_idx == 7:
            s = (t - 280) / 40.0
            l_waist, l_shoulder, l_elbow, l_grip = 0.15, 0.25, 0.4, 0.035
            r_waist = np.interp(s, [0, 1], [-0.52, -0.25])
            r_shoulder = np.interp(s, [0, 1], [0.35, 0.60])
            r_elbow = np.interp(s, [0, 1], [0.55, 0.80])
            r_grip = 0.005

        # Stage 8 (t >= 320): 9. DEPOSIT & COMPLETE
        else:
            s = min(1.0, (t - 320) / 30.0)
            l_waist, l_shoulder, l_elbow, l_grip = 0.15, 0.25, 0.4, 0.035
            r_waist, r_shoulder, r_elbow = -0.25, 0.60, 0.80
            r_grip = np.interp(s, [0, 1], [0.005, 0.035])  # Deposit release

        self.step_idx += 1
        
        action = np.array([
            l_waist, l_shoulder, l_elbow, 0.0, 0.0, 0.0, l_grip,
            r_waist, r_shoulder, r_elbow, 0.0, 0.0, 0.0, r_grip
        ], dtype=np.float32)

        return action
