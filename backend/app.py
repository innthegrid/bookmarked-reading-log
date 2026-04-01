# backend/app.py
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

from extensions import db
from routes import all_blueprints

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-placeholder-123')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    db.init_app(app)
    
    for bp in all_blueprints:
        app.register_blueprint(bp)
    
    @app.route('/api/health')
    def health():
      return {'status': 'ok'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    from models import User
    
    with app.app_context():
        db.create_all()
            
    app.run(debug=True, port=5001)