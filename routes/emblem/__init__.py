from .get import emblem_get_bp
from .post import emblem_post_bp
from .ownList import emblem_own_list_bp

emblem_bps = [emblem_get_bp, emblem_post_bp, emblem_own_list_bp]

__all__ = ["emblem_bps"]