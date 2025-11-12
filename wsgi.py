import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from datetime import datetime, timedelta

from App.database import db, get_migrate
from App.models import User, Admin, Driver, Resident, Drive, Stop, Area, Street, Subject, Observer
from App.main import create_app
from App.controllers import (get_user, get_all_users_json, get_all_users,
                             get_user_by_username, initialize)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


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
        u.logout()

    user = get_user_by_username(username)
    if user and user.login(password):
        print(f"{user.type} {user.username} logged in!")


@user_cli.command("logout", help="Logout of the Bread Van App")
def logout_user_command():
    user = User.query.filter_by(logged_in=True).first()
    if not user:
        print("No user is logged in.")
        return

    user.logout()
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

    drives = user.view_street_drives(chosen_area.id, chosen_street.id)
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

    if username is None or password is None:
        print("Username and password are required.")
        return

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print("Username already taken.")
        return

    admin.create_driver(username, password)
    print(f"Driver {username} created!")


@admin_cli.command("delete_driver", help="Deletes a driver")
@click.argument("driver_id", type=int)
def delete_driver_command(driver_id):
    admin = require_admin()
    if not admin:
        return

    driver = Driver.query.get(driver_id)
    if not driver:
        print("Invalid driver ID.")
        return
    driver_name = driver.username
    admin.delete_driver(driver_id)
    print(f"Driver {driver_name} deleted.")


@admin_cli.command("add_area", help="Add a new area")
@click.argument("name")
def add_area_command(name):
    admin = require_admin()
    if not admin:
        return

    area = admin.add_area(name)
    print(f"Area '{area.name}' added.")


@admin_cli.command("add_street", help="Add a new street to an area")
@click.argument("area_id", type=int)
@click.argument("name")
def add_street_command(area_id, name):
    admin = require_admin()
    if not admin:
        return

    area = Area.query.get(area_id)
    if not area:
        print("Invalid area ID.")
        return

    street = admin.add_street(area_id, name)
    print(f"Street '{street.name}' added to area '{area.name}'.")


@admin_cli.command("delete_area", help="Delete an area")
@click.argument("area_id", type=int)
def delete_area_command(area_id):
    admin = require_admin()
    if not admin:
        return

    area = Area.query.get(area_id)
    if not area:
        print("Invalid area ID.")
        return

    admin.delete_area(area_id)
    print(f"Area '{area.name}' deleted.")


@admin_cli.command("delete_street", help="Delete a street")
@click.argument("street_id", type=int)
def delete_street_command(street_id):
    admin = require_admin()
    if not admin:
        return

    street = Street.query.get(street_id)
    if not street:
        print("Invalid street ID.")
        return

    admin.delete_street(street_id)
    print(f"Street '{street.name}' deleted.")


@admin_cli.command("view_all_areas", help="View all areas")
def view_all_areas_command():
    admin = require_admin()
    if not admin:
        return

    areas = admin.view_all_areas()
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

    streets = admin.view_all_streets()
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

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    try:
        time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        print("Invalid time format. Use HH:MM (24-hour format).")
        return

    scheduled_datetime = datetime.combine(date, time)

    if scheduled_datetime < datetime.now():
        print("Cannot schedule a drive in the past.")
        return

    one_year_later = datetime.now() + timedelta(days=365)
    if scheduled_datetime > one_year_later:
        print("Cannot schedule a drive more than 1 year in advance.")
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

    existing_drive = Drive.query.filter_by(areaId=chosen_area.id,
                                          streetId=chosen_street.id,
                                          date=date).first()

    if existing_drive:
        confirm = input(f"A driver (ID {existing_drive.driverId}) already has a drive scheduled for this area/street on {date_str}. Confirm scheduling? (y/n): ")
        if confirm.lower() != 'y':
            print("Drive scheduling cancelled.")
            return

    driver.schedule_drive(chosen_area.id, chosen_street.id, date_str, time_str)
    print(
        f"\nDrive scheduled for {date} at {time} on {chosen_street.name}, {chosen_area.name}"
    )


@driver_cli.command("cancel_drive", help="Cancel a drive")
@click.argument("drive_id", type=int)
def cancel_drive_command(drive_id):
    driver = require_driver()
    if not driver:
        return

    driver.cancel_drive(drive_id)
    print(f"Drive {drive_id} cancelled.")


@driver_cli.command("view_my_drives", help="View driver's scheduled drives")
def view_drives_command():
    driver = require_driver()
    if not driver:
        return

    drives = [
        d for d in driver.view_drives()
        if d.status in ("Upcoming", "In Progress")
    ]
    if not drives:
        print("No scheduled drives.")
        return

    print("\nYour Scheduled Drives:")
    print("-" * 70)
    print(
        f"{'Drive ID':<10} {'Date':<12} {'Time':<8} {'Area':<20} {'Street':<20}"
    )
    print("-" * 70)
    for drive in drives:
        date_str = drive.date.strftime("%Y-%m-%d")
        time_str = drive.time.strftime("%H:%M")
        print(
            f"{drive.id:<10} {date_str:<12} {time_str:<8} {drive.area.name:<20} {drive.street.name:<20}"
        )
    print("\n")


