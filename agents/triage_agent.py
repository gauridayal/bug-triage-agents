"""
Triage Agent: Reads a raw bug report and classifies it.
Outputs: severity, category, affected components, reproduction steps.
This is 'Context Engineering' in action — we give the model only
the bug info, not the full conversation history.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_model

TRIAGE_PROMPT = """You are a senior software engineer performing bug triage.
Analyze the bug report below and respond ONLY with a JSON object.

Bug Report:
Title: {title}
Description: {description}
Reporter: {reporter}
Environment: {environment}

Return this exact JSON structure (no extra text, no markdown):
{{
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "category": "Frontend|Backend|Database|API|Performance|Security|Other",
  "affected_components": ["component1", "component2"],
  "root_cause_hypothesis": "Your technical analysis in 2-3 sentences",
  "reproduction_steps": ["step1", "step2", "step3"],
  "priority_score": 1-10
}}"""

def run_triage_agent(state: dict) -> dict:
    """
    Takes bug info from state, returns triage analysis.
    'state' is the shared LangGraph state dictionary.
    """
    bug = state["bug_report"]
    model = get_model()

    # Context Engineering: we only send what THIS agent needs
    prompt = TRIAGE_PROMPT.format(
        title=bug["title"],
        description=bug["description"].strip(),
        reporter=bug["reporter"],
        environment=bug["environment"],
    )

    response = model.invoke(prompt)

    # Parse the JSON response
    import json, re
    text = response.content.strip()
    # Remove markdown code fences if the model adds them
    text = re.sub(r'```(?:json)?\s*', '', text).strip('`').strip()
    try:
        triage_result = json.loads(text)
    except json.JSONDecodeError:
        # Fallback if model returns non-JSON
        triage_result = {"severity": "HIGH", "raw_response": text}

    print(f"\n[TRIAGE] Bug classified as {triage_result.get('severity', 'UNKNOWN')} severity")
    print(f"[TRIAGE] Category: {triage_result.get('category', 'Unknown')}")

    # Return updated state — LangGraph merges this into the shared state
    return {"triage_result": triage_result}