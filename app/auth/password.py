
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    """
    Securely hash a user's password before storing it.
    """

    if not isinstance(password, str) or not password.strip():
        raise ValueError("Password cannot be empty.")

    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    return generate_password_hash(password, method="scrypt")


def verify_password(password, password_hash):
    """
    Verify a password against its stored hash.
    """

    if not password or not password_hash:
        return False

    return check_password_hash(password_hash, password)
