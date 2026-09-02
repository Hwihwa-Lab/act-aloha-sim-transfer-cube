# 🎨 Aloha 14-DOF LeRobot Simulator // UI/UX 디자인 규격서

본 문서는 `Aloha 14-DOF Bimanual Robot Simulator`의 **사이버펑크 다크 테마(Cyberpunk Robotics Lab) Bento Grid 레이아웃, 9단계 핸드오버 스테이지, 2분할 관절 카드 및 UI 컴포넌트 규격**을 정의합니다.

---

## 🎨 1. 컬러 팔레트 & 디자인 토큰 (Design Tokens)

| 토큰명 | 색상 코드 (HEX / BGR) | 용도 |
| :--- | :--- | :--- |
| `--bg-main` | `#0B0F19` / `(25, 15, 11)` | 콕핏 딥 다크 배경 |
| `--bg-card` | `#121928` / `(40, 25, 18)` | Bento Grid 카드 패널 배경 |
| `--accent-cyan` | `#00E5FF` / `(255, 220, 0)` | **LEFT ARM (7-DOF)** 관절 바 & 활성 스테이지 하이라이트 박스 |
| `--accent-orange`| `#FF9100` / `(50, 160, 255)` | **RIGHT ARM (7-DOF)** 관절 바 & 단축키 배지 |
| `--accent-green` | `#00E676` / `(120, 230, 0)` | **ACTION 배지**, `MODE: AUTO_PILOT` 상태 배지, Gripper OPEN |
| `--accent-red` | `#FF5252` / `(80, 80, 240)` | Gripper CLOSED (LOCKED) 상태 표시 |
| `--border-subtle`| `#283C55` / `(85, 60, 40)` | 뷰포트 및 Bento 카드 테두리 |

---

## 📐 2. 1280x760 콕핏 레이아웃 사양 (Layout Specification)

```
+----------------------------------------------------------------------------------------------------+
| Aloha 3D Bimanual Robot Simulator                                                                 |
| 14-DOF Dual-Arm MuJoCo Physical Simulation | Hwihwa Lab                                            |
+----------------------------------------------------------------------------------------------------+
| [3D VIEWPORT] (760x480)                               | [BIMANUAL TELEMETRY & AI]                  |
|  +-------------------------------------------------+  |                                            |
|  | [ ACTION: 4. LIFT TO CENTER ] (Neon Green Box)  |  |  [ MODE: AUTO_PILOT (Press 'M') ]          |
|  |                                                 |  |                                            |
|  |   [LEFT ARM] ===>     [RED CUBE]     <=== [RIGHT|  |  Simulation Engine                         |
|  |   (Silver Mesh)       (Table Center) (Silver)   |  |  MuJoCo 3D Physics (C++) | 60.0 FPS        |
|  |                                                 |  |                                            |
|  |                                                 |  |  Active Task: Bimanual Cube Transfer       |
|  |                                                 |  |  Step Counter: 131 Steps | Stage 4 / 9     |
|  +-------------------------------------------------+  |                                            |
|                                                       |  HANDOVER STAGES (Press 1-9):              |
| [LEFT ARM (7-DOF)]         [RIGHT ARM (7-DOF)]        |   [1] 1. LEFT ARM APPROACH                 |
|  Gripper: CLOSED (LOCKED)   Gripper: OPEN             |   [2] 2. DESCEND TO CUBE                   |
|  J1: +0.20  J2: -0.58       J1: -0.07  J2: -0.80      |   [3] 3. GRASP & LOCK CUBE                 |
|  [===    ]  [==     ]       [=      ]  [===    ]      |  [[4] 4. LIFT TO CENTER] (Cyan Box Outline)|
|  J3: +0.94  J4: -0.00       J3: +1.06  J4: -0.00      |   [5] 5. BIMANUAL ALIGNMENT                |
|  J5: +0.32  J6: +0.00       J5: +0.05  J6: -0.00      |   ... [9] 9. DEPOSIT & COMPLETE            |
|  (Cyan 6 Mini Bars)         (Orange 6 Mini Bars)      | ------------------------------------------ |
|                                                       |  KEYBOARD SHORTCUTS ([M], [1~9], [Space]..)|
+----------------------------------------------------------------------------------------------------+
```
