from .quickGet import level_quickGet_bp
from .list import level_list_bp
from .get import level_get_bp

level_bps = [level_quickGet_bp, level_list_bp, level_get_bp]

__all__ = ["level_bps"]