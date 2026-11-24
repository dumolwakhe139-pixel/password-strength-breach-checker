"""Password strength scoring rules (maximum score = 6)."""

COMMON_PATTERNS = ["123", "password", "qwerty"]


def score_password(password):
    """Return a strength score from 0 to 6 using the project's rules."""
    score = 0

    # Rule 1 and 2: length
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1

    # Rule 3 to 6: character variety
    if any(ch.islower() for ch in password):
        score += 1
    if any(ch.isupper() for ch in password):
        score += 1
    if any(ch.isdigit() for ch in password):
        score += 1
    if any(not ch.isalnum() for ch in password):
        score += 1

    # Rule 7: penalty for easy-to-guess patterns
    lowered = password.lower()
    for pattern in COMMON_PATTERNS:
        if pattern in lowered:
            score -= 2
            break  # apply the penalty only once

    return max(score, 0)


def get_rating(score):
    """Convert a numeric score into Weak / Medium / Strong."""
    if score <= 2:
        return "Weak"
    if score <= 4:
        return "Medium"
    return "Strong"


def get_feedback(password):
    """Return a list of tips explaining how to improve the password."""
    tips = []
    if len(password) < 8:
        tips.append("Use at least 8 characters.")
    elif len(password) < 12:
        tips.append("Use 12 or more characters for extra strength.")
    if not any(ch.islower() for ch in password):
        tips.append("Add a lowercase letter.")
    if not any(ch.isupper() for ch in password):
        tips.append("Add an uppercase letter.")
    if not any(ch.isdigit() for ch in password):
        tips.append("Add a number.")
    if not any(not ch.isalnum() for ch in password):
        tips.append("Add a symbol such as ! @ # $.")
    lowered = password.lower()
    if any(p in lowered for p in COMMON_PATTERNS):
        tips.append("Avoid common patterns like 123, password or qwerty.")
    return tips


if __name__ == "__main__":
    print(score_password("Pass123"))        # expected 1
    print(score_password("k9#Lm2!vQx7r"))   # expected 6
