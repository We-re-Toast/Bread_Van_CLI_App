from .auth import *
from .initialize import *

from .user import (
    create_user,
    get_user_by_username,
    get_user,
    get_all_users,
    get_all_users_json,
    update_user,
    user_login,
    user_logout
)

from .resident import (
    resident_create,
    resident_request_stop,
    resident_cancel_stop,
    resident_view_driver_stats,
    resident_view_stock,
    resident_view_inbox,
    resident_subscribe,
    resident_unsubscribe
)

from .driver import (
    driver_schedule_drive,
    driver_cancel_drive,
    driver_view_drives,
    driver_start_drive,
    driver_end_drive,
    driver_view_requested_stops,
    driver_update_stock,
    driver_view_stock
)

from .admin import (
    admin_create_driver,
    admin_delete_driver,
    admin_add_area,
    admin_delete_area,
    admin_view_all_areas,
    admin_add_street,
    admin_delete_street,
    admin_view_all_streets,
    admin_add_item,
    admin_delete_item,
    admin_view_all_items,
    admin_schedule_drive
)


__all__ = [
    # user
    "create_user", "get_user_by_username", "get_user", "get_all_users",
    "get_all_users_json", "update_user", "user_login", "user_logout",

    # resident
    "resident_create", "resident_request_stop", "resident_cancel_stop",
    "resident_view_driver_stats", "resident_view_stock", "resident_view_inbox",

    # driver
    "driver_schedule_drive", "driver_cancel_drive", "driver_view_drives",
    "driver_start_drive", "driver_end_drive", "driver_view_requested_stops",
    "driver_update_stock", "driver_view_stock",

    # admin
    "admin_create_driver", "admin_delete_driver", "admin_add_area",
    "admin_delete_area", "admin_view_all_areas", "admin_add_street",
    "admin_delete_street", "admin_view_all_streets", "admin_add_item",
    "admin_delete_item", "admin_view_all_items", "admin_schedule_drive"
]
