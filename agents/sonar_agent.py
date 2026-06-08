"""
Sonar Agent

Runs SonarScanner,
fetches live SonarQube metrics,
and returns structured findings.
"""

import os
import subprocess
import requests
import json

from dotenv import load_dotenv

load_dotenv()

SONAR_URL = os.getenv("SONAR_URL")
SONAR_TOKEN = os.getenv("SONAR_TOKEN")
SONAR_PROJECT_KEY = os.getenv("SONAR_PROJECT_KEY")
SONAR_SCANNER_PATH = os.getenv("SONAR_SCANNER_PATH")

#print("SONAR_URL =", SONAR_URL)
#print("SONAR_PROJECT_KEY =", SONAR_PROJECT_KEY)
#print("SONAR_SCANNER_PATH =", SONAR_SCANNER_PATH)
#print("TOKEN EXISTS =", SONAR_TOKEN is not None)

#print("[SONAR] Token loaded:", SONAR_TOKEN[:10] if SONAR_TOKEN else "NONE")
#print("[SONAR] Project:", SONAR_PROJECT_KEY)
def run_sonar_agent(state: dict) -> dict:

    print("\n[SONAR] Starting SonarQube analysis...")

    try:

        scan_command = [
            SONAR_SCANNER_PATH,
            f"-Dsonar.token={SONAR_TOKEN}"
        ]

        print("SCAN COMMAND =", scan_command)
        scan_result = subprocess.run(
            scan_command,
            capture_output=True,
            text=True
        )

        if scan_result.returncode != 0:
            print("\n[SONAR ERROR]")
            print(scan_result.stderr)

            return {
                "sonar_result": {
                    "quality_gate": "SCAN_FAILED",
                    "maintainability": "UNKNOWN",
                    "security": "UNKNOWN",
                    "reliability": "UNKNOWN",
                    "open_issues": 0,
                    "issues": [
                        "SonarScanner execution failed"
                    ]
                }
            }

        auth = (SONAR_TOKEN, "")

        quality_url = (
            f"{SONAR_URL}/api/qualitygates/project_status"
            f"?projectKey={SONAR_PROJECT_KEY}"
        )

        quality_response = requests.get(
            quality_url,
            auth=auth
        ).json()

        measures_url = (
            f"{SONAR_URL}/api/measures/component"
            f"?component={SONAR_PROJECT_KEY}"
            f"&metricKeys=bugs,vulnerabilities,code_smells,reliability_rating,security_rating,sqale_rating"
        )

        measures_response = requests.get(
            measures_url,
            auth=auth
        ).json()

        #print("\n[SONAR DEBUG] Measures Response:")
        #print(measures_response)

        #print("\n[SONAR DEBUG] Quality Response:")
        #print(quality_response)

        

        issues_url = (
            f"{SONAR_URL}/api/issues/search"
            f"?componentKeys={SONAR_PROJECT_KEY}"
        )

        issues_response = requests.get(
            issues_url,
            auth=auth
        ).json()

        #print("\n[SONAR DEBUG] Issues Response:")
        #print(issues_response)

        measures = {}

        for metric in measures_response["component"]["measures"]:
            measures[metric["metric"]] = metric["value"]

        sonar_result = {
            "quality_gate":
                quality_response["projectStatus"]["status"],

            "maintainability":
                measures.get("sqale_rating", "N/A"),

            "security":
                measures.get("security_rating", "N/A"),

            "reliability":
                measures.get("reliability_rating", "N/A"),

            "open_issues":
                issues_response["total"],

            "bugs":
                int(measures.get("bugs", 0)),

            "vulnerabilities":
                int(measures.get("vulnerabilities", 0)),

            "code_smells":
                int(measures.get("code_smells", 0)),

            "issues": [
                issue["message"]
                for issue in issues_response["issues"]
            ]
        }

        print(
            f"[SONAR] Quality Gate: "
            f"{sonar_result['quality_gate']}"
        )

        print(
            f"[SONAR] Open Issues: "
            f"{sonar_result['open_issues']}"
        )
        filepath = os.path.abspath("sonar_report.json")

        with open(filepath, "w") as f:
            json.dump(sonar_result, f, indent=4)

        print(f"[SONAR] JSON report saved at: {filepath}")

        return {
            "sonar_result": sonar_result
        }

    except Exception as e:

        print("\n[SONAR ERROR]")
        print(str(e))

        return {
            "sonar_result": {
                "quality_gate": "ERROR",
                "maintainability": "UNKNOWN",
                "security": "UNKNOWN",
                "reliability": "UNKNOWN",
                "open_issues": 0,
                "issues": [str(e)]
            }
        }

