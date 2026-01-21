def render_messages(lead_description: str, prompt: str) -> list:
    return [
        {"role": "system", "content": prompt},
        {"role": "user", "content": lead_description},
    ]
