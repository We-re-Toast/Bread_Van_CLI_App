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
This creates and initializes all accounts and tables.
* Admin
  * admin / adminpass
* Drivers
  * bob / bobpass
  * mary / marypass
* Residents
  * alice / alicepass
  * jane / janepass
  * john / johnpass

### Run any CLI command using:
```bash
flask <group> <command> [args...]
```


## 👤 User Commands | Group: flask user
### Login
```bash
 flask user login <username> <password>
```

### Logout
```bash
flask user logout
```

### View Drives on a Street
```bash
flask user view_street_drives
```
Prompts to select an area and street, then lists scheduled drives.



## 🛠️ Admin Commands | Group: flask admin
Admins manage drivers, areas, and streets.
### List Users
```bash
flask admin list
```

### Create Driver
```bash
flask admin create_driver <username> <password>
```

### Delete Driver
```bash
flask admin delete_driver <driver_id>
```

### Add Area
```bash
flask admin add_area <name>
```

### Add Street
```bash
flask admin add_street <area_id> <name>
```

### Delete Area
```bash
flask admin delete_area <area_id>
```

### Delete Street
```bash
flask admin delete_street <street_id>
```

### View All Areas
```bash
flask admin view_all_areas
```

### View All Streets
```bash
flask admin view_all_streets
```


## 🚐 Driver Commands | Group: flask driver
Drivers manage drives and stops.
### Schedule Drive
```bash
flask driver schedule_drive YYYY-MM-DD HH:MM
```
Prompts to select area & street.
Drives cannot be scheduled in the past nor more than 1 year ahead of the current date.


### Cancel Drive
```bash
flask driver cancel_drive <drive_id>
```

### View My Drives
```bash
flask driver view_my_drives
```

### Start Drive
```bash
flask driver start_drive <drive_id>
```

### End Drive
```bash
flask driver end_drive
```

### View Requested Stops
```bash
flask driver view_requested_stops <drive_id>
```


## 🏠 Resident Commands | Group: flask resident
Residents can request stops and view their inbox.
### Create Resident
```bash
flask resident create <username> <password>
```
Prompts for area, street, and house number. 
A logged-in account is not required to create a resident.

### Request Stop
```bash
flask resident request_stop
```

### Cancel Stop
```bash
flask resident cancel_stop <drive_id>
```

### View Inbox
```bash
flask resident view_inbox
```

### View Driver Stats
```bash
flask resident view_driver_stats <driver_id>
```


## 🔑 Role Requirements
* flask admin ... → must be logged in as Admin
* flask driver ... → must be logged in as Driver
* flask resident ... → must be logged in as Resident


General user commands (login/logout/view_street_drives) are available to all.



New commands
flask resident list_drivers
flask resident subscribe 2
flask resident unsubscribe 2
flask resident my_subscriptions
below now wholes history
flask resident view_inbox
