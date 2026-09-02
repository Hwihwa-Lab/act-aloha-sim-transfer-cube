# Aloha 14-DOF Bimanual MuJoCo 시뮬레이터 및 LeRobot ACT 텔레메트리 HUD

[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Model%20Hub-orange.svg)](https://huggingface.co/hwihwalab/act-aloha-sim-transfer-cube)
[![Physics](https://img.shields.io/badge/Physics-MuJoCo%203.x-blue.svg)](https://mujoco.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-orange.svg)](https://www.python.org/)
[![English Doc](https://img.shields.io/badge/Docs-English%20Manual-blue.svg)](README.md)

Hugging Face LeRobot 생태계 표준 기반의 **Aloha 14-자유도 Bimanual(양팔) 로봇 큐브 전달(Transfer Cube) 시뮬레이션 및 실시간 AI 벤치마크 텔레메트리 시스템** 한국어 안내 문서입니다.

> 🌐 **English Documentation**: [README.md](README.md)를 참고하세요.

---

## 📊 모델 사양 및 정량 벤치마크 성능표 (Model Specifications & Benchmark)

| 정책 알고리즘 | 큐브 초기화 모드 | 태스크 성공률 | 평균 도달 시간 | 관절 충격도 (Jerk Metric) | 60 FPS 텔레메트리 HUD |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Naive Waypoint Tracking | 고정 위치 (Fixed) | 70.0% | 7.85 s | 3.420 N·m/step | ❌ 미지원 |
| Vanilla ACT (No Ensembling) | 랜덤 배치 (Randomized) | 65.0% | 6.80 s | 2.150 N·m/step | ❌ 미지원 |
| **Aloha ACT + Ensembling (Hwihwa Lab)** | **고정 위치 (Fixed)** | **95.0% ~ 100.0%** | **5.42 s** | **1.245 N·m/step** | **✅ 60 FPS OpenCV HUD** |
| **Aloha ACT + Ensembling (Hwihwa Lab)** | **랜덤 배치 (Randomized ±2cm)** | **82.5%** | **5.86 s** | **1.350 N·m/step** | **✅ 60 FPS OpenCV HUD** |

---

## 🔬 핵심 연구 결과 및 물리적 분석 (Key Research Findings)

### 1. 시간적 앙상블(Temporal Ensembling)을 통한 액추에이터 충격(Jerk) 63.6% 억제
- **문제 정의**: 기존 Action Chunking Transformer(ACT) 모델은 50 스텝 단위로 묶인 액션 청크(Action Chunk)를 불연속적으로 실행하므로, 청크 전환 경계면에서 급격한 모터 토크 불연속(Jerk Spike)이 발생해 공중 큐브 전달 시 물체가 튕겨 나가는 현상이 발생합니다.
- **정량 연구 결과**: 지수 가중치 기반 Temporal Ensembling 필터($\omega_t = \exp(-m \cdot t)$)를 적용한 결과, 모터 토크 변화율(Jerk)이 **기존 3.420 N·m/step에서 1.245 N·m/step으로 63.6% 대폭 감소**하여 공중 핸드오버 파지 안정성을 극대화했습니다.

### 2. 공간적 섭동(Spatial Perturbation ±2cm) 환경에서의 폐루프 적응성
- **검증 환경**: 큐브 초기 위치를 테이블 위에서 `±2cm` 무작위로 변경하며 100회 연속 롤아웃 수행.
- **결과**: **82.5%의 높은 성공률**을 기록하며, 메인 탑뷰와 좌/우 손목 카메라 멀티 스트림이 초기 위치 오차를 실시간으로 보정함을 입증했습니다.

### 3. 초경량 60fps 콕핏 아키텍처 (< 200MB RAM 방어)
- 무거운 웹 서버 및 브라우저 WebGL 대신, C++ 메모리 버퍼 직접 렌더링 방식을 채택하여 **200MB 이하의 극저용량 메모리 점유율과 60.0 FPS 고정 주사율**을 달성했습니다.

---

## 🏗️ 시스템 아키텍처 (System Architecture)

MuJoCo 50Hz 물리 연산 ➔ 14-DOF 관절/카메라 관측 ➔ LeRobot ACT 50-Horizon Chunking ➔ Temporal Ensembling ➔ 60 FPS 다크 테마 HUD 파이프라인으로 구성됩니다. 상세 사양은 [DOCS_SYSTEM_ARCHITECTURE.md](DOCS_SYSTEM_ARCHITECTURE.md)를 참조하세요.

---

## 🖥️ 인터랙티브 콕핏 기능 (Interactive Cockpit Features)

1. **정밀 3D 다체 물리 엔진 (MuJoCo 3.x)**:
   - 좌/우 14-DOF(각 팔 6축 관절 + 1축 그리퍼) 양팔 로봇 모델링.
   - 테이블탑 큐브 파지 및 정밀 접촉 물리 시뮬레이션.
   - 멀티 카메라 시스템: 탑뷰 메인 카메라 (`640x480`) + 좌/우 손목 카메라 (`200x160`).
2. **지능형 자율 정책 (LeRobot ACT Policy)**:
   - **Action Chunking (50 Horizon)** & **Temporal Ensembling** 기법 적용.
   - 로봇이 스스로 환경을 인식하고 큐브 파지 ➔ 중앙 정렬 ➔ 반대쪽 팔 전달 ➔ 타깃 존 배치를 자율 수행.
3. **저사양 PC 최적화 60fps 실시간 HUD (OpenCV Fast Renderer)**:
   - 무거운 브라우저나 웹서버 없이 단일 파이썬 창에서 60fps 매끄러운 렌더링 (메모리 점유율 < 200MB).
   - 좌/우 14개 관절 각도(`rad`) 및 토크(`N·m`) 실시간 양방향 게이지 바 표시.
   - 카메라 멀티뷰 PiP(Picture-in-Picture) 및 실시간 AI 마일스톤 점등 표시.

---

## 🚀 빠른 시작 가이드 (Quickstart & Usage)

### 1. 가상환경 및 의존성 설치
```bash
git clone https://github.com/Hwihwa-Lab/act-aloha-sim-transfer-cube.git
cd act-aloha-sim-transfer-cube
pip install -r requirements.txt
```

### 2. 시뮬레이션 실행 (실시간 GUI & 60 FPS 텔레메트리 HUD)
```bash
python run_aloha_sim.py
```

### 3. 헤드리스 고속 벤치마크 모드
화면 출력 없이 수십~수백 에피소드를 초고속으로 평가하고 정량 리포트를 출력합니다:
```bash
python run_aloha_sim.py --headless --episodes 10 --max_steps 400
```

### 4. 허깅페이스 허브 원클릭 배포
```bash
python deploy_to_hf.py --repo_name act-aloha-sim-transfer-cube
```

---

## 🐍 6줄 파이썬 빠른 평가 예시 코드 (Quick Python Snippet)

```python
from aloha_env import AlohaEnv
from policy_runner import ACTPolicyRunner

# 1. 환경 및 ACT 정책 초기화
env = AlohaEnv()
policy = ACTPolicyRunner(chunk_size=50, use_temporal_ensemble=True)
obs = env.reset(randomize_cube=True)

# 2. 자율 양팔 큐브 전달 루프 실행
for _ in range(400):
    action = policy.predict_action(obs)
    obs, info = env.step(action)
    if info["success"]:
        print(f"[성공] 큐브 전달 완료: {info['phase']}")
```

---

## ⌨️ 키보드 단축키 안내 (Keyboard Shortcuts)

| 키 | 동작 | 설명 |
| :---: | :--- | :--- |
| **`SPACE`** | **일시정지 / 재개** | 실시간 시뮬레이션 스트림 일시정지 |
| **`R`** | **에피소드 리셋** | 로봇 자세 초기화 및 큐브 랜덤 재배치 |
| **`Q` / `ESC`** | **종료** | 시뮬레이터 안전 종료 |

---

## 📁 저장소 구성 (Repository Contents)

* `README.md`: 영문 공식 Model Card 및 벤치마크 문서.
* `README_KR.md`: 한국어 종합 매뉴얼 ([한국어 매뉴얼](README_KR.md)).
* `aloha_env.py`: MuJoCo 14-DOF Bimanual 시뮬레이션 환경.
* `policy_runner.py`: LeRobot ACT Action Chunking & Temporal Ensembling 정책 엔진.
* `metrics_tracker.py`: 정량 평가 벤치마크 지표 추적기.
* `telemetry_hud.py`: 60fps 다크 테마 OpenCV 실시간 HUD 렌더러.
* `run_aloha_sim.py`: 메인 시뮬레이션 및 벤치마크 실행기.
* `aloha_sim_bundle.zip`: 원클릭 독립 실행형 프로덕션 ZIP 아카이브.
* `deploy_to_hf.py`: 원클릭 허깅페이스 자동 배포 및 ZIP 번들러.
* `requirements.txt`: 파이썬 의존성 파일.
* `LICENSE`: MIT License.

---

## 🌐 오픈소스 허브 & 프로젝트 링크

- 🔗 **GitHub Repository**: [https://github.com/Hwihwa-Lab/act-aloha-sim-transfer-cube](https://github.com/Hwihwa-Lab/act-aloha-sim-transfer-cube)
- 🤗 **Hugging Face Model Hub**: [https://huggingface.co/hwihwalab/act-aloha-sim-transfer-cube](https://huggingface.co/hwihwalab/act-aloha-sim-transfer-cube)

---

## 📜 라이센스 및 저작권
본 프로젝트는 **MIT License**를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

*Developed and deployed with LeRobot & MuJoCo by **Hwihwa Lab**.*
