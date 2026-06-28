from .get import emblem_get_bp
from .post import emblem_post_bp
from .ownList import emblem_ownList_bp
from .gift import emblem_gift_bp
from .update import emblem_update_bp
from .delete import emblem_delete_bp

emblem_bps = [emblem_get_bp, emblem_post_bp, emblem_ownList_bp, emblem_gift_bp, emblem_update_bp, emblem_delete_bp]

__all__ = ["emblem_bps"]