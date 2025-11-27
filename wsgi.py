import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from App.database import db, get_migrate
from App.models import User
from App.models.enums import DriverStatus, DriveStatus
from App.main import create_app
from App.controllers import initialize
from App.controllers.user import *
from App.controllers.admin import *
from App.controllers.driver import *
from App.controllers.drive import *
from App.controllers.resident import *
from App.controllers.stop_request import *
from App.controllers.item import *
from App.controllers.area import *
from App.controllers.street import *
from App.controllers.notification import (
    get_notification_history,
    mark_notification_as_read,
)
from App.utils.cli_helpers import (
    get_area_id,
    get_street_id,
    get_driver_id,
    get_resident_id,
    get_item_id,
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print("database intialized")


"""
User Commands
"""

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup("user", help="User object commands")


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f"{username} created!")


# this command will be : flask user create bob bobpass


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == "string":
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli)  # add the group to the cli

"""
Admin Commands
"""
admin_cli = AppGroup("admin", help="Admin object commands")


@admin_cli.command(
    "create-driver",
    help="Creates a driver, do create-driver <username> <password> <status> <area_name> <street_name>, area_name and street_name are optional, status can be 'Off Duty' or 'On Duty'",
)
@click.argument("username")
@click.argument("password")
@click.argument("status", type=click.Choice([s.value for s in DriverStatus]))
@click.argument("area_name", default=None)
@click.argument("street_name", default=None)
def create_driver_command(username, password, status, area_name, street_name):
    try:
        area_id = get_area_id(area_name) if area_name else None
        street_id = get_street_id(street_name, area_id) if street_name else None
        create_driver(username, password, status, area_id, street_id)
        print(f"Driver {username} created!")
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command(
    "create-resident",
    help="Creates a resident, do create-resident <username> <password> <area_name> <street_name> <house_number>",
)
@click.argument("username")
@click.argument("password")
@click.argument("area_name")
@click.argument("street_name")
@click.argument("house_number")
def create_resident_command(username, password, area_name, street_name, house_number):
    try:
        area_id = get_area_id(area_name)
        street_id = get_street_id(street_name, area_id)
        create_resident(username, password, area_id, street_id, house_number)
        print(f"Resident {username} created!")
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command("create-area", help="Creates an area, do create-area <name>")
@click.argument("name")
def create_area_command(name):
    try:
        create_area(name)
        print(f"Area {name} created!")
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command(
    "create-street", help="Creates a street, do create-street <name> <area_name>"
)
@click.argument("name")
@click.argument("area_name")
def create_street_command(name, area_name):
    try:
        area_id = get_area_id(area_name)
        create_street(name, area_id)
        print(f"Street {name} created!")
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command("list-drivers", help="Lists all drivers")
@click.argument("format", default="string")
def list_drivers_command(format):
    try:
        if format == "string":
            print(get_all_drivers())
        else:
            print(get_all_drivers_json())
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command("list-residents", help="Lists all residents")
@click.argument("format", default="string")
def list_residents_command(format):
    try:
        if format == "string":
            print(get_all_residents())
        else:
            print(get_all_residents_json())
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command("list-areas", help="Lists all areas")
@click.argument("format", default="string")
def list_areas_command(format):
    try:
        if format == "string":
            print(get_all_areas())
        else:
            print(get_all_areas_json())
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command("list-streets", help="Lists all streets, do list-streets <format>")
@click.argument("format", default="string")
def list_streets_command(format):
    try:
        if format == "string":
            print(get_all_streets())
        else:
            print(get_all_streets_json())
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command(
    "update-street", help="Updates a street, do update-street <street_id> <new_name>"
)
@click.argument("street_id")
@click.argument("new_name")
def update_street_command(street_id, new_name):
    try:
        update_street_name(street_id, new_name)
        print(f"Street {street_id} updated!")
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command(
    "update-area", help="Updates an area, do update-area <area_id> <new_name>"
)
@click.argument("area_id")
@click.argument("new_name")
def update_area_command(area_id, new_name):
    try:
        update_area_name(area_id, new_name)
        print(f"Area {area_id} updated!")
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command(
    "delete-driver", help="Deletes a driver, do delete-driver <driver_id>"
)
@click.argument("driver_id")
def delete_driver_command(driver_id):
    try:
        delete_driver(driver_id)
        print(f"Driver {driver_id} deleted!")
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command(
    "delete-resident", help="Deletes a resident, do delete-resident <resident_id>"
)
@click.argument("resident_id")
def delete_resident_command(resident_id):
    try:
        delete_resident(resident_id)
        print(f"Resident {resident_id} deleted!")
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command("delete-area", help="Deletes an area, do delete-area <area_id>")
@click.argument("area_id")
def delete_area_command(area_id):
    try:
        delete_area(area_id)
        print(f"Area {area_id} deleted!")
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command(
    "delete-street", help="Deletes a street, do delete-street <street_id>"
)
@click.argument("street_id")
def delete_street_command(street_id):
    try:
        delete_street(street_id)
        print(f"Street {street_id} deleted!")
    except Exception as e:
        print(f"Error: {e}")


