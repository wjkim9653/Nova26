"""
Synthea 데이터 로드 및 조회용 모듈
patient_id_map.csv : P001 <-> uuid 매핑 테이블
observations.csv : EHR 데이터 (uuid로 조회)
"""

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent  # data/synthea 디렉토리
ID_MAP_CSV = HERE / "patient_id_map.csv"  # 환자별 UUID를 P### 형태의 환자별 ID로 매핑해두는 테이블
OBS_CSV = HERE / "observations.csv"  # Synthea 100 sample dataset csv의 observations.csv

class PatientNotFound(Exception):
    """환자 ID가 존재하지 않을 때 발생하는 예외"""

def _load_id_map():
    """patiend_id_map.csv를 로드하여 dict로 반환"""
    with open(ID_MAP_CSV, "r", encoding="utf-8", newline="") as f:
        return{row["patient_id"]: row["uuid"] for row in csv.DictReader(f)}

def _index_observations_by_uuid():
    """observations.csv를 로드하여 uuid별(환자별)로 묶어 {uuid: [rows from observations]} 반환"""
    index = {}
    with open(OBS_CSV, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            index.setdefault(row["PATIENT"], []).append(row)  # uuid별로 observations를 묶음
    return index


# --- 본 모듈 import 시 1회 로드 ---
ID_MAP = _load_id_map()
OBS_BY_UUID = _index_observations_by_uuid()


def resolve_uuid(patient_id):
    """'P001' -> uuid 형태로 변환. 존재하지 않는 환자 ID일 경우 PatientNotFound"""
    try:
        return ID_MAP[patient_id]
    except KeyError:
        raise PatientNotFound(patient_id)

def observations_for(patient_id):
    """환자 ID에 해당하는 observations.csv의 모든 관측 row list 반환"""
    uuid = resolve_uuid(patient_id)
    return OBS_BY_UUID.get(uuid, [])  # uuid에 해당하는 observations가 없으면 빈 list 반환