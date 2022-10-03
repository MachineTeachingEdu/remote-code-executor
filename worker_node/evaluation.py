"""
Module to evaluate the code submitted by the student looking for potential malicious code
"""
import os
from pathlib import Path
import json
from exceptions import DangerException

def evaluate_file(absolute_path: str):

    sast_result_file_path = absolute_path.replace(".py", "") + "_result.json"

    os.system(f'bandit "{absolute_path}"  -f json -o "{sast_result_file_path}"')

    test_output = json.load(Path(sast_result_file_path).open())

    metrics = test_output["metrics"]

    HIGH_SEVERITY = metrics["_totals"]["SEVERITY.HIGH"]
    MEDIUM_SEVERITY = metrics["_totals"]["SEVERITY.MEDIUM"]
    LOW_SEVERITY = metrics["_totals"]["SEVERITY.LOW"]
    UNDEFINED_SEVERITY = metrics["_totals"]["SEVERITY.UNDEFINED"]

    DANGER_SCORE = HIGH_SEVERITY * 3 + MEDIUM_SEVERITY * 2 + LOW_SEVERITY * 1 + UNDEFINED_SEVERITY * 0
    TOTAL_WARNINGS = HIGH_SEVERITY + MEDIUM_SEVERITY + LOW_SEVERITY + UNDEFINED_SEVERITY



    if TOTAL_WARNINGS == 0:
        return

    AVG_DANGER_SCORE = DANGER_SCORE / TOTAL_WARNINGS


    if AVG_DANGER_SCORE >= 1:
        raise DangerException("Danger score is too high")

    return