from .get import emblem_get_bp
from .post import emblem_post_bp
from .ownList import emblem_ownList_bp

emblem_bps = [emblem_get_bp, emblem_post_bp, emblem_ownList_bp]

__all__ = ["emblem_bps"]