#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Flask

#§ Server Utility Imports §#
from routes import register_blueprints
from models import db

#§ Misc Imports §#
import os
#§ ------------------------- §#

#§ Creating "storage" folder for database §#
basedir = os.path.abspath(os.path.dirname(__file__))
storage_dir = os.path.join(basedir, "storage")
os.makedirs(storage_dir, exist_ok=True)

#§ Registering blueprints with app §#
app = Flask(__name__)
register_blueprints(app)

#§ Database config §#
db_path = os.path.join(storage_dir, "data.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#§ Creating database tables (from models.py)§#
with app.app_context():
    db.create_all()

#§ Running server on 0.0.0.0 (To accept all incoming traffic addresses) on port 5000 §#
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
