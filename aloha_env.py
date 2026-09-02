"""Aloha Bimanual (14-DOF) MuJoCo Physics Environment.

Features:
- Fixed Cube Physics: Perfectly resting red cube on table surface without collision pop/fall.
- Studio Studio Lighting & Materials: Realistic metallic gray robot arms without white overexposure.
- 3 Perfectly Centered Multi-Angle Camera Perspectives:
  1) top_cam: Overhead Top-down bimanual symmetry view
  2) iso_cam: 3D Isometric 45-degree angled view (Centered focus on table & arms)
  3) front_cam: Eye-level frontal close-up action view (Centered handover view)
- Dual Wrist Camera Renderers (L-Wrist & R-Wrist)
"""

import mujoco
import numpy as np

ALOHA_MJCF_XML = """
<mujoco model="aloha_3d_bimanual_simulator">
  <compiler angle="radian" coordinate="local" meshdir="." autolimits="true"/>
  <option timestep="0.002" integrator="implicitfast" gravity="0 0 -9.81"/>

  <visual>
    <headlight ambient="0.32 0.32 0.36" diffuse="0.48 0.48 0.52" specular="0.15 0.15 0.15"/>
    <global offwidth="1280" offheight="720"/>
    <quality shadowsize="4096"/>
  </visual>

  <default>
    <joint limited="true" damping="0.8" armature="0.01"/>
    <geom condim="6" friction="2.5 0.1 0.005" solimp="0.99 0.99 0.01" solref="0.005 1"/>
    <motor ctrlrange="-3.14 3.14"/>
  </default>

  <worldbody>
    <!-- Dark Studio Floor -->
    <geom name="floor" type="plane" size="5 5 0.1" rgba="0.12 0.14 0.18 1"/>
    
    <!-- Balanced Studio Key Lights -->
    <light directional="true" pos="0 -0.5 2.5" dir="0 0.2 -1" diffuse="0.65 0.65 0.70" specular="0.2 0.2 0.2" castshadow="true"/>
    <light directional="false" pos="-1.5 0.5 2.0" diffuse="0.35 0.35 0.40"/>
    <light directional="false" pos="1.5 -0.5 2.0" diffuse="0.35 0.35 0.40"/>

    <!-- Workbench Table (Surface at z = 0.22) -->
    <body name="table" pos="0 0 0.20">
      <geom name="table_top" type="box" size="0.65 0.40 0.02" rgba="0.22 0.25 0.30 1"/>
      
      <!-- Target drop zone with glowing green ring -->
      <site name="target_zone" type="cylinder" size="0.065 0.002" pos="0.16 0 0.021" rgba="0.2 0.90 0.45 0.6"/>
    </body>

    <!-- Red Transfer Cube (Solidly seated at z = 0.245) -->
    <body name="cube" pos="-0.16 0 0.245">
      <freejoint name="cube_joint"/>
      <geom name="cube_geom" type="box" size="0.024 0.024 0.024" rgba="0.95 0.12 0.12 1" mass="0.04"/>
    </body>

    <!-- ================= 3 PRO CENTERED CAMERA PERSPECTIVES ================= -->
    <!-- 1. Overhead Top-Down View (Looking straight down at table center) -->
    <camera name="top_cam" pos="0 0.05 0.95" xyaxes="1 0 0 0 1 0"/>
    
    <!-- 2. 3D Isometric 45-Degree View (Accurately looking at table center [0, 0.05, 0.22]) -->
    <camera name="iso_cam" pos="0 -0.80 0.70" xyaxes="1 0 0 0 0.4917 0.8708"/>

    <!-- 3. Front Eye-Level Action View (Accurately looking at bimanual workspace) -->
    <camera name="front_cam" pos="0 -0.65 0.40" xyaxes="1 0 0 0 0.2490 0.9685"/>

    <!-- ================= LEFT ARM (6 DOF + Gripper) ================= -->
    <body name="left_base" pos="-0.48 0 0.25">
      <geom type="cylinder" size="0.05 0.03" rgba="0.25 0.28 0.32 1"/>
      
      <body name="left_waist" pos="0 0 0.03">
        <joint name="left_waist" type="hinge" axis="0 0 1" range="-2.6 2.6"/>
        <geom type="cylinder" size="0.04 0.03" rgba="0.55 0.60 0.65 1"/>
        
        <body name="left_shoulder" pos="0 0 0.04">
          <joint name="left_shoulder" type="hinge" axis="0 1 0" range="-1.8 1.8"/>
          <geom type="capsule" fromto="0 0 0 0.14 0 0" size="0.032" rgba="0.75 0.78 0.82 1"/>
          
          <body name="left_elbow" pos="0.14 0 0">
            <joint name="left_elbow" type="hinge" axis="0 1 0" range="-2.2 2.2"/>
            <geom type="capsule" fromto="0 0 0 0.14 0 0" size="0.028" rgba="0.60 0.64 0.68 1"/>
            
            <body name="left_forearm_roll" pos="0.14 0 0">
              <joint name="left_forearm_roll" type="hinge" axis="1 0 0" range="-2.6 2.6"/>
              <geom type="cylinder" size="0.025 0.025" quat="0.707 0 0.707 0" rgba="0.75 0.78 0.82 1"/>
              
              <body name="left_wrist_pitch" pos="0.035 0 0">
                <joint name="left_wrist_pitch" type="hinge" axis="0 1 0" range="-1.6 1.6"/>
                <geom type="cylinder" size="0.022 0.02" rgba="0.55 0.60 0.65 1"/>
                
                <body name="left_wrist_roll" pos="0.03 0 0">
                  <joint name="left_wrist_roll" type="hinge" axis="1 0 0" range="-2.6 2.6"/>
                  <geom type="box" size="0.022 0.026 0.018" rgba="0.30 0.35 0.40 1"/>
                  <camera name="left_wrist_cam" pos="0.04 0 0.04" quat="0.707 0 0.707 0"/>
                  
                  <!-- Left Gripper Fingers -->
                  <body name="left_finger_l" pos="0.025 -0.018 0">
                    <joint name="left_gripper" type="slide" axis="0 1 0" range="0 0.035"/>
                    <geom name="left_pad_l" type="box" size="0.022 0.006 0.015" rgba="0.70 0.74 0.78 1"/>
                  </body>
                  <body name="left_finger_r" pos="0.025 0.018 0">
                    <geom name="left_pad_r" type="box" size="0.022 0.006 0.015" rgba="0.70 0.74 0.78 1"/>
                  </body>
                </body>
              </body>
            </body>
          </body>
        </body>
      </body>
    </body>

    <!-- ================= RIGHT ARM (6 DOF + Gripper) ================= -->
    <body name="right_base" pos="0.48 0 0.25">
      <geom type="cylinder" size="0.05 0.03" rgba="0.25 0.28 0.32 1"/>
      
      <body name="right_waist" pos="0 0 0.03">
        <joint name="right_waist" type="hinge" axis="0 0 1" range="-2.6 2.6"/>
        <geom type="cylinder" size="0.04 0.03" rgba="0.55 0.60 0.65 1"/>
        
        <body name="right_shoulder" pos="0 0 0.04">
          <joint name="right_shoulder" type="hinge" axis="0 1 0" range="-1.8 1.8"/>
          <geom type="capsule" fromto="0 0 0 -0.14 0 0" size="0.032" rgba="0.75 0.78 0.82 1"/>
          
          <body name="right_elbow" pos="-0.14 0 0">
            <joint name="right_elbow" type="hinge" axis="0 1 0" range="-2.2 2.2"/>
            <geom type="capsule" fromto="0 0 0 -0.14 0 0" size="0.028" rgba="0.60 0.64 0.68 1"/>
            
            <body name="right_forearm_roll" pos="-0.14 0 0">
              <joint name="right_forearm_roll" type="hinge" axis="1 0 0" range="-2.6 2.6"/>
              <geom type="cylinder" size="0.025 0.025" quat="0.707 0 0.707 0" rgba="0.75 0.78 0.82 1"/>
              
              <body name="right_wrist_pitch" pos="-0.035 0 0">
                <joint name="right_wrist_pitch" type="hinge" axis="0 1 0" range="-1.6 1.6"/>
                <geom type="cylinder" size="0.022 0.02" rgba="0.55 0.60 0.65 1"/>
                
                <body name="right_wrist_roll" pos="-0.03 0 0">
                  <joint name="right_wrist_roll" type="hinge" axis="1 0 0" range="-2.6 2.6"/>
                  <geom type="box" size="0.022 0.026 0.018" rgba="0.30 0.35 0.40 1"/>
                  <camera name="right_wrist_cam" pos="-0.04 0 0.04" quat="0.707 0 -0.707 0"/>
                  
                  <!-- Right Gripper Fingers -->
                  <body name="right_finger_l" pos="-0.025 -0.018 0">
                    <joint name="right_gripper" type="slide" axis="0 1 0" range="0 0.035"/>
                    <geom name="right_pad_l" type="box" size="0.022 0.006 0.015" rgba="0.70 0.74 0.78 1"/>
                  </body>
                  <body name="right_finger_r" pos="-0.025 0.018 0">
                    <geom name="right_pad_r" type="box" size="0.022 0.006 0.015" rgba="0.70 0.74 0.78 1"/>
                  </body>
                </body>
              </body>
            </body>
          </body>
        </body>
      </body>
    </body>
  </worldbody>

  <actuator>
    <!-- Left Arm -->
    <position name="act_left_waist" joint="left_waist" kp="80" kv="5"/>
    <position name="act_left_shoulder" joint="left_shoulder" kp="80" kv="5"/>
    <position name="act_left_elbow" joint="left_elbow" kp="70" kv="4"/>
    <position name="act_left_forearm_roll" joint="left_forearm_roll" kp="40" kv="2"/>
    <position name="act_left_wrist_pitch" joint="left_wrist_pitch" kp="40" kv="2"/>
    <position name="act_left_wrist_roll" joint="left_wrist_roll" kp="30" kv="1.5"/>
    <position name="act_left_gripper" joint="left_gripper" kp="200" kv="10" ctrlrange="0 0.035"/>

    <!-- Right Arm -->
    <position name="act_right_waist" joint="right_waist" kp="80" kv="5"/>
    <position name="act_right_shoulder" joint="right_shoulder" kp="80" kv="5"/>
    <position name="act_right_elbow" joint="right_elbow" kp="70" kv="4"/>
    <position name="act_right_forearm_roll" joint="right_forearm_roll" kp="40" kv="2"/>
    <position name="act_right_wrist_pitch" joint="right_wrist_pitch" kp="40" kv="2"/>
    <position name="act_right_wrist_roll" joint="right_wrist_roll" kp="30" kv="1.5"/>
    <position name="act_right_gripper" joint="right_gripper" kp="200" kv="10" ctrlrange="0 0.035"/>
  </actuator>
</mujoco>
"""

