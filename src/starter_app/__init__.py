"""starter_app — rename this package to fit your project."""

__version__ = "0.1.0"


def hello() -> str:
    """Return a greeting. Replace with your application code."""
    return "Hello from starter_app!"


def greet(name: str) -> str:
    """Return a personalized greeting for ``name``.

    Leading and trailing whitespace is stripped. Raise ``ValueError`` when
    ``name`` is empty or contains only whitespace.
    """
    trimmed = name.strip()
    if not trimmed:
        raise ValueError("name must not be empty")
    return f"Hello, {trimmed}!"
