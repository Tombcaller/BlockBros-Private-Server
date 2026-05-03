#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Flask
from flask_cors import CORS

#§ Server Utility Imports §#
from routes import register_blueprints
from models import db, Level
import config

#§ Misc Imports §#
import os
#§ ------------------------- §#

#§ Creating "storage" folder for database §#
basedir = os.path.abspath(os.path.dirname(__file__))
storage_dir = os.path.join(basedir, "storage")
os.makedirs(storage_dir, exist_ok=True)

#§ Registering blueprints with app §#
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["POST"]}})
register_blueprints(app)

#§ Database config §#
db_path = os.path.abspath(os.path.join(storage_dir, config.serverConfig["db_name"]))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#§ Creating database tables (from models.py) §#
with app.app_context():
    db.create_all()

    #§ Set levelId autoincrement to start at 10001 by making placeholder level §#
    if not Level.query.first():
        placeholderLevel = Level(levelId=10000, internalId=0, gamerInternalId=0, title="Placeholder", theme=0, levelMap="{}", completionTime=0)
        db.session.add(placeholderLevel)
        db.session.commit()

#§ Running server on 0.0.0.0 (To accept all incoming traffic addresses) on port 8108 §#
if __name__ == "__main__":
    app.run(host= config.serverConfig["host"],
            port= config.serverConfig["port"],
            debug=config.serverConfig["debug"])

    