STAGES_9 = [
    "1. LEFT ARM APPROACH",
    "2. DESCEND TO CUBE",
    "3. GRASP & LOCK CUBE",
    "4. LIFT TO CENTER",
    "5. BIMANUAL ALIGNMENT",
    "6. RIGHT ARM CLAMP",
    "7. LEFT RELEASE & RETRACT",
    "8. RIGHT ARM DELIVERY",
    "9. DEPOSIT & COMPLETE"
]

class AlohaEnv:
    def __init__(self, render_width=760, render_height=460):
        self.model = mujoco.MjModel.from_xml_string(ALOHA_MJCF_XML)
        self.data = mujoco.MjData(self.model)
        self.render_width = render_width
        self.render_height = render_height
        
        self.renderer_main = mujoco.Renderer(self.model, height=render_height, width=render_width)
        self.renderer_wrist_l = mujoco.Renderer(self.model, height=95, width=130)
        self.renderer_wrist_r = mujoco.Renderer(self.model, height=95, width=130)

        self.current_cam = "top_cam"

        self.actuator_ids = [i for i in range(14)]
        self.cube_body_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, "cube")
        self.reset()

    def set_camera(self, cam_name):
        self.current_cam = cam_name

    def reset(self, randomize_cube=False):
        mujoco.mj_resetData(self.model, self.data)
        
        initial_qpos = np.array([
            0.0, 0.3, 0.4, 0.0, 0.0, 0.0, 0.035,
            0.0, 0.3, 0.4, 0.0, 0.0, 0.0, 0.035
        ])
        
        for i, act_id in enumerate(self.actuator_ids):
            self.data.ctrl[act_id] = initial_qpos[i]

        cube_x = -0.16 + (np.random.uniform(-0.01, 0.01) if randomize_cube else 0.0)
        cube_y = 0.0 + (np.random.uniform(-0.01, 0.01) if randomize_cube else 0.0)
        self.data.qpos[14:17] = [cube_x, cube_y, 0.245]
        self.data.qpos[17:21] = [1.0, 0.0, 0.0, 0.0]

        for _ in range(50):
            mujoco.mj_step(self.model, self.data)

        return self.get_observation()

    def step(self, action_14dof):
        action_14dof = np.clip(action_14dof, -3.14, 3.14)
        for i, act_id in enumerate(self.actuator_ids):
            self.data.ctrl[act_id] = action_14dof[i]

        for _ in range(10):
            mujoco.mj_step(self.model, self.data)

        obs = self.get_observation()
        return obs

    def get_joint_positions(self):
        return np.array([self.data.qpos[i] for i in range(14)])

    def get_joint_torques(self):
        return np.array([self.data.actuator_force[i] for i in range(14)])

    def get_cube_pos(self):
        return np.array(self.data.xpos[self.cube_body_id])

    def get_observation(self):
        self.renderer_main.update_scene(self.data, camera=self.current_cam)
        img_main = self.renderer_main.render()

        self.renderer_wrist_l.update_scene(self.data, camera="left_wrist_cam")
        img_wrist_l = self.renderer_wrist_l.render()

        self.renderer_wrist_r.update_scene(self.data, camera="right_wrist_cam")
        img_wrist_r = self.renderer_wrist_r.render()

        return {
            "image_main": img_main,
            "image_wrist_l": img_wrist_l,
            "image_wrist_r": img_wrist_r,
            "qpos": self.get_joint_positions(),
            "torques": self.get_joint_torques(),
            "cube_pos": self.get_cube_pos(),
        }
