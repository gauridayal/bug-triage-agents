"""
Research Agent: Uses the triage result to research known fixes.
In a real system, this would query a bug database or StackOverflow.
Here, it uses the LLM's knowledge + the triage context.
This demonstrates A2A-style: receiving structured output from Triage Agent.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_model

RESEARCH_PROMPT = """You are a senior developer researching fixes for a classified bug.

BUG TITLE: {title}
SEVERITY: {severity}
CATEGORY: {category}
ROOT CAUSE HYPOTHESIS: {root_cause}
AFFECTED COMPONENTS: {components}

Based on this information, provide a research report as JSON (no extra text):
{{
  "similar_known_issues": ["description of similar issue 1", "similar issue 2"],
  "recommended_approach": "Detailed technical approach to fix this in 3-4 sentences",
  "libraries_to_check": ["lib1", "lib2"],
  "estimated_fix_time": "X hours/days",
  "references": ["Best practice or pattern name relevant to this fix"]
}}"""

def run_research_agent(state: dict) -> dict:
    """
    Receives triage_result from state (passed by Triage Agent via LangGraph).
    This is Agent-to-Agent (A2A) communication — structured data, not raw text.
    """
    bug = state["bug_report"]
    triage = state["triage_result"]  # ← A2A: receiving from previous agent
    model = get_model()

    prompt = RESEARCH_PROMPT.format(
        title=bug["title"],
        severity=triage.get("severity", "UNKNOWN"),
        category=triage.get("category", "Unknown"),
        root_cause=triage.get("root_cause_hypothesis", "Unknown"),
        components=", ".join(triage.get("affected_components", [])),
    )

    response = model.invoke(prompt)

    import json, re
    text = re.sub(r'```(?:json)?\s*', '', response.content.strip()).strip('`').strip()
    try:
        research_result = json.loads(text)
    except json.JSONDecodeError :
        research_result = {"raw_response": text}

    print(f"\n[RESEARCH] Found approach: {research_result.get('recommended_approach', '')[:80]}...")
    return {"research_result": research_result}