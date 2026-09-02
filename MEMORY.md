# 🧠 프로젝트 메모리 및 의사결정 히스토리 (MEMORY.md)

## 📌 현재 상태: Phase 1 완료 (MuJoCo 14-DOF + ACT 정책 + 60fps HUD + 거버넌스 완비)

---

### 🏛️ 완료된 주요 의사결정 (Completed Decisions)

1. **물리 엔진 백엔드 선정**:
   - 저사양 PC에서의 극저지연 연산 및 고정밀 접촉 역학을 위해 MuJoCo 3.x C-바인딩 선정.
2. **시각화 아키텍처 (60fps Defense)**:
   - 무거운 웹 서버 및 브라우저 WebGL 이중 부하를 배제하고, OpenCV C++ 메모리 버퍼 직접 오버레이 방식을 채택하여 메모리 200MB 이하, 60.0 FPS 프레임 방어 달성.
3. **지능형 정책 제어 (LeRobot ACT)**:
   - Action Chunking(50 Horizon) 및 Temporal Ensembling 알고리즘을 도입하여 4단계 마일스톤(Grasp ➔ Align ➔ Handover ➔ Place) 자율 수행 및 관절 떨림 억제(Jerk: 1.245 N·m/step).
4. **글로벌 배포 & 거버넌스 체계 구축**:
   - 공식 Model Card(`README.md`), 한국어 매뉴얼(`README_KR.md`), `.cursorrules`, 5대 `DOCS_*` 체계 구축.
   - Hwihwa Lab 표준 MIT License 및 `aloha_sim_bundle.zip` 원클릭 자동 배포기(`deploy_to_hf.py`) 완비.
   - 공식 리포지토리 명명: `act-aloha-sim-transfer-cube` (GitHub & Hugging Face 동일화).

---

### 🚀 다음 개발 마일스톤 (Next Milestones)

- [ ] Hugging Face Hub 공식 `lerobot/act_aloha_sim_transfer_cube_human` 원격 가중치 직접 다운로드 및 롤아웃 벤치마크.
- [ ] 시뮬레이션 롤아웃 에피소드 데이터의 LeRobot Dataset v2 포맷(HDF5 + mp4) 자동 익스포트 파이프라인 추가.
