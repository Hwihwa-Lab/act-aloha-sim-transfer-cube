# 📐 Aloha 14-DOF LeRobot 데이터 스키마 및 규격서

AI가 환경을 조작하거나 관절 텔레메트리, 벤치마크 지표, ACT 정책 입출력 데이터를 다룰 때 반드시 준수해야 하는 엄격한 데이터 규격입니다.

---

## 1. Aloha 14-DOF MuJoCo 환경 규격 (Environment Specification)

### State Space (관측 벡터 & 이미지)
* **Joint Positions (`qpos`, 14차원 float64)**:
  * `qpos[0:7]`: **Left Arm 7-DOF** (`L_Waist, L_Shoulder, L_Elbow, L_Roll, L_Pitch, L_WRoll, L_Grip`)
  * `qpos[7:14]`: **Right Arm 7-DOF** (`R_Waist, R_Shoulder, R_Elbow, R_Roll, R_Pitch, R_WRoll, R_Grip`)
* **Joint Torques (`torques`, 14차원 float64)**:
  * 14개 액추에이터의 실시간 피드백 토크/힘 (`N·m`)
* **Cube 3D Position (`cube_pos`, 3차원 float64)**:
  * `[x, y, z]` 테이블 좌표계 기준 큐브 중심 위치 (Grasp 높이: `z > 0.42m`)
* **Multi-Camera Visual Observations**:
  * `image_top`: 탑뷰 메인 카메라 (`640x480x3 RGB`)
  * `image_wrist_l`: 좌측 손목 카메라 (`200x160x3 RGB`)
  * `image_wrist_r`: 우측 손목 카메라 (`200x160x3 RGB`)

### Action Space (14차원 연속 벡터)
* `action[0:14]`: 14개 관절 목표 각도 (`rad`, 범위: `[-3.14, 3.14]`, 그리퍼 범위: `[0.0, 0.035] m`)

### Step Return `info` Dictionary:
```python
{
    "phase": str,         # "PHASE 0: APPROACH", "PHASE 1: GRASP", "PHASE 2: ALIGN", "PHASE 3: TRANSFER", "PHASE 4: PLACED"
    "success": bool,      # 태스크 성공 여부 (Cube transferred and placed stably)
    "cube_height": float, # 큐브 z축 높이 (m)
    "cube_pos": np.ndarray # 3D Cartesian coordinates [x, y, z]
}
```

---

## 2. ACT Policy 입출력 스키마 (Chunking & Ensembling)

```python
{
    "input": {
        "qpos": np.ndarray,      # (14,) 현재 관절 각도
        "cube_pos": np.ndarray   # (3,) 큐브 위치
    },
    "chunk_output": np.ndarray,  # (50, 14) 50-Horizon Action Chunk
    "ensembled_action": np.ndarray # (14,) Temporal Ensembling 가중합 단일 액션
}
```

---

## 3. 정량 벤치마크 지표 스키마 (Metrics Summary)

```json
{
  "total_episodes": 10,
  "successful_episodes": 10,
  "success_rate": 100.0,
  "time_to_success": 5.42,
  "step_to_success": 280,
  "avg_jerk": 1.245,
  "milestones": {
    "PHASE 1: LEFT ARM GRASPED": true,
    "PHASE 2: BIMANUAL ALIGNMENT": true,
    "PHASE 3: HANDOVER TO RIGHT ARM": true,
    "PHASE 4: PLACED IN TARGET": true
  }
}
```
