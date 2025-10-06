from .register import auth_register_bp
from .login import auth_login_bp
from .alt_login import auth_alt_login_bp

auth_bps = [auth_register_bp, auth_login_bp, auth_alt_login_bp]

__all__ = ["auth_bps"]