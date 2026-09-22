# N.O.V.A. 2026

분당서울대학교병원 의료인공지능센터 주최 **대화형 의료 진단 AI 에이전트 대회** 준비 저장소.
미팅 공통 미션과 대회 과제를 미션 단위로 구현·관리한다.

## 문서

- [대회 정보](docs/competition.md)
- [미션 1 — ReAct Medical Agent](docs/mission-1-react.md)

## 구조

최상위를 용도별로 나눈다: 문서는 `docs/`, 구현체는 `src/`, 데이터셋과 데이터셋 관련
파이썬 모듈은 `data/<데이터셋>/`, 실행 스크립트(`.sh`)는 `scripts/`.

```
docs/                          대회·미션 문서
data/synthea/                  데이터셋 + 로더/prep (patients.csv, observations.csv, dataset.py …)
src/react_medical_agent/       미션 1 구현체 (tools.py, react.py, llm.py, main.py)
scripts/                       실행 스크립트(.sh)
```

환경 관리는 `uv`. 실행은 리포 루트에서 `uv run python -m src.react_medical_agent.main`.
