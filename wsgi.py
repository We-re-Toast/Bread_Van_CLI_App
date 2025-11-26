import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from datetime import datetime, timedelta
from flask_migrate import Migrate, upgrade

from App.database import db, get_migrate
from App.models import User, Admin, Driver, Resident, Drive, Stop, Area, Street, DriverStock, Observer, SubjectMixin
from App.main import create_app
from App.controllers import (get_user, get_all_users_json, get_all_users,
                             get_user_by_username, initialize)
from App.controllers.admin import (
    admin_create_driver,
    admin_delete_driver,
    admin_add_area,
    admin_add_street,
    admin_delete_area,
    admin_delete_street,
    admin_view_all_areas,
    admin_view_all_streets
)
from App.controllers.driver import (
    driver_schedule_drive,
    driver_cancel_drive,
    driver_view_drives,
    driver_start_drive,
    driver_end_drive,
    driver_view_requested_stops,
    driver_update_drive_menu,
    driver_update_drive_eta
)
from App.controllers.resident import (
    resident_create,
    resident_request_stop,
    resident_cancel_stop,
    resident_view_inbox,
    resident_view_driver_stats,
    resident_subscribe_to_drive,
    resident_unsubscribe_from_drive,
    resident_get_subscribed_drives,
    resident_get_notifications,
    resident_get_notification_stats,
    resident_mark_notification_read,
    resident_mark_all_notifications_read,
    resident_clear_notifications,
    resident_update_notification_preferences,
    resident_request_stop_from_notification
)

