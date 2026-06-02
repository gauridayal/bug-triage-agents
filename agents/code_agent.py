"""
Code Agent: Generates an actual code patch/fix.
Uses Qwen3-Coder — which is specifically excellent at this.
Receives structured context from both Triage and Research agents.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_model

CODE_PROMPT = """You are an expert developer. Write a code fix for this bug.

BUG: {title}
CATEGORY: {category}
ROOT CAUSE: {root_cause}
RECOMMENDED APPROACH: {approach}

Write the fix as JSON (no extra text outside the JSON):
{{
  "language": "python|javascript|java|etc",
  "fix_description": "What this code does and why it fixes the bug",
  "before_code": "The problematic code pattern (pseudocode if unknown)",
  "after_code": "The fixed code with detailed comments",
  "unit_test": "A simple test case that verifies the fix works"
}}"""

def run_code_agent(state: dict) -> dict:
    bug = state["bug_report"]
    triage = state["triage_result"]
    research = state["research_result"]
    model = get_model()

    prompt = CODE_PROMPT.format(
        title=bug["title"],
        category=triage.get("category", "Unknown"),
        root_cause=triage.get("root_cause_hypothesis", "Unknown"),
        approach=research.get("recommended_approach", "Apply best practice fix"),
    )

    response = model.invoke(prompt)

    import json, re
    text = re.sub(r'```(?:json)?\s*', '', response.content.strip()).strip('`').strip()
    try:
        code_result = json.loads(text)
    except json.JSONDecodeError:
        code_result = {"after_code": response.content, "raw": True}

    print(f"\n[CODE] Generated fix in {code_result.get('language', 'unknown')} language")
    return {"code_result": code_result}