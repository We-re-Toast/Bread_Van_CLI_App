# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .driver_views import driver_views
from .resident_views import resident_views
from .admin_views import admin_views
from .common_views import common_views


views = [user_views, index_views, auth_views, common_views, driver_views, resident_views, admin_views]
# blueprints must be added to this list