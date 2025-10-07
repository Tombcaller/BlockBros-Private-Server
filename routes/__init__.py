from .ping import ping_bp
from .auth import *
from .master import *
from .level import *
from .gamer import *

def register_blueprints(app):
    for bp in [ping_bp, *auth_bps, *master_bps, *level_bps, *gamer_bps]:
        app.register_blueprint(bp)
