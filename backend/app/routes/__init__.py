from app.routes.auth import auth_bp, auth_ns
from app.routes.operations import operations_bp, operations_ns
from app.routes.stock import stock_bp, stock_ns
from app.routes.history import history_bp, history_ns
from app.routes.settings import settings_bp, settings_ns
from app.routes.profile import profile_bp, profile_ns

__all__ = [
    'auth_bp', 'auth_ns',
    'operations_bp', 'operations_ns',
    'stock_bp', 'stock_ns',
    'history_bp', 'history_ns',
    'settings_bp', 'settings_ns',
    'profile_bp', 'profile_ns'
]

