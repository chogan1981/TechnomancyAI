def clean_code_block(code: str) -> str:
    """
    Strips markdown-style code fences (```python and ```)
    from the beginning and end of AI-generated code blocks.
    """
    return code.replace("```python", "").replace("```", "").strip()
