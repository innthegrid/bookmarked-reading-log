# backend/routes/__init__.py
from .books import books_bp
from .library import library_bp
from .dashboard import dashboard_bp
from .stats import stats_bp
from .goals import goals_bp

all_blueprints = [
    books_bp,
    library_bp,
    dashboard_bp,
    stats_bp,
    goals_bp
]