class Tool:
    def __init__(self, fn, name: str, description: str = ""):
        self.fn = fn
        self.name = name
        self.description = description

def tool(name: str, description: str = ""):
    """Dekorator, um Funktionen als Nuri-Tools zu registrieren."""
    def decorator(fn):
        fn._Nuri_tool = Tool(fn, name, description)
        return fn
    return decorator
