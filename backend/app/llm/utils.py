from backend.app.llm.prompts.lead_analysis_v1 import LEAD_ANALYSIS_PROMPT_V1


def render_messages(lead_description: str) -> list:
    return [
        {"role": "system", "content": LEAD_ANALYSIS_PROMPT_V1},
        {"role": "user", "content": lead_description},
    ]
