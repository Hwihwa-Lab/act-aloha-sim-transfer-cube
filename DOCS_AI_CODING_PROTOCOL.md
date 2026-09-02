# 🤖 AI Coding Protocol (Aloha 14-DOF LeRobot 마스터 지침서)

본 문서는 AI가 `lerobot-aloha-sim` 프로젝트에서 작업할 때 '바이브 코딩(Vibe Coding)'과 물리 엔진/관절 제어 규격 왜곡을 방지하기 위한 마스터 가이드(목차)입니다.

---

## 📑 문서 맵핑 (Document Mapping)
AI는 코드 생성 및 디버깅 시, 작업 내용에 맞춰 아래의 문서를 **반드시 선행 로드**하고 준수해야 합니다.

* **시스템 아키텍처 및 데이터 흐름 변경 시:** `DOCS_SYSTEM_ARCHITECTURE.md` 필수 확인
* **에이전트 실행 순서 및 벤치마크 루프 변경 시:** `DOCS_AGENT_EXECUTION_PROTOCOL.md` 필수 확인
* **결정 이력 및 마일스톤 확인 시:** `MEMORY.md` 필수 확인

---

## 🛡️ 핵심 방어 원칙 (Guardrails)

1. **MuJoCo 14-DOF 관절 규격 왜곡 금지:**
   - Aloha Bimanual 환경의 14개 관절(좌 7, 우 7) 인덱스 매핑 및 물리 제한 범위를 임의로 변경하지 마십시오.
   - 액터 제어 토크 및 Kp/Kv 게인값은 실제 Dynamixel 서보 모터 스펙을 유지해야 합니다.

2. **지능형 제어 및 시각화 파이프라인 보존:**
   - `policy_runner.py`의 Action Chunking(50 Horizon) 및 Temporal Ensembling 알고리즘을 훼손하지 마십시오.
   - `telemetry_hud.py`의 60fps 다크 테마 HUD 오버레이, 멀티 카메라 PiP, 14개 관절 게이지 바 렌더링이 항상 정상 작동해야 합니다.

3. **정량 벤치마크 지표 무결성:**
   - 4단계 마일스톤(`P1: Left Grasp`, `P2: Alignment`, `P3: Handover`, `P4: Placement`), 성공률(%), 소요 시간(s), 모션 안정성(Jerk Metric) 측정 로직을 임의로 왜곡하거나 더미 값으로 조작하지 마십시오.

4. **저사양 PC 성능 방어 (60fps Defense):**
   - 메모리 500MB 이하 유지, OpenCV C++ 행렬 연산 기반의 무지연 렌더링을 보존하십시오.

5. **원클릭 배포 및 ZIP 아카이브 무결성:**
   - `deploy_to_hf.py`를 통한 원클릭 허깅페이스 배포 시 `aloha_sim_bundle.zip`이 최신 코드로 자동 패키징되고, `DOCS_*` 및 `.cursorrules` 등 내부 개발 문서는 제외(`ignore_patterns`)된 채 클린 업로드되어야 합니다.
