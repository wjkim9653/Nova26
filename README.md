# N.O.V.A. 2026

분당서울대학교병원 의료인공지능센터 주최 **대화형 의료 진단 AI 에이전트 대회** 구현 리포.

## 문서

- [대회 정보](docs/competition.md)
- [미션 1 — ReAct Medical Agent](docs/mission-1-react.md)

## 구조

최상위를 용도별로 나눔: 문서는 `docs/`, 구현체는 `src/`, 데이터셋과 데이터셋 관련
파이썬 모듈은 `data/<데이터셋>/`, 실행 스크립트(`.sh`)는 `scripts/`.

```
docs/                          대회·미션 문서
data/synthea/                  데이터셋 + 로더/prep (patients.csv, observations.csv, dataset.py …)
src/react_medical_agent/       미션 1 구현체 (tools.py, react.py, llm.py, main.py)
scripts/                       실행 스크립트(.sh)
```

환경 관리는 `uv`로 통일함.

## 미션 1 데모 실행

`gpt-5.6-luna` 키를 `.env`에 넣은 뒤(`cp .env.example .env` 후 `OPENAI_API_KEY` 입력),
다음 커맨드 실행하여 미션1 구현체 실험(환자 ID 매핑 재생성 + 데모 3케이스: 기록없음/발열/정상) 실행 가능.

```bash
bash scripts/run_demo.sh
```

개별 실행:
```bash
uv run --env-file .env python -m src.react_medical_agent.main -q "환자 P002의 체온을 섭씨로 알려줘."
```

자세한 설명·예시 로그는 [미션 1 문서](docs/mission-1-react.md) 참고.