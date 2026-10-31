
from app.database import repositories
from app.database import validators
from app.auth.password import hash_password, verify_password


def register_user(user_id, email, password, role):
    """Register a user against an existing student or mentor profile."""

    if not all(isinstance(value, str) for value in (user_id, email, password, role)):
        raise ValueError("All registration fields must be text.")

    user_id = user_id.strip()
    email = email.strip().lower()
    role = role.strip().lower()

    if not user_id:
        raise ValueError("User ID cannot be empty.")

    validators.validate_email(email)

    if role not in validators.USER_ROLES:
        raise ValueError("Invalid user role.")

    # Verify that the corresponding profile exists.
    if role == "student":
        profile = repositories.get_student(user_id)
    else:
        profile = repositories.get_mentor(user_id)

    if not profile:
        raise ValueError(f"No existing {role} profile found for this ID.")

    # Prevent one profile from being linked to multiple accounts.
    if repositories.get_user_by_id(user_id):
        raise ValueError("An account already exists for this ID.")

    if repositories.get_user_by_email(email):
        raise ValueError("Email is already registered.")

    user_data = {
        "user_id": user_id,
        "email": email,
        "password_hash": hash_password(password),
        "role": role,
        "is_active": True
    }

    return repositories.create_user(user_data)


def login_user(email, password):
    """Authenticate a user using email and password."""

    if not isinstance(email, str) or not isinstance(password, str):
        return None

    email = email.strip().lower()

    if not email or not password:
        return None

    user = repositories.get_user_by_email(email)

    if not user:
        return None

    if not user.get("is_active", True):
        return None

    if not verify_password(password, user.get("password_hash")):
        return None

    return {
        "user_id": user["user_id"],
        "email": user["email"],
        "role": user["role"]
    }
