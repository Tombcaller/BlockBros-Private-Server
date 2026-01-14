from .list import comment_list_bp
from .post import comment_post_bp
from .delete import comment_delete_bp

comment_bps = [comment_post_bp, comment_list_bp, comment_delete_bp]

__all__ = ["comment_bps"]