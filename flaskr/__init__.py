import os
from dotenv import load_dotenv
import openai
from flask import Flask

# Load environment variables from .env file
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'expense_tracker.db'),
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set OpenAI API key globally
    openai.api_key = app.config['OPENAI_API_KEY']

    # Import and register blueprints
    from . import db, auth, tracker, ai

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(tracker.bp)
    app.register_blueprint(ai.bp)
    app.add_url_rule('/', endpoint='index')

    return app
