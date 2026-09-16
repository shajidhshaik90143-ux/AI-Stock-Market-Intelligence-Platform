def format_currency(value):
    """Format a number as a readable currency value."""

    if value is None:
        return "N/A"

    try:
        value = float(value)

        if abs(value) >= 1_000_000_000_000:
            return f"${value / 1_000_000_000_000:.2f}T"

        if abs(value) >= 1_000_000_000:
            return f"${value / 1_000_000_000:.2f}B"

        if abs(value) >= 1_000_000:
            return f"${value / 1_000_000:.2f}M"

        if abs(value) >= 1_000:
            return f"${value / 1_000:.2f}K"

        return f"${value:,.2f}"

    except (ValueError, TypeError):
        return str(value)


def format_number(value):
    """Format a number."""

    if value is None:
        return "N/A"

    try:
        return f"{float(value):,.2f}"

    except (ValueError, TypeError):
        return str(value)


def format_percent(value):
    """Format a percentage."""

    if value is None:
        return "N/A"

    try:
        return f"{float(value):.2f}%"

    except (ValueError, TypeError):
        return str(value)


def format_large_number(value):
    """Format large numbers using K, M and B."""

    if value is None:
        return "N/A"

    try:

        value = float(value)

        if abs(value) >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f}B"

        if abs(value) >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"

        if abs(value) >= 1_000:
            return f"{value / 1_000:.2f}K"

        return f"{value:.2f}"

    except (ValueError, TypeError):
        return str(value)