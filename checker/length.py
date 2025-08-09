def length_points(password):
    """Assign points based on password length."""
    length = len(password)
    if length < 8:
        return 1
    elif 8 <= length <= 12:
        return 6
    else:
        return 7