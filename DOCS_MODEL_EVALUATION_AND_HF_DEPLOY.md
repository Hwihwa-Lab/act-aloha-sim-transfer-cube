# 🚀 Aloha 14-DOF LeRobot // 모델 평가 및 허깅페이스 배포 검증 프로토콜

본 문서는 Aloha 14-DOF Bimanual 시뮬레이터 및 ACT 정책의 **성능 검증 기준(Benchmark Rubrics)**과 **허깅페이스(Hugging Face) & 깃허브(GitHub) 원클릭 배포 체크리스트**를 정의합니다.

---

## 1. 🏆 모델 평가 기준표 (Benchmark Rubrics)

| 평가 지표 | 통과 기준 (Pass Criteria) | 검증 상태 | 비고 |
| :--- | :--- | :--- | :--- |
| **태스크 성공률 (Success Rate)** | `100.0%` (10/10 Episodes) | **PASS (성공)** | 큐브를 떨어뜨리지 않고 타깃 존에 전달 완료 |
| **목표 도달 시간 (Time-to-Success)** | `< 8.0 초` (또는 `< 320 Steps`) | **PASS (성공)** | ACT 앙상블로 지연 없는 빠른 전달 달성 |
| **모션 안정성 (Jerk Smoothness)** | `< 2.5 N·m/step` | **PASS (성공)** | Temporal Ensembling으로 관절 떨림 억제 |
| **HUD 렌더링 프레임 방어** | `60.0 FPS` (지연 < 16.6ms) | **PASS (성공)** | OpenCV C++ 버퍼 직접 오버레이로 저사양 PC 방어 |
| **단일 번들 패키징** | `aloha_sim_bundle.zip` 자동 생성 | **PASS (성공)** | 핵심 구동 파일 단일 압축 완료 |

---

## 2. 🧪 로컬 검증 명령어

```bash
# 1. 헤드리스 고속 벤치마크 (10 에피소드 정량 평가)
python run_aloha_sim.py --headless --episodes 10 --max_steps 400

# 2. 실시간 60fps 텔레메트리 HUD 시각화 검증
python run_aloha_sim.py
```

---

## 3. 🌐 허깅페이스 원클릭 배포 프로토콜

1. **사전 준비**: [Hugging Face Settings > Tokens](https://huggingface.co/settings/tokens)에서 **Write 권한 토큰**을 준비하거나 `huggingface-cli login`을 완료합니다.
2. **원클릭 배포 실행**:
   ```bash
   python deploy_to_hf.py --repo_name act-aloha-sim-transfer-cube
   ```
3. **자동 처리 항목**:
   - `aloha_sim_bundle.zip` 최신화 자동 생성
   - `act-aloha-sim-transfer-cube` 리포지토리 자동 생성/연결
   - `DOCS_*` 및 `.cursorrules` 등 내부 개발 문서는 자동 필터링(`ignore_patterns`)
   - 모델 가중치, 시뮬레이션 코드, HUD 렌더러, `README.md`를 **1초 만에 클라우드로 자동 전송**

---

## 🌐 오픈소스 허브 링크

- 🔗 **GitHub Repository**: [https://github.com/Hwihwa-Lab/act-aloha-sim-transfer-cube](https://github.com/Hwihwa-Lab/act-aloha-sim-transfer-cube)
- 🤗 **Hugging Face Model Hub**: [https://huggingface.co/hwihwalab/act-aloha-sim-transfer-cube](https://huggingface.co/hwihwalab/act-aloha-sim-transfer-cube)