app.cli.add_command(admin_cli)


"""
Driver Commands
"""

driver_cli = AppGroup("driver", help="Driver object commands")


@driver_cli.command(
    "schedule-drive",
    help="Schedules a drive. Usage: schedule-drive <driver> <area> <street> <date> <time> --item Name:Qty",
)
@click.argument("driver_username")
@click.argument("area_name")
@click.argument("street_name")
@click.argument("date_str")
@click.argument("time_str")
@click.option(
    "--item", "-i", multiple=True, help="Item to add in format 'Name:Quantity'"
)
def schedule_drive_command(
    driver_username, area_name, street_name, date_str, time_str, item
):
    try:
        driver_id = get_driver_id(driver_username)
        area_id = get_area_id(area_name)
        street_id = get_street_id(street_name, area_id)

        items_list = []
        if item:
            for i in item:
                try:
                    name, quantity = i.split(":")
                    item_id = get_item_id(name.strip())
                    items_list.append({"item_id": item_id, "quantity": int(quantity)})
                except ValueError:
                    print(f"Error: Invalid item format '{i}'. Use 'Name:Quantity'")
                    return

        new_drive = schedule_drive(
            driver_id,
            area_id,
            street_id,
            date_str,
            time_str,
            DriveStatus.SCHEDULED,
            items=items_list,
        )
        print(f"Drive scheduled for driver {driver_username} with ID {new_drive.id}")
    except Exception as e:
        print(f"Error: {e}")


@driver_cli.command(
    "view-drives",
    help="Views all drives for a driver, do view-drives <driver_username>",
)
@click.argument("driver_username")
def view_drives_command(driver_username):
    try:
        driver_id = get_driver_id(driver_username)
        drives = view_drives(driver_id)
        print(f"Drives for driver {driver_username}: {drives}")
    except Exception as e:
        print(f"Error: {e}")


@driver_cli.command(
    "start-drive", help="Starts a drive, do start-drive <driver_username> <drive_id>"
)
@click.argument("driver_username")
@click.argument("drive_id")
def start_drive_command(driver_username, drive_id):
    try:
        driver_id = get_driver_id(driver_username)
        start_drive(driver_id, drive_id)
        print(f"Drive started for driver {driver_username}!")
    except Exception as e:
        print(f"Error: {e}")


@driver_cli.command(
    "complete-drive",
    help="Completes a drive, do complete-drive <driver_username> <drive_id>",
)
@click.argument("driver_username")
@click.argument("drive_id")
def complete_drive_command(driver_username, drive_id):
    try:
        driver_id = get_driver_id(driver_username)
        complete_drive(driver_id, drive_id)
        print(f"Drive completed for driver {driver_username}!")
    except Exception as e:
        print(f"Error: {e}")


@driver_cli.command(
    "update-driver-status",
    help="Updates a driver's status, do update-driver-status <driver_username> <status>, status can be 'Off Duty' or 'On Duty'",
)
@click.argument("driver_username")
@click.argument("status", type=click.Choice([s.value for s in DriverStatus]))
def update_driver_status_command(driver_username, status):
    try:
        driver_id = get_driver_id(driver_username)
        update_driver_status(driver_id, status)
        print(f"Driver status updated for driver {driver_username}!")
    except Exception as e:
        print(f"Error: {e}")


@driver_cli.command(
    "update-username",
    help="Updates a driver's username, do update-username <driver_username> <new_username>",
)
@click.argument("driver_username")
@click.argument("new_username")
def update_username_command(driver_username, new_username):
    try:
        driver_id = get_driver_id(driver_username)
        update_username(driver_id, new_username)
        print(f"Username updated for driver {driver_username}!")
    except Exception as e:
        print(f"Error: {e}")


@driver_cli.command(
    "update-area-id",
    help="Updates a driver's area ID, do update-area-id <driver_username> <area_name>",
)
@click.argument("driver_username")
@click.argument("area_name")
def update_area_id_command(driver_username, area_name):
    try:
        driver_id = get_driver_id(driver_username)
        area_id = get_area_id(area_name)
        update_area_id(driver_id, area_id)
        print(f"Area ID updated for driver {driver_username}!")
    except Exception as e:
        print(f"Error: {e}")


