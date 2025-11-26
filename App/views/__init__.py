# blue prints are imported
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .resident import resident_views
from .notification import notification_views
from .subscription import subscription_views
from .admin import setup_admin, admin_views


views = [user_views, index_views, auth_views, resident_views, notification_views, subscription_views, admin_views]
# blueprints must be added to this list
