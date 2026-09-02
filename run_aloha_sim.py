"""Main Entrypoint for Aloha 14-DOF Bimanual Robot Simulator.

Features:
- Fixed Window Close (X-button cleanly terminates process)
- Direct Mouse Click & Hover Interactive Toolbar
- 9-Stage Handover Sequence with Keyboard Shortcuts [1~9]
- Auto-pilot / Manual Mode Toggle [M]
- Dual Wrist Cameras PiP (LeRobot Official Standard)
"""

import argparse
import time
import cv2
import numpy as np

from aloha_env import AlohaEnv
from policy_runner import ACTPolicyRunner
from telemetry_hud import TelemetryHUD

# Global mouse state
mouse_x, mouse_y = 0, 0
mouse_clicked_action = None

def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y, mouse_clicked_action
    mouse_x, mouse_y = x, y
    if event == cv2.EVENT_LBUTTONDOWN:
        hud = param
        mouse_clicked_action = hud.get_clicked_button(x, y)

def main():
    global mouse_clicked_action, mouse_x, mouse_y
    parser = argparse.ArgumentParser(description="Aloha 14-DOF Bimanual Simulator | Hwihwa Lab")
    parser.add_argument("--episodes", type=int, default=50, help="Number of benchmark episodes")
    parser.add_argument("--headless", action="store_true", help="Run without graphical window")
    args = parser.parse_args()

    print("=" * 65)
    print("  ALOHA 14-DOF BIMANUAL SIMULATOR")
    print("  Autonomous ACT Bimanual Control | Hwihwa Lab")
    print("=" * 65)
    print("[*] Initializing MuJoCo 14-DOF Physics Environment...")
    env = AlohaEnv(render_width=760, render_height=460)
    policy = ACTPolicyRunner(chunk_size=50, use_temporal_ensemble=True)
    hud = TelemetryHUD(width=1280, height=820)

    window_name = "Aloha 14-DOF Bimanual Simulator | Hwihwa Lab"
    if not args.headless:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 1280, 820)
        cv2.setMouseCallback(window_name, mouse_callback, param=hud)

    # Start in READY/PAUSED mode on launch (Wait for user click or SPACE)
    is_auto = True
    paused = True
    initial_ready = True
    current_cam = "top_cam"
    running = True

    # Accurate 1-second interval FPS counter
    fps_display = 60.0
    frame_count = 0
    last_fps_time = time.perf_counter()

    for ep in range(1, args.episodes + 1):
        if not running:
            break

        obs = env.reset(randomize_cube=False)
        policy.reset()
        print(f"\n>>> [Episode {ep}] Ready. Click [START] or press SPACE to run.")

        step = 0
        max_steps = 380

        while step < max_steps and running:
            loop_start = time.perf_counter()
            triggered_reset = False

            if not paused and is_auto:
                action = policy.predict_action(obs)
                obs = env.step(action)
                step += 1
            else:
                obs = env.get_observation()

            # Measure accurate 1-second FPS
            frame_count += 1
            now = time.perf_counter()
            elapsed = now - last_fps_time
            if elapsed >= 0.5:
                fps_display = frame_count / elapsed
                frame_count = 0
                last_fps_time = now

            # Render HUD Frame with Mouse Position
            stage_idx = policy.get_stage_info(step)

            if not args.headless:
                try:
                    frame = hud.render(
                        obs, 
                        stage_idx=stage_idx, 
                        step=step, 
                        total_steps=max_steps, 
                        fps=fps_display, 
                        is_auto=is_auto, 
                        paused=paused, 
                        initial_ready=initial_ready,
                        cam_name=current_cam,
                        mouse_pos=(mouse_x, mouse_y)
                    )
                    cv2.imshow(window_name, frame)
                except Exception:
                    running = False
                    break

            # 2. Handle Mouse Button Clicks
            if mouse_clicked_action is not None:
                action_btn = mouse_clicked_action
                mouse_clicked_action = None

                if action_btn == "toggle_play":
                    initial_ready = False
                    paused = not paused
                    print(f"[*] Simulation {'PAUSED' if paused else 'RUNNING'} via Mouse Click")
                elif action_btn == "reset":
                    print("[*] Environment reset via Mouse Click.")
                    triggered_reset = True
                elif action_btn == "toggle_mode":
                    is_auto = not is_auto
                    print(f"[*] Mode changed: {'AUTO_PILOT' if is_auto else 'MANUAL_TELEOP'} via Mouse Click")
                elif action_btn == "switch_cam":
                    cam_cycle = ["top_cam", "iso_cam", "front_cam"]
                    curr_idx = cam_cycle.index(current_cam) if current_cam in cam_cycle else 0
                    current_cam = cam_cycle[(curr_idx + 1) % len(cam_cycle)]
                    env.set_camera(current_cam)
                    print(f"[*] Camera switched to: {current_cam} via Mouse Click")
                elif action_btn == "quit":
                    print("\n[!] Simulation terminated by user via Mouse Click.")
                    running = False
                    break

            # 3. Handle Window Close & Keyboard Events
            if not args.headless:
                key = cv2.waitKey(10) & 0xFF

                # Check if user clicked the X window button
                try:
                    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                        print("\n[!] Window closed by user (X button). Terminating simulator cleanly.")
                        running = False
                        break
                except Exception:
                    running = False
                    break

                if key in [ord('q'), ord('Q'), 27]:
                    print("\n[!] Simulation terminated by user.")
                    running = False
                    break
                elif key == ord(' '):
                    initial_ready = False
                    paused = not paused
                    print(f"[*] Simulation {'PAUSED' if paused else 'RUNNING'}")
                elif key in [ord('m'), ord('M')]:
                    is_auto = not is_auto
                    print(f"[*] Mode changed: {'AUTO_PILOT' if is_auto else 'MANUAL_TELEOP'}")
                elif key in [ord('c'), ord('C')]:
                    cam_cycle = ["top_cam", "iso_cam", "front_cam"]
                    curr_idx = cam_cycle.index(current_cam) if current_cam in cam_cycle else 0
                    current_cam = cam_cycle[(curr_idx + 1) % len(cam_cycle)]
                    env.set_camera(current_cam)
                    print(f"[*] Camera switched to: {current_cam} via Key [C]")
                elif key in [ord('r'), ord('R')]:
                    print("[*] Environment reset.")
                    triggered_reset = True
                elif ord('1') <= key <= ord('9'):
                    target_stage = key - ord('1')
                    step = target_stage * 40
                    policy.step_idx = step
                    print(f"[*] Jumped to Stage {target_stage + 1}")

            if triggered_reset or not running:
                break

        if not running:
            break
        print(f">>> [Episode {ep}] Cycle Complete.")

    try:
        cv2.destroyAllWindows()
    except Exception:
        pass

if __name__ == "__main__":
    main()