@driver_cli.command("start_drive", help="Start a drive")
@click.argument("drive_id")
def start_drive_command(drive_id):
    driver = require_driver()
    if not driver:
        return

    current_drive = Drive.query.filter_by(driverId=driver.id,
                                          status="In Progress").first()
    if current_drive:
        print(f"You are already on drive {current_drive.id}.")
        return

    drive = Drive.query.filter_by(driverId=driver.id,
                                  id=drive_id,
                                  status="Upcoming").first()
    if not drive:
        print("Drive not found or cannot be started.")
        return

    driver.start_drive(drive_id)
    print(f"Drive {drive_id} has started.")


@driver_cli.command("end_drive", help="End the current drive")
def end_drive_command():
    driver = require_driver()
    if not driver:
        return

    current_drive = Drive.query.filter_by(driverId=driver.id,
                                          status="In Progress").first()
    if not current_drive:
        print("No drive in progress.")
        return

    driver.end_drive(current_drive.id)
    print(f"Drive {current_drive.id} has ended.")


@driver_cli.command("view_requested_stops",
                    help="View requested stops for a drive")
@click.argument("driveId")
def view_requested_stops_command(driveId):
    driver = require_driver()
    if not driver:
        return

    stops = driver.view_requested_stops(driveId)
    if not stops:
        print("No requested stops for this drive.")
        return

    print(
        f"\nRequested Stops from {stops[0].drive.street.name}, {stops[0].drive.area.name}:"
    )
    for stop in stops:
        print(
            f"#{stop.resident.houseNumber} \tResident: {stop.resident.username}"
        )


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

    house_number = click.prompt("Enter your house number", type=int)

    resident = Resident(username=username,
                        password=password,
                        areaId=chosen_area.id,
                        streetId=chosen_street.id,
                        houseNumber=house_number)
    db.session.add(resident)
    db.session.commit()
    print(
        f"Resident {username} created at #{house_number} {chosen_street.name}, {chosen_area.name}"
    )


@resident_cli.command(
    "request_stop",
    help="Requests a Stop from a drive on the resident's street")
def request_stop_command():
    resident = require_resident()
    if not resident:
        return

    drives = Drive.query.filter_by(areaId=resident.areaId,
                                   streetId=resident.streetId,
                                   status="Upcoming").all()

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
        print(
            f"{drive.id:<10} {date_str:<12} {time_str:<8} {drive.driverId:<20}"
        )
    print("\n")

    chosen_drive = click.prompt("Select a drive by ID to request a stop",
                                type=int)
    if chosen_drive < 1 or chosen_drive > len(drives):
        print("Invalid drive choice.")
        return

    existing_stop = Stop.query.filter_by(driveId=chosen_drive,
                                         residentId=resident.id).first()

    if existing_stop:
        print(f"You have already requested a stop for drive {chosen_drive}.")
        return

    resident.request_stop(chosen_drive)
    print(f"Stop requested for drive {chosen_drive}.")


@resident_cli.command("cancel_stop",
                      help="Cancel a previously requested Stop from a drive")
@click.argument("drive_id")
def cancel_stop_command(drive_id):
    resident = require_resident()
    if not resident:
        return

    stop = Stop.query.filter_by(driveId=drive_id,
                                residentId=resident.id).first()
    if not stop:
        print("No stop requested for this drive.")
        return

    resident.cancel_stop(stop.id)
    print(f"Stop for drive {drive_id} cancelled.")


@resident_cli.command("view_inbox",
                      help="View notifications in the resident's inbox")
def view_inbox_command():
    resident = require_resident()
    if not resident:
        return

    inbox = resident.view_inbox()

    if inbox:
        print("Inbox Notifications:")
        for notif in inbox:
            print(notif)
    else:
        print("Your inbox is empty.")


@resident_cli.command("view_driver_stats",
                      help="View the status and location of a driver")
@click.argument("driver_id")
def view_driver_stats_command(driver_id):
    resident = require_resident()
    if not resident:
        return

    driver = resident.view_driver_stats(driver_id)

    if not driver:
        print("Driver not found.")
        return

    if driver.status == "Offline":
        print(f"Driver {driver.username} is currently offline.")
        return

    if driver.status == "Available":
        area = Area.query.get(driver.areaId)
        print(
            f"Driver {driver.username} is currently available at {area.name}")
        return

    if driver.status == "Busy":
        area = Area.query.get(driver.areaId)
        street = Street.query.get(driver.streetId)
        print(
            f"Driver {driver.username} is currently on a drive at {street.name}, {area.name}"
        )
        return


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