@driver_cli.command(
    "update-street-id",
    help="Updates a driver's street ID, do update-street-id <driver_username> <street_name> <area_name>",
)
@click.argument("driver_username")
@click.argument("street_name")
@click.argument("area_name")
def update_street_id_command(driver_username, street_name, area_name):
    try:
        driver_id = get_driver_id(driver_username)
        area_id = get_area_id(area_name)
        street_id = get_street_id(street_name, area_id)
        update_street_id(driver_id, street_id)
        print(f"Street ID updated for driver {driver_username}!")
    except Exception as e:
        print(f"Error: {e}")


@driver_cli.command(
    "add-drive-item",
    help="Adds an item to a drive, do add-drive-item <driver_username> <drive_id> <item_name> <quantity>",
)
@click.argument("driver_username")
@click.argument("drive_id")
@click.argument("item_name")
@click.argument("quantity")
def add_drive_item_command(driver_username, drive_id, item_name, quantity):
    try:
        driver_id = get_driver_id(driver_username)
        item_id = get_item_id(item_name)
        add_drive_item(drive_id, item_id, quantity)
        print(f"Item '{item_name}' added to drive {drive_id}!")
    except Exception as e:
        print(f"Error: {e}")


@driver_cli.command(
    "view-drive-items",
    help="Views items in a drive, do view-drive-items <driver_username> <drive_id>",
)
@click.argument("driver_username")
@click.argument("drive_id")
def view_drive_items_command(driver_username, drive_id):
    try:
        items = get_drive_items(drive_id)
        print(f"Items for drive {drive_id}: {items}")
    except Exception as e:
        print(f"Error: {e}")


app.cli.add_command(driver_cli)

"""
Resident Commands
"""

resident_cli = AppGroup("resident", help="Resident object commands")


@resident_cli.command(
    "request-stop",
    help="Requests a stop, do request-stop <resident_username> <drive_id> <message>",
)
@click.argument("resident_username")
@click.argument("drive_id")
@click.argument("message")
def request_stop_command(resident_username, drive_id, message):
    try:
        resident_id = get_resident_id(resident_username)
        stop_request = request_stop(resident_id, drive_id, message)
        print(
            f"Stop requested for resident {resident_username} on drive {drive_id} with stop ID {stop_request.id}"
        )
    except Exception as e:
        print(f"Error: {e}")


@resident_cli.command(
    "cancel-stop", help="Cancels a stop, do cancel-stop <resident_username> <stop_id>"
)
@click.argument("resident_username")
@click.argument("stop_id")
def cancel_stop_command(resident_username, stop_id):
    try:
        resident_id = get_resident_id(resident_username)
        cancel_stop(resident_id, stop_id)
        print(f"Stop cancelled for resident {resident_username}!")
    except Exception as e:
        print(f"Error: {e}")


@resident_cli.command(
    "get-driver-status-and-location",
    help="Gets a driver's status and location, do get-driver-status-and-location <driver_username>",
)
@click.argument("driver_username")
def get_driver_status_and_location_command(driver_username):
    try:
        driver_id = get_driver_id(driver_username)
        driver_status_and_location = get_driver_status_and_location(driver_id)
        print(
            f"Driver status and location for {driver_username}: {driver_status_and_location}"
        )
    except Exception as e:
        print(f"Error: {e}")


@resident_cli.command(
    "update-area-info",
    help="Updates an area, do update-area-info <resident_username> <new_area_name>",
)
@click.argument("resident_username")
@click.argument("new_area_name")
def update_area_info_command(resident_username, new_area_name):
    try:
        resident_id = get_resident_id(resident_username)
        new_area_id = get_area_id(new_area_name)
        update_area_info(resident_id, new_area_id)
        print(f"Area info updated for resident {resident_username}!")
    except Exception as e:
        print(f"Error: {e}")


@resident_cli.command(
    "update-street-info",
    help="Updates a street, do update-street-info <resident_username> <new_street_name> <new_area_name>",
)
@click.argument("resident_username")
@click.argument("new_street_name")
@click.argument("new_area_name")
def update_street_info_command(resident_username, new_street_name, new_area_name):
    try:
        resident_id = get_resident_id(resident_username)
        new_area_id = get_area_id(new_area_name)
        new_street_id = get_street_id(new_street_name, new_area_id)
        update_street_info(resident_id, new_street_id)
        print(f"Street info updated for resident {resident_username}!")
    except Exception as e:
        print(f"Error: {e}")


