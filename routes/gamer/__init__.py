from .nickname.check import gamer_nickname_check_bp
from .put import gamer_put_bp

gamer_bps = [gamer_nickname_check_bp, gamer_put_bp]

__all__ = ["gamer_bps"]