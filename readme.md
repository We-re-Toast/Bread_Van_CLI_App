# 🍞 Bread Van App CLI
This project provides a command-line interface (CLI) for managing and interacting with the Bread Van App.
 It is built with Flask CLI and click, and supports multiple roles: Admin, Driver, and Resident.

## 🚀 Setup
### Install dependencies:
```bash
$ pip install -r requirements.txt
```

### Initialize the database:
```bash
flask init
```
This creates and initializes all tables.

### Run any CLI command using:
```bash
flask <group> <command> [args...]
```


👤 User Commands
Group: flask user
Login

 flask user login <username> <password>


Logout

 flask user logout


View Drives on a Street

 flask user view_street_drives
 Prompts to select an area and street, then lists scheduled drives.



🛠️ Admin Commands
Group: flask admin
Admins manage drivers, areas, and streets.
List Users

 flask admin list [string|json]


Create Driver

 flask admin create_driver <username> <password>


Delete Driver

 flask admin delete_driver <driver_id>


Add Area

 flask admin add_area <name>


Add Street

 flask admin add_street <area_id> <name>


Delete Area

 flask admin delete_area <area_id>


Delete Street

 flask admin delete_street <street_id>


View All Areas

 flask admin view_all_areas


View All Streets

 flask admin view_all_streets



🚐 Driver Commands
Group: flask driver
Drivers manage drives and stops.
Schedule Drive

 flask driver schedule_drive YYYY-MM-DD HH:MM
 Prompts to select area & street.


Cancel Drive

 flask driver cancel_drive <drive_id>


View My Drives

 flask driver view_my_drives


Start Drive

 flask driver start_drive <drive_id>


End Drive

 flask driver end_drive


View Requested Stops

 flask driver view_requested_stops <drive_id>



🏠 Resident Commands
Group: flask resident
Residents can create accounts, request stops, and view their inbox.
Create Resident

 flask resident create <username> <password>
 Prompts for area, street, and house number.


Request Stop

 flask resident request_stop


Cancel Stop

 flask resident cancel_stop <drive_id>


View Inbox

 flask resident view_inbox


View Driver Stats

 flask resident view_driver_stats <driver_id>



🔑 Role Requirements
flask admin ... → must be logged in as Admin


flask driver ... → must be logged in as Driver


flask resident ... → must be logged in as Resident


General user commands (login/logout/view_street_drives) are available to all.
If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
