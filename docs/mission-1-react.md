# 미션 1 — ReAct Medical Agent

첫 미팅(**2026-09-23 10:00 KST, Zoom**) 공통 미션. 에이전트 동작 원리(ReAct) 이해가 목적.

## 목표

ReAct 방식으로 도구를 호출해 환자 질문에 답하는 간단한 의료 에이전트 구현.

- 참고 논문: ReAct — https://arxiv.org/abs/2210.03629
- 모델: `gpt-5.6-luna` (API 키 없으면 교수님께 문의)
- **외부 에이전트 라이브러리 사용 금지** — Python으로 핵심 로직 직접 작성.

## 구현할 도구

- `get_patient_temperature(patient_id)` — 가상 환자 체온을 화씨(°F)로 반환
- `fahrenheit_to_celsius(temperature)` — 화씨 → 섭씨 변환

환자 데이터는 가상 데이터로 구성.

## 예시

- 질문: `환자 P001의 체온을 섭씨로 알려줘.`
- 답: `환자 P001의 체온은 섭씨 38.0도입니다.` (P001 = 100.4°F 설정 시)

## 공유

미팅에서 각자 코드·실행 로그 공유, 교수님 참고 코드도 함께 리뷰.

## 구현 위치

`mission-1-react/` 아래에 작성 예정.
