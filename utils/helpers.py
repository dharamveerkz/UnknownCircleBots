import random
import string

# =========================================================
# RANDOM STRING
# =========================================================


def generate_random_string(length=6):

    chars = (
        string.ascii_letters
        + string.digits
    )

    return "".join(
        random.choice(chars)
        for _ in range(length)
    )

# =========================================================
# FORMAT USER
# =========================================================


def format_user(user):

    if user.username:

        return f"@{user.username}"

    return user.first_name

# =========================================================
# SPLIT LONG MESSAGE
# =========================================================


def split_message(
    text,
    limit=4000
):

    return [
        text[i:i + limit]
        for i in range(
            0,
            len(text),
            limit
        )
    ]

# =========================================================
# RANDOM CHOICE SAFE
# =========================================================


def safe_random_choice(items):

    if not items:
        return None

    return random.choice(items)
