"""
Simple ReAct Medical Agent용 tools 모듈
- get_patient_temperature(patient_id): 해당 환자의 최신 체온을 화씨로 반환
- fahrenheit_to_celsius(temperature): 화씨 -> 섭씨 변환
"""

from data.synthea import dataset  # import 시 자동으로 patient_id_maps.csv와 observations.csv가 메모리에 로드됨

BODY_TEMP_LOINC = "8310-5"  # 체온 관측의 LOINC 코드 (데이터셋 스키마 지식이므로 tool 모듈에 저장)


class NoTemperatureRecord(Exception):
    """해당 환자의 체온 관측 기록이 없을 때 발생하는 예외"""


# TOOL Function Implementations
def get_patient_temperature(patient_id):
    """ID로 특정된 해당 환자의 최신 체온 기록을 화씨로 반환함."""
    rows = dataset.observations_for(patient_id)  # 환자 ID에 해당하는 모든 관측 row list
    temp_rows = [r for r in rows if r["CODE"] == BODY_TEMP_LOINC]  # 체온 관측 row만 필터링
    if not temp_rows:
        raise NoTemperatureRecord(patient_id)
    latest_row = max(temp_rows, key=lambda r: r["DATE"])  # DATE 기준으로 최신 row 선택
    celsius = float(latest_row["VALUE"])  # 관측값은 섭씨로 저장되어 있음
    return round(celsius * 9 / 5 + 32, 1)  # 섭씨 -> 화씨 변환 후 소수점 1자리로 반올림

def fahrenheit_to_celsius(temperature):
    """화씨 -> 섭씨 변환"""
    fahrenheit = float(temperature)  # tool argument가 string type으로 들어올 수 있으므로 float로 casting
    return round((fahrenheit - 32) * 5 / 9, 1)  # 소수점 1자리로 반올림


# TOOL Function Metadata
TOOLS = {
    "get_patient_temperature": {
        "func": get_patient_temperature,
        "description": "환자 ID로 그 환자의 최신 체온 기록을 화씨로 반환함. e.g. get_patient_temperature[P001]",
    },
    "fahrenheit_to_celsius": {
        "func": fahrenheit_to_celsius,
        "description": "화씨 온도를 섭씨로 변환함. e.g. fahrenheit_to_celsius[100.4]",
    },
}