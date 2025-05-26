from Nuri_sdk import tool

@tool(name="echo", description="Gibt den Text unverändert zurück.")
def echo(text: str) -> str:
    """Einfacher Test-Skill."""
    return text
