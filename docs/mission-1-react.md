# 미션 1 — ReAct Medical Agent

첫 미팅(**2026-09-23 10:00 KST, Zoom**) 공통 미션. 외부 에이전트 라이브러리 없이 **ReAct 루프를
직접 구현**해 에이전트 동작 원리를 익힘.

> 참고 논문: ReAct — https://arxiv.org/abs/2210.03629 · 모델: `gpt-5.6-luna` (OpenAI 호환)

## 목표

가상 환자에게 질문하면, 도구를 호출해 정보를 얻고 답하는 에이전트를 만듦.

- 예시 질문: `환자 P002의 체온을 섭씨로 알려줘.` → `환자 P002의 체온은 37.9°C입니다.`
- 직접 구현한 도구 2개:
  - `get_patient_temperature(patient_id)` — 그 환자의 **최신** 체온을 화씨(°F)로 반환
  - `fahrenheit_to_celsius(temperature)` — 화씨 → 섭씨 변환

## 동작 원리 (ReAct)

LLM이 **Thought(추론) → Action(도구 호출)** 을 내면, 코드가 도구를 실행해 **Observation(관찰)** 을
돌려주는 걸 반복하다가 `Finish[답]` 으로 종료함.

```
Thought: 환자 P002의 최신 체온을 확인한 후 섭씨로 변환하겠습니다.
Action: get_patient_temperature[P002]
Observation: 100.2               ← 코드가 도구를 실제 실행해 채움
Thought: 100.2°F를 섭씨로 변환하겠습니다.
Action: fahrenheit_to_celsius[100.2]
Observation: 37.9
Action: Finish[환자 P002의 체온은 37.9°C입니다.]
```

- 한 호출은 `Observation:` 직전까지만 취해 모델이 관찰을 **지어내지 못하게 함**.
- `gpt-5.6-luna`는 API의 `stop` 파라미터를 지원하지 않아, **응답을 받은 뒤 코드에서 잘라** stop을
  흉내 냄(`llm.py`의 `_truncate_at_stop`).

## 구조

```
src/react_medical_agent/
  main.py     진입점 (argparse, 질문 → run_react)
  react.py    ReAct 루프 + 시스템 프롬프트 + Action 파싱
  tools.py    도구 2개 + 도구 레지스트리(TOOLS)  (체온=LOINC 8310-5 지식은 여기)
  llm.py      gpt-5.6-luna 클라이언트 (stop 미지원 → 클라이언트 truncate)
data/synthea/
  dataset.py            데이터 로드 + 접근 (P-id→uuid, 환자별 관측 조회)
  build_patient_map.py  patients.csv → patient_id_map.csv 생성(prep)
  patients.csv / observations.csv / patient_id_map.csv / README.md(출처)
```

역할 분리: **`dataset.py`는 로드·접근만**, "체온만 골라 최신 선택" 같은 **검색·판단은 도구(`tools.py`)** 가 함.

## 데이터

Synthea 100-sample 합성 데이터(출처·라이선스는 [`data/synthea/README.md`](../data/synthea/README.md)).

- 체온은 `observations.csv`에 LOINC `8310-5`, **섭씨(`Cel`)** 로, 환자당 여러 시점 저장 →
  도구가 `DATE` 기준 **최신 1건**을 고름.
- `patient_id_map.csv`: `P001…P108 ↔ uuid`(전 환자, `patients.csv` 등장 순서). 도구가 외래키처럼 참조함.
- **`P001`은 체온 기록이 없는 환자**라, "기록 없음"을 어떻게 처리하는지 보여주는 데모 케이스로 씀.

## 실행

환경 관리는 `uv`. 모델 호출용 키가 필요함.

```bash
# 1) .env 준비: OPENAI_API_KEY(=gpt-5.6-luna 키) 입력. cp .env.example .env 후 편집.
uv add openai

# 2) 오늘 실험 전체 재현 (매핑 재생성 + 데모 3케이스)
bash scripts/run_demo.sh

# 개별 실행
uv run --env-file .env python -m src.react_medical_agent.main -q "환자 P002의 체온을 섭씨로 알려줘."
```

## 실행 예시 로그

**① 체온 기록 없는 환자 (P001) — "기록 없음" 처리**
```
Action: get_patient_temperature[P001]
Observation: 오류: NoTemperatureRecord: P001
Action: Finish[환자 P001의 체온 기록이 없어 섭씨로 알려드릴 수 없습니다.]
```
도구가 예외를 던지면 루프가 이를 Observation으로 넘기고, 모델이 상황을 인지해 답함.

**② 발열 환자 (P002) — 100.2°F → 37.9°C**
```
Action: get_patient_temperature[P002] → Observation: 100.2
Action: fahrenheit_to_celsius[100.2]  → Observation: 37.9
Action: Finish[환자 P002의 체온은 37.9°C입니다.]
```

**③ 정상 환자 (P003) — 98.8°F → 37.1°C**
```
Action: get_patient_temperature[P003] → Observation: 98.8
Action: fahrenheit_to_celsius[98.8]   → Observation: 37.1
Action: Finish[환자 P003의 체온은 37.1°C입니다.]
```

## 구현 메모

- **`stop` 미지원**: `gpt-5.6-luna`는 chat.completions에서 `stop`을 거부(400) → 응답 후 클라이언트에서 절단함.
- **단위 순환**: 원본 데이터셋 온도 단위가 섭씨였음. `get_patient_temperature` 툴에서 화씨로 변환한 값을 반환하고 → `fahrenheit_to_celsius`가
  다시 섭씨로 변환한 값을 반환함.
- **no-record**: 현재는 예외 처리해둠(오류 raise). 정상 결과로 간주하는 문구로 리턴하도록 구현 수정 가능하나, 지금 예외처리 해둔 구현으로도 에이전트 모델이 제대로 답변하는 모습 확인함
