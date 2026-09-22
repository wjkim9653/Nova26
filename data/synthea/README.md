# 환자 데이터 — Synthea 합성 레코드

이 디렉터리의 환자 데이터는 **Synthea™** 로 생성된 **합성(가상) 데이터**임. 실제 환자가 아니며
개인식별정보(PII)가 아님.

## 출처

- **데이터셋**: Synthea™ *100 Sample Synthetic Patient Records* (CSV)
- **제공**: The MITRE Corporation
- **원본 파일**: `synthea_sample_data_csv_latest.zip`
- **다운로드**: 2026-09-21, https://synthea.mitre.org/downloads
- **Synthea 소프트웨어**: Apache License 2.0 — https://github.com/synthetichealth/synthea

## 사용 조건

MITRE 다운로드 페이지 명시:

> "The data is free from cost, privacy, and security restrictions. It can be used without
> restriction for a variety of secondary uses in academia, research, industry, and government."

무제한 사용이 가능하며, 출처(아래 인용) 표기만 요구됨. 대회 규칙(연구 출판 가능 라이선스 +
출처 명시)을 충족함.

## 인용

> Jason Walonoski, Mark Kramer, Joseph Nichols, Andre Quina, Chris Moesel, Dylan Hall,
> Carlton Duffett, Kudakwashe Dube, Thomas Gallagher, Scott McLachlan.
> *Synthea: An approach, method, and software mechanism for generating synthetic patients
> and the synthetic electronic health care record.*
> Journal of the American Medical Informatics Association, Volume 25, Issue 3,
> March 2018, Pages 230–238. https://doi.org/10.1093/jamia/ocx079

## 파일 구성

| 파일 | 내용 |
|------|------|
| `patients.csv` | 합성 환자 108명. 원본 Synthea 컬럼 전체. 환자 식별자 `Id` 는 UUID. |
| `observations.csv` | 관측 기록 원본 전체(시계열). 체온 = LOINC code **`8310-5`**, `CATEGORY=vital-signs`, **`VALUE` 는 섭씨(`UNITS=Cel`)**. 환자당 여러 시점 기록 존재. |
| `patient_id_map.csv` | 자체 생성 매핑: `patient_id`(P001…) ↔ `uuid`. 도구가 친숙한 외래키처럼 참조. 같은 디렉터리의 `build_patient_map.py` 로 생성함. |
| `build_patient_map.py` | `patients.csv` → `patient_id_map.csv` 생성 스크립트(데이터셋 prep). |
| `dataset.py` | 데이터 로드·조회 모듈(최신 체온 조회 등). `src/` 구현체가 import함. |

## 참고

- 체온 원본 단위는 **섭씨**임. `get_patient_temperature` 는 미션의 도구 계약에 따라 이를 **화씨로 변환**해 반환함.
- 한 환자에 체온 기록이 여러 시점 쌓여 있어, 도구는 **`DATE` 기준 최신 1건**을 선택함.
