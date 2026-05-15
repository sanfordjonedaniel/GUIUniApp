import re

EMAIL_PATTERN    = re.compile(r'^[a-zA-Z]+\.[a-zA-Z]+@university\.com$')
PASSWORD_PATTERN = re.compile(r'^[A-Z][a-zA-Z]{5,}\d{3,}$')


def validate_email(email):
    return bool(EMAIL_PATTERN.match(email))


def validate_password(password):
    return bool(PASSWORD_PATTERN.match(password))


def validate_credentials(email, password):
    return validate_email(email) and validate_password(password)
