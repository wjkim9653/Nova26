"""
Synthea 100 sample dataset csv의 patients.csv 내 환자별 UUID를 P### 형태의 환자별 ID로 맵핑해두는 테이블 생성
(환자 UUID 등장 순서대로 P001, P002, P003, ... 형태로 매핑)
"""

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent  # data/synthea 디렉토리
SRC = HERE / "patients.csv"  # Synthea 100 sample dataset csv
OUT = HERE / "patient_id_map.csv"  # 환자별 UUID를 P### 형태의 환자별 ID로 맵핑해두는 테이블


def main():
    # patient.csv read
    with open(SRC, "r", encoding="utf-8") as f:
        patients = list(csv.DictReader(f))  # 원본 csv의 각 row가 dict로 저장되어 있는 list

    # patient_id_map.csv write
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["patient_id", "uuid"])  # header row 먼저 작성
        for i, row in enumerate(patients, start=1):  # enumerate로 환자 row를 순회하며, i는 1부터 시작
            patient_id = f"P{i:03d}"  # P001, P002, P003, ... 형태로 매핑
            uuid = row["Id"]  # 환자별 UUID
            writer.writerow([patient_id, uuid])  # 환자별 ID와 UUID를 한 row에 작성

    print(f"{len(patients)} patients mapped to {OUT}")

if __name__ == "__main__":
    main()