from App.controllers.user import (
    user_login,
    user_logout,
    user_view_street_drives
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

with app.app_context():
    upgrade()
    existing = db.session.query(User).filter_by(username='admin').first()
    if not existing:
        new_admin = Admin(username='admin', password='adminpass')
        db.session.add(new_admin)
        db.session.commit()


# Initialisation
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('Welcome to the Bread Van App!')
    print("For documentation, visit: https://github.com/LiannMaicoo/Bread_Van_CLI_App")


# User Commands
##################################################################################
user_cli = AppGroup('user', help='User object commands')


@user_cli.command("login", help="Login to the Bread Van App")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def login_user_command(username, password):
    logged_in_users = User.query.filter_by(logged_in=True).all()
    for u in logged_in_users:
        user_logout(u)
    try:
        user = user_login(username, password)
        print(f"{user.type} {user.username} logged in!")
    except ValueError as e:
        print(str(e))


@user_cli.command("logout", help="Logout of the Bread Van App")
def logout_user_command():
    user = User.query.filter_by(logged_in=True).first()
    if not user:
        print("No user is logged in.")
        return

    user_logout(user)
    print(f'{user.username} logged out')


@user_cli.command("view_street_drives", help="View all drives on a street")
def view_street_drives_command():
    user = User.query.filter_by(logged_in=True).first()
    if not user:
        print("Must be logged in to perform this action.")
        return

    areas = Area.query.all()
    if not areas:
        print("No areas available. Please create an area first.")
        return

    print("\nAvailable Areas:")
    for i, area in enumerate(areas, start=1):
        print(f"{i}. {area.name}")

    chosen_area_index = click.prompt("Select an area by number", type=int)
    if chosen_area_index < 1 or chosen_area_index > len(areas):
        print("Invalid area choice.")
        return
    chosen_area = areas[chosen_area_index - 1]

    streets = Street.query.filter_by(areaId=chosen_area.id).all()
    if not streets:
        print(
            "No streets available in the selected area. Please create a street first."
        )
        return

    print(f"\nAvailable Streets in {chosen_area.name}:")
    for i, street in enumerate(streets, start=1):
        print(f"{i}. {street.name}")

    chosen_index = click.prompt("Select a street by number", type=int)

    if chosen_index < 1 or chosen_index > len(streets):
        print("Invalid street choice.")
        return

    chosen_street = streets[chosen_index - 1]

    drives = user_view_street_drives(user, chosen_area.id, chosen_street.id)
    if not drives:
        print("No drives scheduled for this street.")
        return

    print(
        f"\nAll Scheduled Drives on {drives[0].street.name}, {drives[0].area.name}:"
    )
    print("-" * 70)
    print(f"{'Drive ID':<10} {'Date':<12} {'Time':<8} {'Driver':<20}")
    print("-" * 70)
    for drive in drives:
        date_str = drive.date.strftime("%Y-%m-%d")
        time_str = drive.time.strftime("%H:%M")
        print(
            f"{drive.id:<10} {date_str:<12} {time_str:<8} {drive.driverId:<20}"
        )
    print("\n")


app.cli.add_command(user_cli)

# Admin Commands
##################################################################################
admin_cli = AppGroup('admin',
                     help='Admin commands for managing areas and streets')
@admin_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    admin = require_admin()
    if not admin:
        return

    users = get_all_users()
    if users is None:
        print("No users found.")
        return

    print("\nUsers in the database:")
    print("-" * 70)
    print(f"{'ID':<10} {'Username':<20} {'Type':<20}")
    print("-" * 70)
    for user in users:
        print(f"{user.id:<10} {user.username:<20} {user.type:<20}")
    print("\n")


@admin_cli.command("create_driver", help="Creates a driver")
@click.argument("username")
@click.argument("password")
def create_driver_command(username, password):
    admin = require_admin()
    if not admin:
        return
    try:
        driver = admin_create_driver(username, password)
        print(f"Driver {driver.username} created!")
    except ValueError as e:
        print(str(e))


@admin_cli.command("delete_driver", help="Deletes a driver")
@click.argument("driver_id", type=int)
def delete_driver_command(driver_id):
    admin = require_admin()
    if not admin:
        return
    try:
        driver = admin_delete_driver(driver_id)
        print(f"Driver {driver.username} deleted.")
    except ValueError as e:
        print(str(e))


@admin_cli.command("add_area", help="Add a new area")
@click.argument("name")
def add_area_command(name):
    admin = require_admin()
    if not admin:
        return
    area = admin_add_area(name)
    print(f"Area '{area.name}' added.")


@admin_cli.command("add_street", help="Add a new street to an area")
@click.argument("area_id", type=int)
@click.argument("name")
def add_street_command(area_id, name):
    admin = require_admin()
    if not admin:
        return
    try:
        street = admin_add_street(area_id, name)
        area = Area.query.get(area_id)
        print(f"Street '{street.name}' added to area '{area.name}'.")
    except ValueError as e:
        print(str(e))


@admin_cli.command("delete_area", help="Delete an area")
@click.argument("area_id", type=int)
def delete_area_command(area_id):
    admin = require_admin()
    if not admin:
        return
    try:
        area = admin_delete_area(area_id)
        print(f"Area '{area.name}' deleted.")
    except ValueError as e:
        print(str(e))


@admin_cli.command("delete_street", help="Delete a street")
@click.argument("street_id", type=int)
def delete_street_command(street_id):
    admin = require_admin()
    if not admin:
        return
    try:
        street = admin_delete_street(street_id)
        print(f"Street '{street.name}' deleted.")
    except ValueError as e:
        print(str(e))


@admin_cli.command("view_all_areas", help="View all areas")
def view_all_areas_command():
    admin = require_admin()
    if not admin:
        return
    areas = admin_view_all_areas()
    if not areas:
        print("No areas available.")
        return
    print("\nAll Areas:")
    for area in areas:
        print(f"{area.id}. {area.name}")
    print("\n")


@admin_cli.command("view_all_streets", help="View all streets")
def view_all_streets_command():
    admin = require_admin()
    if not admin:
        return
    streets = admin_view_all_streets()
    if not streets:
        print("No streets available.")
        return
    print("\nAll Streets:")
    for street in streets:
        print(f"{street.id}. {street.name} (Area ID: {street.areaId})")
    print("\n")


app.cli.add_command(admin_cli)

# Driver Commands
##################################################################################
driver_cli = AppGroup('driver', help='Driver object commands')


@driver_cli.command("schedule_drive", help="Schedule a drive")
@click.argument("date_str")
@click.argument("time_str")
def schedule_drive_command(date_str, time_str):
    driver = require_driver()
    if not driver:
        return
    # Area/street selection logic remains in CLI for user prompts
    areas = Area.query.all()
    if not areas:
        print("No areas available. Please create an area first.")
        return
    print("\nAvailable Areas:")
    for i, area in enumerate(areas, start=1):
        print(f"{i}. {area.name}")
    chosen_area_index = click.prompt("Select an area by number", type=int)
    if chosen_area_index < 1 or chosen_area_index > len(areas):
        print("Invalid area choice.")
        return
    chosen_area = areas[chosen_area_index - 1]
    streets = Street.query.filter_by(areaId=chosen_area.id).all()
    if not streets:
        print("No streets available in the selected area. Please create a street first.")
        return
    print(f"\nAvailable Streets in {chosen_area.name}:")
    for i, street in enumerate(streets, start=1):
        print(f"{i}. {street.name}")
    chosen_index = click.prompt("Select a street by number", type=int)
    if chosen_index < 1 or chosen_index > len(streets):
        print("Invalid street choice.")
        return
    chosen_street = streets[chosen_index - 1]
    
    # Get optional menu and ETA
    menu = click.prompt("Enter menu items (optional - press Enter to skip)", default="", show_default=False)
    eta_str = click.prompt("Enter ETA (optional - format HH:MM, press Enter to skip)", default="", show_default=False)
    
    menu = menu if menu else None
    eta_str = eta_str if eta_str else None
    
    try:
        new_drive = driver_schedule_drive(driver, chosen_area.id, chosen_street.id, date_str, time_str, menu, eta_str)
        print(f"\nDrive scheduled for {date_str} at {time_str} on {chosen_street.name}, {chosen_area.name}")
        if menu:
            print(f"Menu: {menu}")
        if eta_str:
            print(f"ETA: {eta_str}")
    except ValueError as e:
        print(str(e))

@driver_cli.command("update_drive_menu", help="Update menu for a drive")
@click.argument("drive_id", type=int)
@click.argument("menu")
def update_drive_menu_command(drive_id, menu):
    driver = require_driver()
    if not driver:
        return
    try:
        updated_drive = driver_update_drive_menu(driver, drive_id, menu)
        print(f"Menu updated for drive {drive_id}")
        print(f"New menu: {menu}")
    except ValueError as e:
        print(str(e))

@driver_cli.command("update_drive_eta", help="Update ETA for a drive")
@click.argument("drive_id", type=int)
@click.argument("eta_str")
def update_drive_eta_command(drive_id, eta_str):
    driver = require_driver()
    if not driver:
        return
    try:
        updated_drive = driver_update_drive_eta(driver, drive_id, eta_str)
        print(f"ETA updated for drive {drive_id}")
        print(f"New ETA: {eta_str}")
    except ValueError as e:
        print(str(e))

@driver_cli.command("cancel_drive", help="Cancel a drive")
@click.argument("drive_id", type=int)
def cancel_drive_command(drive_id):
    driver = require_driver()
    if not driver:
        return
    driver_cancel_drive(driver, drive_id)
    print(f"Drive {drive_id} cancelled.")

@driver_cli.command("view_my_drives", help="View driver's scheduled drives")
def view_drives_command():
    driver = require_driver()
    if not driver:
        return
    drives = driver_view_drives(driver)
    if not drives:
        print("No scheduled drives.")
        return
    print("\nYour Scheduled Drives:")
    print("-" * 100)
    print(f"{'Drive ID':<10} {'Date':<12} {'Time':<8} {'Area':<20} {'Street':<20} {'Menu':<30}")
    print("-" * 100)
    for drive in drives:
        date_str = drive.date.strftime("%Y-%m-%d")
        time_str = drive.time.strftime("%H:%M")
        menu_preview = drive.menu[:27] + "..." if drive.menu and len(drive.menu) > 30 else drive.menu
        print(f"{drive.id:<10} {date_str:<12} {time_str:<8} {drive.area.name:<20} {drive.street.name:<20} {menu_preview or 'No menu':<30}")
    print("\n")

@driver_cli.command("start_drive", help="Start a drive")
@click.argument("drive_id")
def start_drive_command(drive_id):
    driver = require_driver()
    if not driver:
        return
    try:
        driver_start_drive(driver, drive_id)
        print(f"Drive {drive_id} has started.")
    except ValueError as e:
        print(str(e))

@driver_cli.command("end_drive", help="End the current drive")
def end_drive_command():
    driver = require_driver()
    if not driver:
        return
    try:
        ended_drive = driver_end_drive(driver)
        print(f"Drive {ended_drive.id} has ended.")
    except ValueError as e:
        print(str(e))

@driver_cli.command("view_requested_stops", help="View requested stops for a drive")
@click.argument("driveId")
def view_requested_stops_command(driveId):
    driver = require_driver()
    if not driver:
        return
    stops = driver_view_requested_stops(driver, driveId)
    if not stops:
        print("No requested stops for this drive.")
        return
    print(f"\nRequested Stops from {stops[0].drive.street.name}, {stops[0].drive.area.name}:")
    for stop in stops:
        print(f"#{stop.resident.houseNumber} \tResident: {stop.resident.username}")


app.cli.add_command(driver_cli)

# Resident Commands
##################################################################################
resident_cli = AppGroup('resident', help='Resident object commands')


@resident_cli.command("create", help="Creates a resident")
@click.argument("username")
@click.argument("password")
def create_resident_command(username, password):
    areas = Area.query.all()
    if not areas:
        print("No areas available. Please create an area first.")
        return
    print("\nAvailable Areas:")
    for i, area in enumerate(areas, start=1):
        print(f"{i}. {area.name}")
    chosen_area_index = click.prompt("Select an area by number", type=int)
    if chosen_area_index < 1 or chosen_area_index > len(areas):
        print("Invalid area choice.")
        return
    chosen_area = areas[chosen_area_index - 1]
    streets = Street.query.filter_by(areaId=chosen_area.id).all()
    if not streets:
        print("No streets available in the selected area. Please create a street first.")
        return
    print(f"\nAvailable Streets in {chosen_area.name}:")
    for i, street in enumerate(streets, start=1):
        print(f"{i}. {street.name}")
    chosen_index = click.prompt("Select a street by number", type=int)
    if chosen_index < 1 or chosen_index > len(streets):
        print("Invalid street choice.")
        return
    chosen_street = streets[chosen_index - 1]
    house_number = click.prompt("Enter your house number", type=int)
    resident = resident_create(username, password, chosen_area.id, chosen_street.id, house_number)
    print(f"Resident {username} created at #{house_number} {chosen_street.name}, {chosen_area.name}")

@resident_cli.command("request_stop", help="Requests a Stop from a drive on the resident's street")
def request_stop_command():
    resident = require_resident()
    if not resident:
        return
    drives = Drive.query.filter_by(areaId=resident.areaId, streetId=resident.streetId, status="Upcoming").all()
    if not drives:
        print("No scheduled drives to your street.")
        return
    print("\nScheduled Drives to your Street:")
    print("-" * 50)
    print(f"{'Drive ID':<10} {'Date':<12} {'Time':<8} {'Driver ID':<10}")
    print("-" * 50)
    for drive in drives:
        date_str = drive.date.strftime("%Y-%m-%d")
        time_str = drive.time.strftime("%H:%M")
        print(f"{drive.id:<10} {date_str:<12} {time_str:<8} {drive.driverId:<20}")
    print("\n")
    chosen_drive = click.prompt("Select a drive by ID to request a stop", type=int)
    try:
        resident_request_stop(resident, chosen_drive)
        print(f"Stop requested for drive {chosen_drive}.")
    except ValueError as e:
        print(str(e))

@resident_cli.command("request_stop_by_id", help="Request a stop for a specific drive ID")
@click.argument("drive_id", type=int)
def request_stop_by_id_command(drive_id):
    resident = require_resident()
    if not resident:
        return
    try:
        stop = resident_request_stop_from_notification(resident, drive_id)
        print(f"Stop requested for drive {drive_id}.")
    except ValueError as e:
        print(str(e))

@resident_cli.command("cancel_stop", help="Cancel a previously requested Stop from a drive")
@click.argument("drive_id")
def cancel_stop_command(drive_id):
    resident = require_resident()
    if not resident:
        return
    try:
        resident_cancel_stop(resident, drive_id)
        print(f"Stop for drive {drive_id} cancelled.")
    except ValueError as e:
        print(str(e))

@resident_cli.command("view_inbox", help="View notifications in the resident's inbox")
@click.option("--unread-only", is_flag=True, help="Show only unread notifications")
def view_inbox_command(unread_only):
    resident = require_resident()
    if not resident:
        return
    notifications = resident_get_notifications(resident, unread_only=unread_only)
    if not notifications:
        print("Your inbox is empty." if not unread_only else "No unread notifications.")
        return
    
    title = "UNREAD NOTIFICATIONS" if unread_only else "ALL NOTIFICATIONS"
    print(f"\n{title}:")
    print("=" * 80)
    print(f"{'#':<3} {'Status':<6} {'Time':<19} {'Type':<15} {'Message'}")
    print("=" * 80)
    
    for i, notif in enumerate(notifications, 1):
        status = "Unread" if not notif.get('read', False) else "Read"
        notif_type = notif.get('type', 'info')
        timestamp = notif.get('timestamp', 'Unknown')
        message = notif.get('message', 'No message')
        
        print(f"{i:<3} {status:<6} {timestamp:<19} {notif_type:<15} {message}")
    
    stats = resident_get_notification_stats(resident)
    print(f"\nStatistics: {stats['total_notifications']} total, {stats['unread_notifications']} unread")

@resident_cli.command("notification_stats", help="View notification statistics")
def notification_stats_command():
    resident = require_resident()
    if not resident:
        return
    stats = resident_get_notification_stats(resident)
    print(f"\nNotification Statistics for {resident.username}:")
    print(f"   Total notifications: {stats['total_notifications']}")
    print(f"   Unread notifications: {stats['unread_notifications']}")
    print(f"   Notification preferences: {', '.join(stats['notification_preferences'])}")

@resident_cli.command("mark_notification_read", help="Mark a specific notification as read")
@click.argument("notification_index", type=int)
def mark_notification_read_command(notification_index):
    resident = require_resident()
    if not resident:
        return
    try:
        resident_mark_notification_read(resident, notification_index - 1)  
        print(f"Notification #{notification_index} marked as read.")
    except ValueError as e:
        print(str(e))

@resident_cli.command("mark_all_read", help="Mark all notifications as read")
def mark_all_read_command():
    resident = require_resident()
    if not resident:
        return
    resident_mark_all_notifications_read(resident)
    print("All notifications marked as read.")

@resident_cli.command("clear_inbox", help="Clear all notifications")
def clear_inbox_command():
    resident = require_resident()
    if not resident:
        return
    resident_clear_notifications(resident)
    print("Inbox cleared.")

@resident_cli.command("update_preferences", help="Update notification preferences")
def update_preferences_command():
    resident = require_resident()
    if not resident:
        return
    
    current_prefs = resident.notification_preferences
    available_prefs = ["drive_scheduled", "menu_updated", "eta_updated", "stop_confirmed"]
    
    print(f"\nCurrent preferences: {current_prefs}")
    print("\nAvailable notification types:")
    for i, pref in enumerate(available_prefs, 1):
        print(f"  {i}. {pref}")
    
    print("\nEnter the numbers of preferences you want (comma-separated):")
    print("Example: 1,2,4 for drive_scheduled, menu_updated, stop_confirmed")
    
    try:
        choices = click.prompt("Your choices", type=str)
        chosen_indices = [int(x.strip()) for x in choices.split(',')]
        
        new_prefs = []
        for idx in chosen_indices:
            if 1 <= idx <= len(available_prefs):
                new_prefs.append(available_prefs[idx-1])
        
        if not new_prefs:
            print("No valid preferences selected.")
            return
            
        resident_update_notification_preferences(resident, new_prefs)
        print(f"Preferences updated to: {new_prefs}")
        
    except ValueError:
        print("Invalid input. Please enter numbers separated by commas.")

@resident_cli.command("view_driver_stats", help="View the status and location of a driver")
@click.argument("driver_id")
def view_driver_stats_command(driver_id):
    resident = require_resident()
    if not resident:
        return
    try:
        driver = resident_view_driver_stats(resident, driver_id)
        if driver.status == "Offline":
            print(f"Driver {driver.username} is currently offline.")
        elif driver.status == "Available":
            area = Area.query.get(driver.areaId)
            print(f"Driver {driver.username} is currently available at {area.name}")
        elif driver.status == "Busy":
            area = Area.query.get(driver.areaId)
            street = Street.query.get(driver.streetId)
            print(f"Driver {driver.username} is currently on a drive at {street.name}, {area.name}")
    except ValueError as e:
        print(str(e))

# Resident Subscription Commands for Observer Pattern

@resident_cli.command("subscribe_drive", help="Subscribe to notifications for a drive")
@click.argument("drive_id", type=int)
def subscribe_drive_command(drive_id):
    resident = require_resident()
    if not resident:
        return
    try:
        resident_subscribe_to_drive(resident, drive_id)
        print(f"Subscribed to notifications for drive {drive_id}")
    except ValueError as e:
        print(str(e))

@resident_cli.command("unsubscribe_drive", help="Unsubscribe from notifications for a drive")
@click.argument("drive_id", type=int)
def unsubscribe_drive_command(drive_id):
    resident = require_resident()
    if not resident:
        return
    try:
        resident_unsubscribe_from_drive(resident, drive_id)
        print(f"Unsubscribed from notifications for drive {drive_id}")
    except ValueError as e:
        print(str(e))

@resident_cli.command("view_subscribed_drives", help="View drives you're subscribed to")
def view_subscribed_drives_command():
    resident = require_resident()
    if not resident:
        return
    drives = resident_get_subscribed_drives(resident)
    if not drives:
        print("You are not subscribed to any drives.")
        return
    
    print("\nYour Subscribed Drives:")
    print("-" * 100)
    print(f"{'Drive ID':<10} {'Date':<12} {'Time':<8} {'Area':<20} {'Street':<20} {'Menu':<30}")
    print("-" * 100)
    for drive in drives:
        date_str = drive.date.strftime("%Y-%m-%d")
        time_str = drive.time.strftime("%H:%M")
        menu_preview = drive.menu[:27] + "..." if drive.menu and len(drive.menu) > 30 else drive.menu
        eta_str = drive.eta.strftime("%H:%M") if drive.eta else "Not set"
        print(f"{drive.id:<10} {date_str:<12} {time_str:<8} {drive.area.name:<20} {drive.street.name:<20} {menu_preview or 'No menu':<30}")
    print("\n")


app.cli.add_command(resident_cli)


# Helper Commands
##################################################################################
def require_admin():
    user = User.query.filter_by(logged_in=True).first()
    if not user:
        print("Must be logged in first.")
        return None

    if isinstance(user, Admin):
        return user

    print("Must be logged in as a admin to perform this action.")
    return None


def require_driver():
    user = User.query.filter_by(logged_in=True).first()
    if not user:
        print("Must be logged in first.")
        return None

    if isinstance(user, Driver):
        return user

    print("Must be logged in as a driver to perform this action.")
    return None


def require_resident():
    user = User.query.filter_by(logged_in=True).first()
    if not user:
        print("Must be logged in first.")
        return None

    if isinstance(user, Resident):
        return user

    print("Must be logged in as a resident to perform this action.")
    return None


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)