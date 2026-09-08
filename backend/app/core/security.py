"""Password hashing and opaque session identifiers (stdlib only)."""
import hashlib
import hmac
import secrets

PREFIX = "pbkdf2_sha256$"


def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 600000)
    return f'{PREFIX}600000${salt}${digest.hex()}'


def verify_password(password, stored):
    if not stored.startswith(PREFIX):
        # Upgrade an existing plaintext account only after a successful login.
        return hmac.compare_digest(password.encode(), stored.encode())
    try:
        _, rounds, salt, digest = stored.split('$')
        actual = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), int(rounds)).hex()
        return hmac.compare_digest(actual, digest)
    except (ValueError, TypeError):
        return False


def token_digest(token):
    return hashlib.sha256(token.encode()).hexdigest()
