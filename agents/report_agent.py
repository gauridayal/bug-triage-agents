"""
Report Agent: Synthesizes ALL agent outputs into a human-readable report.
This is the final step — produces the polished output for the developer/manager.
Demonstrates Context Engineering: we compress and structure everything before synthesis.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_model

def run_report_agent(state: dict) -> dict:
    bug = state["bug_report"]
    triage = state["triage_result"]
    research = state["research_result"]
    code = state["code_result"]
    model = get_model()

    # Context Engineering: summarise everything into a clean prompt
    summary_prompt = f"""Write a professional bug resolution report for a software team.

BUG ID: {bug['id']}
TITLE: {bug['title']}

TRIAGE FINDINGS:
- Severity: {triage.get('severity')}
- Category: {triage.get('category')}
- Priority Score: {triage.get('priority_score', 'N/A')}/10
- Root Cause: {triage.get('root_cause_hypothesis', 'See details')}
- Affected Components: {', '.join(triage.get('affected_components', []))}

RESEARCH FINDINGS:
- Recommended Approach: {research.get('recommended_approach', 'N/A')}
- Estimated Fix Time: {research.get('estimated_fix_time', 'N/A')}

CODE FIX:
- Language: {code.get('language', 'N/A')}
- Fix Description: {code.get('fix_description', 'N/A')}

Write a clear, professional report with sections:
1. Executive Summary (2 sentences for non-technical stakeholders)
2. Technical Analysis
3. Resolution Steps
4. Testing Instructions
5. Prevention Recommendations

Use plain English. Be concise but complete."""

    response = model.invoke(summary_prompt)

    final_report = response.content
    print("\n[REPORT] Final report generated successfully.")
    return {"final_report": final_report}