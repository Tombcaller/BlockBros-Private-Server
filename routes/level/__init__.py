from .quickGet import level_quickGet_bp
from .list import level_list_bp
from .get import level_get_bp
from .post import level_post_bp
from .clear import level_clear_bp
from .update import level_update_bp

level_bps = [level_quickGet_bp, level_list_bp, level_get_bp, level_post_bp, level_clear_bp, level_update_bp]

__all__ = ["level_bps"]