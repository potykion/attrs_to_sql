import re

def camelcase_to_underscore(camelcase: str) -> str:
    """https://stackoverflow.com/a/1176023"""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camelcase)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

