"""High-Fidelity Cyberpunk Telemetry HUD with LeRobot Multi-Camera PiP & Clean Visual Hierarchy.

Features:
- Minimalist LED Status Indicator (● READY, ● RUNNING, ● PAUSED) - No False Affordance!
- Elegant Mode Header Banner (Clickable & Informative)
- Main Bimanual Viewport with Neon Action Badge
- Viewport Camera Mode Tag: [CAM: TOP VIEW], [CAM: 3D ISOMETRIC], [CAM: FRONT ACTION]
- Dual Wrist Cameras PiP (Left Wrist & Right Wrist)
- Bottom Bento Grid: Left Arm (7-DOF) + Right Arm (7-DOF)
- Perfectly Balanced 5-Button Toolbar:
  [ START / PAUSE ] [ RESET CUBE ] [ AUTO-PILOT ] [ SWITCH CAM ] [ QUIT ]
"""

import cv2
import numpy as np
from aloha_env import STAGES_9

class TelemetryHUD:
    def __init__(self, width=1280, height=820):
        self.width = width
        self.height = height

        # Interactive Buttons Definition: (id, label, x1, y1, x2, y2, bg, accent)
        btn_y1 = 745
        btn_y2 = 795
        self.buttons = [
            {"id": "toggle_play", "label": "START", "label_alt": "PAUSE", "x1": 25, "y1": btn_y1, "x2": 215, "y2": btn_y2, "accent": (0, 230, 100), "bg": (20, 45, 30)},
            {"id": "reset", "label": "RESET CUBE", "label_alt": "RESET CUBE", "x1": 230, "y1": btn_y1, "x2": 420, "y2": btn_y2, "accent": (240, 160, 40), "bg": (35, 35, 45)},
            {"id": "toggle_mode", "label": "AUTO-PILOT", "label_alt": "MANUAL", "x1": 435, "y1": btn_y1, "x2": 625, "y2": btn_y2, "accent": (0, 220, 255), "bg": (20, 40, 50)},
            {"id": "switch_cam", "label": "SWITCH CAM", "label_alt": "SWITCH CAM", "x1": 640, "y1": btn_y1, "x2": 830, "y2": btn_y2, "accent": (240, 200, 60), "bg": (30, 40, 50)},
            {"id": "quit", "label": "QUIT", "label_alt": "QUIT", "x1": 845, "y1": btn_y1, "x2": 985, "y2": btn_y2, "accent": (80, 80, 240), "bg": (45, 25, 25)},
        ]

        # Mode banner clickable zone on right panel
        self.mode_banner = {"x1": 810, "y1": 105, "x2": self.width - 25, "y2": 140}

    def get_clicked_button(self, mouse_x, mouse_y):
        for btn in self.buttons:
            if btn["x1"] <= mouse_x <= btn["x2"] and btn["y1"] <= mouse_y <= btn["y2"]:
                return btn["id"]
        # Also allow clicking the mode banner
        if self.mode_banner["x1"] <= mouse_x <= self.mode_banner["x2"] and self.mode_banner["y1"] <= mouse_y <= self.mode_banner["y2"]:
            return "toggle_mode"
        return None

    def render(self, obs, stage_idx, step, total_steps=360, fps=60.0, is_auto=True, paused=False, initial_ready=False, cam_name="top_cam", mouse_pos=(0, 0)):
        canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        canvas[:] = (11, 15, 25)  # Dark futuristic background

        # 1. Top Header Bar (Hwihwa Lab Exact Standard)
        cv2.putText(canvas, "ALOHA 14-DOF BIMANUAL SIMULATOR", (25, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.82, (255, 255, 255), 2)
        cv2.putText(canvas, "Autonomous ACT Bimanual Control | Hwihwa Lab", (25, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (140, 160, 180), 1)

        # Minimalist LED Status Indicator (No false button appearance!)
        if initial_ready:
            st_text, led_color = "READY", (0, 220, 255)
        elif paused:
            st_text, led_color = "PAUSED", (255, 180, 40)
        else:
            st_text, led_color = "RUNNING", (0, 240, 100)

        # Draw glowing LED dot & text
        cv2.circle(canvas, (self.width - 320, 41), 5, led_color, -1)
        cv2.putText(canvas, st_text, (self.width - 305, 46), cv2.FONT_HERSHEY_SIMPLEX, 0.52, led_color, 2)

        # FPS Badge
        cv2.putText(canvas, f"FPS: {fps:.1f} (MuJoCo)", (self.width - 190, 46), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (80, 220, 120), 2)

        # 2. Main Viewport (760x460)
        vp_x1, vp_y1, vp_x2, vp_y2 = 25, 80, 785, 540
        img_main = obs["image_main"]
        img_main_bgr = cv2.cvtColor(img_main, cv2.COLOR_RGB2BGR)
        main_view = cv2.resize(img_main_bgr, (vp_x2 - vp_x1, vp_y2 - vp_y1))
        canvas[vp_y1:vp_y2, vp_x1:vp_x2] = main_view
        cv2.rectangle(canvas, (vp_x1, vp_y1), (vp_x2, vp_y2), (45, 60, 80), 2)

        # Action Tag & Camera Tag with Semi-Transparent Glassmorphism
        # 1) Action Tag (Left)
        current_action_label = STAGES_9[stage_idx]
        badge_text = f"ACTION: {current_action_label}"
        text_w = cv2.getTextSize(badge_text, cv2.FONT_HERSHEY_SIMPLEX, 0.46, 1)[0][0]
        tag_w = text_w + 30
        tag_h = 28
        ax1, ay1, ax2, ay2 = vp_x1 + 15, vp_y1 + 15, vp_x1 + 15 + tag_w, vp_y1 + 15 + tag_h

        # Alpha Blend Background (60% Dark Glass)
        overlay_action = canvas[ay1:ay2, ax1:ax2].copy()
        cv2.rectangle(overlay_action, (0, 0), (tag_w, tag_h), (12, 18, 26), -1)
        cv2.addWeighted(overlay_action, 0.65, canvas[ay1:ay2, ax1:ax2], 0.35, 0, canvas[ay1:ay2, ax1:ax2])
        
        # Subtle Glass Border & Left Neon Accent Indicator
        cv2.rectangle(canvas, (ax1, ay1), (ax2, ay2), (40, 65, 75), 1)
        cv2.rectangle(canvas, (ax1, ay1), (ax1 + 4, ay2), (0, 240, 150), -1)
        cv2.putText(canvas, badge_text, (ax1 + 14, ay1 + 19), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (0, 255, 170), 1)

        # 2) Camera Tag (Right)
        if "iso" in cam_name:
            cam_desc = "CAM: 3D ISOMETRIC"
        elif "front" in cam_name:
            cam_desc = "CAM: FRONT ACTION"
        else:
            cam_desc = "CAM: TOP VIEW"
        
        c_text_w = cv2.getTextSize(cam_desc, cv2.FONT_HERSHEY_SIMPLEX, 0.44, 1)[0][0]
        c_tag_w = c_text_w + 24
        c_tag_h = 28
        cx1, cy1, cx2, cy2 = vp_x2 - c_tag_w - 15, vp_y1 + 15, vp_x2 - 15, vp_y1 + 15 + c_tag_h

        # Alpha Blend Background (60% Dark Glass)
        overlay_cam = canvas[cy1:cy2, cx1:cx2].copy()
        cv2.rectangle(overlay_cam, (0, 0), (c_tag_w, c_tag_h), (12, 18, 26), -1)
        cv2.addWeighted(overlay_cam, 0.65, canvas[cy1:cy2, cx1:cx2], 0.35, 0, canvas[cy1:cy2, cx1:cx2])

        # Subtle Glass Border & Cyan Accent Text
        cv2.rectangle(canvas, (cx1, cy1), (cx2, cy2), (35, 60, 80), 1)
        cv2.putText(canvas, cam_desc, (cx1 + 12, cy1 + 19), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 220, 255), 1)

        # Multi-Cam Wrist PiPs
        if "image_wrist_l" in obs and "image_wrist_r" in obs:
            img_wl = cv2.cvtColor(obs["image_wrist_l"], cv2.COLOR_RGB2BGR)
            img_wr = cv2.cvtColor(obs["image_wrist_r"], cv2.COLOR_RGB2BGR)
            wl_pip = cv2.resize(img_wl, (120, 85))
            wr_pip = cv2.resize(img_wr, (120, 85))

            canvas[vp_y2 - 95:vp_y2 - 10, vp_x1 + 15:vp_x1 + 135] = wl_pip
            cv2.rectangle(canvas, (vp_x1 + 15, vp_y2 - 95), (vp_x1 + 135, vp_y2 - 10), (0, 220, 255), 1)
            cv2.putText(canvas, "L-Wrist", (vp_x1 + 20, vp_y2 - 78), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)

            canvas[vp_y2 - 95:vp_y2 - 10, vp_x2 - 135:vp_x2 - 15] = wr_pip
            cv2.rectangle(canvas, (vp_x2 - 135, vp_y2 - 95), (vp_x2 - 15, vp_y2 - 10), (255, 160, 50), 1)
            cv2.putText(canvas, "R-Wrist", (vp_x2 - 130, vp_y2 - 78), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)

        # 3. Bottom Bento Grid: Left Arm & Right Arm 7-DOF Cards
        card_y1, card_y2 = 555, 725
        left_x1, left_x2 = 25, 395
        right_x1, right_x2 = 415, 785

        qpos = obs["qpos"]
        l_grip = qpos[6]
        r_grip = qpos[13]

        l_grip_str = "CLOSED (LOCKED)" if l_grip < 0.02 else "OPEN"
        l_grip_col = (50, 80, 240) if l_grip < 0.02 else (80, 230, 120)
        r_grip_str = "CLOSED (LOCKED)" if r_grip < 0.02 else "OPEN"
        r_grip_col = (50, 80, 240) if r_grip < 0.02 else (80, 230, 120)

        # Left Arm Card
        cv2.rectangle(canvas, (left_x1, card_y1), (left_x2, card_y2), (18, 25, 40), -1)
        cv2.rectangle(canvas, (left_x1, card_y1), (left_x2, card_y2), (40, 60, 85), 1)
        cv2.putText(canvas, "LEFT ARM (7-DOF)", (left_x1 + 15, card_y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 255), 2)
        cv2.putText(canvas, f"Gripper: {l_grip_str}", (left_x1 + 180, card_y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.42, l_grip_col, 1)

        for i in range(6):
            col_idx = i % 3
            row_idx = i // 3
            bx = left_x1 + 15 + col_idx * 115
            by = card_y1 + 60 + row_idx * 55
            val = qpos[i]
            cv2.putText(canvas, f"J{i+1}:{val:+0.2f}", (bx, by - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 240), 1)
            cv2.rectangle(canvas, (bx, by), (bx + 95, by + 8), (35, 45, 60), -1)
            fill_w = int(np.clip((val + 1.5) / 3.0 * 95, 0, 95))
            cv2.rectangle(canvas, (bx, by), (bx + fill_w, by + 8), (0, 220, 255), -1)

        # Right Arm Card
        cv2.rectangle(canvas, (right_x1, card_y1), (right_x2, card_y2), (18, 25, 40), -1)
        cv2.rectangle(canvas, (right_x1, card_y1), (right_x2, card_y2), (40, 60, 85), 1)
        cv2.putText(canvas, "RIGHT ARM (7-DOF)", (right_x1 + 15, card_y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 160, 50), 2)
        cv2.putText(canvas, f"Gripper: {r_grip_str}", (right_x1 + 180, card_y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.42, r_grip_col, 1)

        for i in range(6):
            col_idx = i % 3
            row_idx = i // 3
            bx = right_x1 + 15 + col_idx * 115
            by = card_y1 + 60 + row_idx * 55
            val = qpos[7 + i]
            cv2.putText(canvas, f"J{i+1}:{val:+0.2f}", (bx, by - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 240), 1)
            cv2.rectangle(canvas, (bx, by), (bx + 95, by + 8), (35, 45, 60), -1)
            fill_w = int(np.clip((val + 1.5) / 3.0 * 95, 0, 95))
            cv2.rectangle(canvas, (bx, by), (bx + fill_w, by + 8), (255, 160, 50), -1)

        # 4. Right Side Panel
        p_x = 810
        cv2.putText(canvas, "BIMANUAL TELEMETRY & AI", (p_x, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 220, 240), 2)

        # Mode Header Banner (Informative, Clickable, and Perfectly Center-Aligned)
        mx, my = mouse_pos
        is_mode_hovered = (self.mode_banner["x1"] <= mx <= self.mode_banner["x2"] and self.mode_banner["y1"] <= my <= self.mode_banner["y2"])
        mode_str = "MODE: AUTO_PILOT [Click/M]" if is_auto else "MODE: MANUAL TELEOP [Click/M]"
        mode_accent = (0, 220, 120) if is_auto else (255, 160, 40)
        mode_bg = (20, 38, 30) if is_auto else (38, 28, 20)

        bx1, by1, bx2, by2 = self.mode_banner["x1"], self.mode_banner["y1"], self.mode_banner["x2"], self.mode_banner["y2"]
        cv2.rectangle(canvas, (bx1, by1), (bx2, by2), mode_bg, -1)
        cv2.rectangle(canvas, (bx1, by1), (bx2, by2), mode_accent, 2 if is_mode_hovered else 1)

        # Perfect horizontal and vertical center alignment
        mode_font_scale = 0.46
        mode_thickness = 2 if is_mode_hovered else 1
        text_size = cv2.getTextSize(mode_str, cv2.FONT_HERSHEY_SIMPLEX, mode_font_scale, mode_thickness)[0]
        text_x = bx1 + (bx2 - bx1 - text_size[0]) // 2
        text_y = by1 + (by2 - by1 + text_size[1]) // 2
        cv2.putText(canvas, mode_str, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, mode_font_scale, mode_accent, mode_thickness)

        info_y = 165
        cv2.putText(canvas, "Simulation Engine", (p_x, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (140, 150, 160), 1)
        cv2.putText(canvas, f"MuJoCo 3D Physics (C++) | {fps:.1f} FPS", (p_x, info_y + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (240, 240, 240), 1)

        info_y += 38
        cv2.putText(canvas, "Actuator & Benchmark", (p_x, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (140, 150, 160), 1)
        cv2.putText(canvas, "14-DOF Continuous | Jerk: 1.25 N*m", (p_x, info_y + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 220, 255), 1)

        info_y += 38
        cv2.putText(canvas, "Active Task", (p_x, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (140, 150, 160), 1)
        cv2.putText(canvas, "Bimanual Cube Transfer & Handover", (p_x, info_y + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (240, 240, 240), 1)

        info_y += 38
        cv2.putText(canvas, "Step Counter & Progress", (p_x, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (140, 150, 160), 1)
        cv2.putText(canvas, f"{step} Steps | Stage {stage_idx + 1} / 9", (p_x, info_y + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 240, 170), 1)

        # Handover Stages (1 ~ 9)
        stage_y_start = 350
        cv2.putText(canvas, "HANDOVER STAGES (Press 1-9):", (p_x, stage_y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 210, 220), 2)

        for i in range(9):
            sy = stage_y_start + 22 + i * 21
            is_active = (i == stage_idx)
            s_name = STAGES_9[i]

            if is_active:
                cv2.rectangle(canvas, (p_x, sy - 14), (self.width - 25, sy + 5), (20, 35, 45), -1)
                cv2.rectangle(canvas, (p_x, sy - 14), (self.width - 25, sy + 5), (0, 220, 255), 1)
                text_col = (0, 240, 255)
            else:
                text_col = (110, 130, 150)

            cv2.putText(canvas, f"[{i+1}] {s_name}", (p_x + 10, sy), cv2.FONT_HERSHEY_SIMPLEX, 0.42, text_col, 1)

        # Keyboard Shortcuts
        ks_y = 575
        cv2.line(canvas, (p_x, ks_y - 10), (self.width - 25, ks_y - 10), (40, 50, 65), 1)
        cv2.putText(canvas, "KEYBOARD SHORTCUTS", (p_x, ks_y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 210, 220), 2)
        
        shortcuts = [
            ("[M]", "Toggle Auto-Pilot / Manual Teleop"),
            ("[1~9]", "Jump to specific handover stage"),
            ("[Space]", "Pause / Resume 3D Physics"),
            ("[R]", "Reset environment (Re-drop cube)"),
            ("[C]", "Cycle Camera (Top / 3D / Front)"),
            ("[Q / ESC]", "Exit simulation")
        ]
        
        for idx, (k_btn, k_desc) in enumerate(shortcuts):
            sy = ks_y + 32 + idx * 20
            cv2.putText(canvas, k_btn, (p_x, sy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 200, 50), 1)
            cv2.putText(canvas, k_desc, (p_x + 65, sy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (160, 175, 190), 1)

        # 5. Interactive Control Toolbar (Bottom Section: 735 to 810)
        cv2.rectangle(canvas, (0, 735), (self.width, self.height), (16, 22, 32), -1)
        cv2.line(canvas, (0, 735), (self.width, 735), (40, 55, 75), 1)

        for btn in self.buttons:
            is_hovered = (btn["x1"] <= mx <= btn["x2"] and btn["y1"] <= my <= btn["y2"])
            
            if btn["id"] == "toggle_play":
                label = "START" if (paused or initial_ready) else "PAUSE"
                accent = (0, 255, 120) if (paused or initial_ready) else (255, 180, 40)
            elif btn["id"] == "toggle_mode":
                label = "AUTO-PILOT" if is_auto else "MANUAL"
                accent = (0, 220, 255) if is_auto else (255, 140, 60)
            else:
                label = btn["label"]
                accent = btn["accent"]

            bg_color = (35, 48, 65) if is_hovered else btn["bg"]
            border_thick = 2 if is_hovered else 1

            cv2.rectangle(canvas, (btn["x1"], btn["y1"]), (btn["x2"], btn["y2"]), bg_color, -1)
            cv2.rectangle(canvas, (btn["x1"], btn["y1"]), (btn["x2"], btn["y2"]), accent, border_thick)

            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.48, 1)[0]
            text_x = btn["x1"] + (btn["x2"] - btn["x1"] - text_size[0]) // 2
            text_y = btn["y1"] + (btn["y2"] - btn["y1"] + text_size[1]) // 2
            cv2.putText(canvas, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255) if is_hovered else accent, 1 if not is_hovered else 2)

        return canvas
