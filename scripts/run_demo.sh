#!/usr/bin/env bash
# 미션 1 ReAct Medical Agent — 실험 재현 스크립트
# 매핑 테이블 재생성 후, 데모 3케이스(기록없음 / 발열 / 정상)를 실행한다.
# 사용: bash scripts/run_demo.sh   (리포 루트가 아니어도 됨)
set -euo pipefail

# 리포 루트로 이동 (이 스크립트는 scripts/ 안에 있음)
cd "$(dirname "$0")/.."

# 모델 호출용 키 확인
if [ ! -f .env ]; then
  echo "[!] .env 가 없습니다. 'cp .env.example .env' 후 OPENAI_API_KEY 를 채우세요." >&2
  exit 1
fi

echo "### 1) 환자 ID 매핑 재생성 (patients.csv -> patient_id_map.csv)"
uv run python data/synthea/build_patient_map.py

demo() {
  echo
  echo "======================================================================"
  echo "Q: $1"
  echo "======================================================================"
  uv run --env-file .env python -m src.react_medical_agent.main -q "$1"
}

echo
echo "### 2) ReAct 에이전트 데모"
demo "환자 P001의 체온을 섭씨로 알려줘."   # 체온 기록 없는 환자 → "기록 없음" 처리
demo "환자 P002의 체온을 섭씨로 알려줘."   # 발열 (100.2°F → 37.9°C)
demo "환자 P003의 체온을 섭씨로 알려줘."   # 정상 (98.8°F → 37.1°C)

echo
echo "### 완료"
