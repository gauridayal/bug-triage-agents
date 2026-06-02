import sys
import json

from orchestrator import bug_triage_app
from sample_bugs import SAMPLE_BUGS

def process_bug(bug: dict):
    print("\n" + "=" * 70)
    print(f"Bug Analysis Started | {bug['id']}")
    print(f"Title: {bug['title']}")
    print("=" * 70)

    print("\nStarting analysis workflow...\n")

    steps = [
        "Reviewing issue details",
        "Looking for likely causes",
        "Generating code fix",
        "Preparing resolution report"
    ]

    for i, step in enumerate(steps, start=1):
        print(f"  [{i}/4] {step}")

    print("\nPlease wait...\n")

    # Initial state — only the bug report is provided at start
    initial_state = {
        "bug_report": bug,
        "triage_result": {},
        "research_result": {},
        "code_result": {},
        "final_report": "",
    }

    # Run the LangGraph pipeline
    result = bug_triage_app.invoke(initial_state)

    # ── Print Results ──────────────────────────────────────
    print("\n" + "=" * 70)
    print(f"Analysis Complete | {bug['id']}")
    print("=" * 70)

    # TRIAGE
    triage = result["triage_result"]

    print("\n[1] Triage Summary")
    print("-" * 70)
    print(json.dumps(triage, indent=2))

    # RESEARCH
    print("\n[2] Investigation Notes")
    print("-" * 70)
    print(json.dumps(result["research_result"], indent=2))

    # CODE FIX
    print("\n[3] Proposed Code Fix")
    print("-" * 70)

    code = result["code_result"]

    if code.get("language"):
        print(f"Language: {code['language']}")

    print("\nOriginal Code")
    print("~" * 70)
    print(code.get("before_code", "N/A"))

    print("\nUpdated Code")
    print("~" * 70)
    print(code.get("after_code", "N/A"))

    # FINAL REPORT
    print("\n[4] Resolution Report")
    print("-" * 70)
    print(result["final_report"])

    print("\n" + "=" * 70)
    print("Processing finished successfully.")
    print("=" * 70)

    # Save report to file
    report_filename = f"report_{bug['id']}.txt"

    with open(report_filename, "w", encoding="utf-8") as f:
        f.write("BUG RESOLUTION REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Bug ID: {bug['id']}\n")
        f.write(f"Title: {bug['title']}\n\n")
        f.write("TRIAGE SUMMARY\n")
        f.write("-" * 70 + "\n")
        f.write(json.dumps(triage, indent=2))
        f.write("\n\n")
        f.write("FINAL REPORT\n")
        f.write("-" * 70 + "\n")
        f.write(result["final_report"])

    print(f"\nReport saved: {report_filename}")

    return result

if __name__ == "__main__":
    # Allow selecting a bug from command line
    bug_index = 0

    if "--bug" in sys.argv:
        idx = sys.argv.index("--bug")
        bug_index = int(sys.argv[idx + 1]) - 1

    selected_bug = SAMPLE_BUGS[bug_index]
    process_bug(selected_bug)