@resident_cli.command(
    "update-house-number",
    help="Updates a house number, do update-house-number <resident_username> <new_house_number>",
)
@click.argument("resident_username")
@click.argument("new_house_number")
def update_house_number_command(resident_username, new_house_number):
    try:
        resident_id = get_resident_id(resident_username)
        update_house_number(resident_id, new_house_number)
        print(f"House number updated for resident {resident_username}!")
    except Exception as e:
        print(f"Error: {e}")


@resident_cli.command(
    "get-requested-stops",
    help="Gets requested stops, do get-requested-stops <resident_username>",
)
@click.argument("resident_username")
def get_requested_stops_command(resident_username):
    try:
        resident_id = get_resident_id(resident_username)
        stops = get_requested_stops(resident_id)
        print(f"Requested stops for resident {resident_username}: {stops}")
    except Exception as e:
        print(f"Error: {e}")


@resident_cli.command(
    "get-notifications",
    help="Gets notifications for a resident, do get-notifications <resident_username>",
)
@click.argument("resident_username")
def get_notifications_command(resident_username):
    try:
        resident_id = get_resident_id(resident_username)
        notifications = get_notification_history(resident_id)
        notifications = get_notification_history(resident_id)
        if not notifications:
            print(f"No notifications found for resident {resident_username}")
            return

        print(f"Notifications for resident {resident_username}:")
        print("-" * 50)
        for notification in notifications:
            status = "Read" if notification.get("is_read") else "Unread"
            print(f"ID: {notification.get('id')}")
            print(f"Time: {notification.get('timestamp')}")
            print(f"Status: {status}")
            print(f"Message: {notification.get('message')}")
            print("-" * 50)
    except Exception as e:
        print(f"Error: {e}")


@resident_cli.command(
    "read-notification",
    help="Marks a notification as read, do read-notification <resident_username> <notification_id>",
)
@click.argument("resident_username")
@click.argument("notification_id")
def read_notification_command(resident_username, notification_id):
    try:
        resident_id = get_resident_id(resident_username)
        mark_notification_as_read(notification_id, resident_id)
        print(f"Notification {notification_id} marked as read!")
    except Exception as e:
        print(f"Error: {e}")


app.cli.add_command(resident_cli)


"""
Test Commands
"""

test = AppGroup("test", help="Testing commands")


@test.command("all", help="Run all tests")
def all_tests_command():
    sys.exit(pytest.main([]))


@test.command("unit", help="Run Unit tests")
def unit_tests_command():
    sys.exit(pytest.main(["App/tests/unit"]))


@test.command("int", help="Run Integration tests")
def int_tests_command():
    sys.exit(pytest.main(["App/tests/integration"]))


app.cli.add_command(test)

"""
Item Commands
"""

item_cli = AppGroup("item", help="Item object commands")


@item_cli.command(
    "create-item",
    help="Creates an item, do create-item <name> <price> <description> <tags>",
)
@click.argument("name")
@click.argument("price", type=float)
@click.argument("description")
@click.argument("tags")
def create_item_command(name, price, description, tags):
    try:
        import json

        tags_list = json.loads(tags)
        create_item(name, price, description, tags_list)
        print(f"Item {name} created!")
    except Exception as e:
        print(f"Error: {e}")


@item_cli.command("list-items", help="Lists all items")
@click.argument("format", default="string")
def list_items_command(format):
    try:
        if format == "string":
            print(get_all_items())
        else:
            print(get_all_items_json())
    except Exception as e:
        print(f"Error: {e}")


@item_cli.command(
    "update-item",
    help="Updates an item, do update-item <item_id> <name> <price> <description> <tags>",
)
@click.argument("item_id")
@click.argument("name", required=False)
@click.argument("price", type=float, required=False)
@click.argument("description", required=False)
@click.argument("tags", required=False)
def update_item_command(item_id, name, price, description, tags):
    try:
        import json

        tags_list = json.loads(tags) if tags else None
        update_item(item_id, name, price, description, tags_list)
        print(f"Item {item_id} updated!")
    except Exception as e:
        print(f"Error: {e}")


@item_cli.command("delete-item", help="Deletes an item, do delete-item <item_id>")
@click.argument("item_id")
def delete_item_command(item_id):
    try:
        delete_item(item_id)
        print(f"Item {item_id} deleted!")
    except Exception as e:
        print(f"Error: {e}")


app.cli.add_command(item_cli)
