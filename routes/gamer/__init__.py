from .nickname.check import gamer_nickname_check_bp
from .put import gamer_put_bp
from .search import gamer_search_bp
from .get import gamer_get_bp

gamer_bps = [gamer_nickname_check_bp, gamer_put_bp, gamer_search_bp, gamer_get_bp]

__all__ = ["gamer_bps"]