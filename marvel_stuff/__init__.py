from flask import Flask
from config import Config
from .authentication.routes import auth
from .site.routes import site
from .api.routes import api 
from .models import db, User, login_manager, ma
from flask_migrate import Migrate
from flask_cors import CORS
from .helpers import JSONEncoder


app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
login_manager.login_view = 'auth.signin'
#user must sign in inorder to access this route


migrate = Migrate(app, db)
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
CORS(app)

app.json_encoder = JSONEncoder