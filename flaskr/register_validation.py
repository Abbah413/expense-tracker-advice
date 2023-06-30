import re


def is_valid(username: str, password: str):
    if not username:
        error = 'Username is required.'
        return error
    if len(password) < 8:
        error = 'Password must be at least 8 characters.'
        return error
    if len(password) > 15:
        error = "Password can't be more than 15 characters."
        return error
    if not re.search(r'\d', password):
        error = 'Password must contain at least one number.'
        return error
    if not has_special_characters(password):
        error = 'Password must contain at least one special character.'
        return error
    if not password:
        error = 'Password is required.'
        return error

    return None


def has_special_characters(password: str):
    special_characters = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
    return special_characters.search(password) is not None