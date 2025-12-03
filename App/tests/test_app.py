import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, time, datetime, timedelta

from App.main import create_app
from App.database import db, create_db
from App.models import User, Resident, Driver, Admin, Area, Street, Drive, Stop, Item, DriverStock
from App.controllers import *


LOGGER = logging.getLogger(__name__)


def future(days=1): # helper function to get a date string days in the future
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

#'''
#   Unit Tests
#'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_user_getJSON(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='pbkdf2:sha256')
        newuser = User("bob", password)
        assert newuser.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class ResidentUnitTests(unittest.TestCase):

    def test_new_resident(self):
        resident = Resident("john", "johnpass", 1, 2, 123)
        assert resident.username == "john"
        assert resident.password != "johnpass"
        assert resident.areaId == 1
        assert resident.streetId == 2
        assert resident.houseNumber == 123
        assert resident.inbox == []

    def test_resident_type(self):
        resident = Resident("john", "johnpass", 1, 2, 123)
        assert resident.type == "Resident"

    def test_resident_getJSON(self):
        resident = Resident("john", "johnpass", 1, 2, 123)
        resident_json = resident.get_json()
        self.assertDictEqual(resident_json, {"id":None, "username":"john", "areaId":1, "streetId":2, "houseNumber":123, "inbox":[]})

    def test_receive_notif(self):
        resident = Resident("john", "johnpass", 1, 2, 123)
        resident.receive_notif("New msg")
        assert resident.inbox[-1].endswith("New msg")
        assert resident.inbox[-1].startswith("[")

    def test_view_inbox(self):
        resident = Resident("john", "johnpass", 1, 2, 123)
        resident.receive_notif("msg1")
        resident.receive_notif("msg2")
        assert len(resident.inbox) == 2
        assert resident.inbox[0].endswith("msg1")
        assert resident.inbox[1].endswith("msg2")
        assert resident.inbox[0].startswith("[")
        assert resident.inbox[1].startswith("[")

    def test_subscribe(self):         # verify subscribe method adds driver id and prevents duplicates

        resident = Resident("jane", "janepass", 1, 2, 10)

        if resident.subscriptions is None:
            resident.subscriptions = []

        assert resident.subscriptions == []

        # subscribe to driver id 42
        resident.subscribe(42)
        assert 42 in resident.subscriptions

        # subscribing again should not create duplicates
        resident.subscribe(42)
        assert resident.subscriptions.count(42) == 1

    def test_unsubscribe(self):
        # verify unsubscribe removes a previously subscribed id
        resident = Resident("jane", "janepass", 1, 2, 10)
        if resident.subscriptions is None:
            resident.subscriptions = []

        resident.subscribe(77)
        assert 77 in resident.subscriptions

        resident.unsubscribe(77)
        assert 77 not in resident.subscriptions
        assert resident.subscriptions == []

    def test_unsubscribe_nonexistent_is_noop(self):
        # unsubscribing an id that isn't present should be a no-op
        resident = Resident("mark", "markpass", 1, 2, 5)
        if resident.subscriptions is None:
            resident.subscriptions = []
        # this should not raise and should leave subscriptions empty
        resident.unsubscribe(9999)
        assert resident.subscriptions == []
        
class DriverUnitTests(unittest.TestCase):

    def test_new_driver(self):
        driver = Driver("steve", "stevepass", "Busy", 2, 12)
        assert driver.username == "steve"
        assert driver.password != "stevepass"
        assert driver.status == "Busy"
        assert driver.areaId == 2
        assert driver.streetId == 12
        
    def test_driver_type(self):
        driver = Driver("steve", "stevepass", "Busy", 2, 12)
        assert driver.type == "Driver"

    def test_driver_getJSON(self):
        driver = Driver("steve", "stevepass", "Busy", 2, 12)
        driver_json = driver.get_json()
        self.assertDictEqual(driver_json, {"id":None, "username":"steve", "status":"Busy", "areaId":2, "streetId":12})

class AdminUnitTests(unittest.TestCase):

    def test_new_admin(self):
        admin = Admin("admin", "adminpass")
        assert admin.username == "admin"
        assert admin.password != "adminpass"

    def test_admin_type(self):
        admin = Admin("admin", "adminpass")
        assert admin.type == "Admin"

    def test_admin_getJSON(self):
        admin = Admin("admin", "adminpass")
        admin_json = admin.get_json()
        self.assertDictEqual(admin_json, {"id":None, "username":"admin"})

class AreaUnitTests(unittest.TestCase):

    def test_new_area(self):
        area = Area("Sangre Grande")
        assert area.name == "Sangre Grande"

    def test_area_getJSON(self):
        area = Area("Sangre Grande")
        area_json = area.get_json()
        self.assertDictEqual(area_json, {"id":None, "name":"Sangre Grande"})

class StreetUnitTests(unittest.TestCase):

    def test_new_street(self):
        street = Street("Picton Road", 8)
        assert street.name == "Picton Road"
        assert street.areaId == 8

    def test_street_getJSON(self):
        street = Street("Picton Road", 8)
        street_json = street.get_json()
        self.assertDictEqual(street_json, {"id":None, "name":"Picton Road", "areaId":8})

class DriveUnitTests(unittest.TestCase):

    def test_new_drive(self):
        drive = Drive(78, 2, 12, date(2025, 11, 8), time(11, 30), "Upcoming")
        assert drive.driverId == 78
        assert drive.areaId == 2
        assert drive.streetId == 12
        assert drive.date == date(2025, 11, 8)
        assert drive.time == time(11, 30)
        assert drive.status == "Upcoming"

    def test_drive_getJSON(self):
        drive = Drive(78, 2, 12, date(2025, 11, 8), time(11, 30), "Upcoming")
        drive_json = drive.get_json()
        self.assertDictEqual(drive_json, {"id":None, "driverId":78, "areaId":2, "streetId":12, "date":"2025-11-08", "time":"11:30:00", "status":"Upcoming"})

class StopUnitTests(unittest.TestCase):

    def test_new_stop(self):
        stop = Stop(1, 2)
        assert stop.driveId == 1
        assert stop.residentId == 2

    def test_stop_getJSON(self):
        stop = Stop(1, 2)
        stop_json = stop.get_json()
        self.assertDictEqual(stop_json, {"id":None, "driveId":1, "residentId":2})

class ItemUnitTests(unittest.TestCase):

    def test_new_item(self):
        item = Item("Whole-Grain Bread", 19.50, "Healthy whole-grain loaf", ["whole-grain", "healthy"])
        assert item.name == "Whole-Grain Bread"
        assert item.price == 19.50
        assert item.description == "Healthy whole-grain loaf"
        assert item.tags == ["whole-grain", "healthy"]

    def test_item_getJSON(self):
        item = Item("Whole-Grain Bread", 19.50, "Healthy whole-grain loaf", ["whole-grain", "healthy"])
        item_json = item.get_json()
        self.assertDictEqual(item_json, {"id":None, "name":"Whole-Grain Bread", "price":19.50, "description":"Healthy whole-grain loaf", "tags":["whole-grain", "healthy"]})

class DriverStockUnitTests(unittest.TestCase):

    def test_new_driverStock(self):
        driverStock = DriverStock(1, 2, 30)
        assert driverStock.driverId == 1
        assert driverStock.itemId == 2
        assert driverStock.quantity == 30

    def test_driverStock_getJSON(self):
        driverStock = DriverStock(1, 2, 30)
        driverStock_json = driverStock.get_json()
        self.assertDictEqual(driverStock_json, {"id":None, "driverId":1, "itemId":2, "quantity":30})
        

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    db.create_all()    
    yield app.test_client()
    db.drop_all()


class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "ronniepass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        create_user("bob", "bobpass")
        create_user("rick", "ronniepass")
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        create_user("rick", "ronniepass")
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    def test_login(self):
        create_user("ronnie", "ronniepass")
        user = user_login("ronnie", "ronniepass")
        assert user.username == "ronnie"

    def test_logout(self):
        create_user("ronnie", "ronniepass")
        user = user_login("ronnie", "ronniepass")
        user_logout(user)
        assert user.logged_in == False
        if isinstance(user, Driver):
            updated_user = get_user(user.id)
            assert updated_user.status == "Offline"


class ResidentsIntegrationTests(unittest.TestCase):
    
    def setUp(self):
        self.area = admin_add_area("St. Augustine")
        self.street = admin_add_street(self.area.id, "Warner Street")
        self.driver = admin_create_driver("driver1", "pass")
        self.resident = resident_create("john", "johnpass", self.area.id, self.street.id, 123)
        self.drive = driver_schedule_drive(self.driver, self.area.id, self.street.id, future(1), "11:30")
        self.item = admin_add_item("Whole-Grain Bread", 19.50, "Healthy whole-grain loaf", ["whole-grain", "healthy"])


    def test_request_stop(self):
        stop = resident_request_stop(self.resident, self.drive.id)
        self.assertIsNotNone(stop)

    def test_cancel_stop(self):
        stop = resident_request_stop(self.resident, self.drive.id)
        resident_cancel_stop(self.resident, stop.id)
        self.assertIsNone(Stop.query.filter_by(id=stop.id).first())

    def test_view_driver_stats(self):
        driver = resident_view_driver_stats(self.resident, self.driver.id)
        self.assertIsNotNone(driver)

    def test_view_stock(self):
        driver_update_stock(self.driver, self.item.id, 30)
        stock = resident_view_stock(self.resident, self.driver.id)
        self.assertIsNotNone(stock)


class DriversIntegrationTests(unittest.TestCase):
                
    def setUp(self):
        self.area = admin_add_area("St. Augustine")
        self.street = admin_add_street(self.area.id, "Warner Street")
        self.driver = admin_create_driver("driver1", "pass")
        self.resident = resident_create("john", "johnpass", self.area.id, self.street.id, 123)
        self.drive = driver_schedule_drive(self.driver, self.area.id, self.street.id, future(1), "11:30")
        self.stop = resident_request_stop(self.resident, self.drive.id)
        self.item = admin_add_item("Whole-Grain Bread", 19.50, "Healthy whole-grain loaf", ["whole-grain", "healthy"])

    def test_schedule_drive(self):
        drive = driver_schedule_drive(self.driver, self.area.id, self.street.id, future(7), "09:00")
        self.assertIsNotNone(drive)

    def test_cancel_drive(self):
        drive = driver_schedule_drive(self.driver, self.area.id, self.street.id, future(8), "08:15")
        driver_cancel_drive(self.driver, drive.id)
        assert drive.status == "Cancelled"

    def test_view_drives(self):
        drives = driver_view_drives(self.driver)
        self.assertIsNotNone(drives)

    def test_start_drive(self):
        driver_start_drive(self.driver, self.drive.id)
        drive = Drive.query.filter_by(id=self.drive.id).first()
        assert self.drive.status == "In Progress"
        assert self.driver.status == "Busy"

    def test_end_drive(self):
        driver_start_drive(self.driver, self.drive.id)
        driver_end_drive(self.driver)
        drive = Drive.query.filter_by(id=self.drive.id).first()
        assert self.drive.status == "Completed"
        assert self.driver.status == "Available"

    def test_view_requested_stops(self):
        stops = driver_view_requested_stops(self.driver, self.drive.id)
        self.assertIsNotNone(stops)
    
    def test_update_stock(self):
        newquantity = 30
        driver_update_stock(self.driver, self.item.id, newquantity)
        stock = DriverStock.query.filter_by(driverId=self.driver.id, itemId=self.item.id).first()
        assert stock.quantity == newquantity

    def test_view_stock(self):
        stock = driver_view_stock(self.driver)
        self.assertIsNotNone(stock)


class AdminsIntegrationTests(unittest.TestCase):
    
    def test_create_driver(self):
        driver = admin_create_driver("driver1", "driverpass")
        assert Driver.query.filter_by(id=driver.id).first() != None

    def test_delete_driver(self):
        driver = admin_create_driver("driver1", "driverpass")
        admin_delete_driver(driver.id)
        assert Driver.query.filter_by(id=driver.id).first() == None

    def test_add_area(self):
        area = admin_add_area("Port-of-Spain")
        assert Area.query.filter_by(id=area.id).first() != None

    def test_delete_area(self):
        area = admin_add_area("Port-of-Spain")
        admin_delete_area(area.id)
        assert Area.query.filter_by(id=area.id).first() == None

    def test_view_all_areas(self):
        admin_add_area("Port-of-Spain")
        admin_add_area("Arima")
        admin_add_area("San Fernando")
        areas = admin_view_all_areas()
        assert areas != None
        assert len(areas) == 3

    def test_add_street(self):
        area = admin_add_area("Port-of-Spain")
        street = admin_add_street(area.id, "Fredrick Street")
        assert Street.query.filter_by(id=street.id).first() != None

    def test_delete_street(self):
        area = admin_add_area("Port-of-Spain")
        street = admin_add_street(area.id, "Fredrick Street")
        admin_delete_street(street.id)
        assert Street.query.filter_by(id=street.id).first() == None

    def test_view_all_streets(self):
        area = admin_add_area("Port-of-Spain")
        admin_add_street(area.id, "Fredrick Street")
        admin_add_street(area.id, "Warner Street")
        admin_add_street(area.id, "St. Vincent Street")
        streets = admin_view_all_streets()
        assert streets != None
        assert len(streets) == 3

    def test_add_item(self):
        item = admin_add_item("Whole-Grain Bread", 19.50, "Healthy whole-grain loaf", ["whole-grain", "healthy"])
        assert Item.query.filter_by(id=item.id).first() != None

    def test_delete_item(self):
        item = admin_add_item("Whole-Grain Bread", 19.50, "Healthy whole-grain loaf", ["whole-grain", "healthy"])
        admin_delete_item(item.id)
        assert Item.query.filter_by(id=item.id).first() == None

    def test_view_all_items(self):
        admin_add_item("Whole-Grain Bread", 19.50, "Healthy whole-grain loaf", ["whole-grain", "healthy"])
        admin_add_item("White Milk Bread", 12.00, "Soft and fluffy white milk bread", ["white", "soft"])
        admin_add_item("Whole-Wheat Bread", 15.00, "Nutritious whole-wheat bread", ["whole-wheat", "nutritious"])
        items = admin_view_all_items()
        assert items != None
        assert len(items) == 3
        

class ResidentInvalidTests(unittest.TestCase):
    def setUp(self):
        self.area = admin_add_area("TestArea")
        self.street = admin_add_street(self.area.id, "TestStreet")
        self.resident = Resident("testUser", "pass", self.area.id, self.street.id, 12)
        db.session.add(self.resident)
        db.session.commit()

    # ========== SUBSCRIBE INVALID ==========
    def test_subscribe_invalid_value(self):
        self.resident.subscribe(None)
        self.assertIn(None, self.resident.subscriptions)  # current behavior: it stores None

    def test_subscribe_duplicate(self):
        self.resident.subscribe(1)
        self.resident.subscribe(1)  # duplicate subscribe should not add twice
        self.assertEqual(self.resident.subscriptions.count(1), 1)

    # ========== UNSUBSCRIBE INVALID ==========
    def test_unsubscribe_not_subscribed(self):
        # Should not break or crash
        try:
            self.resident.unsubscribe(99)  # id not in subscriptions
            success = True
        except:
            success = False
        self.assertTrue(success)

    # ========== REQUEST STOP INVALID ==========
    def test_request_stop_invalid_drive(self):
        result = self.resident.request_stop(9999)  # drive doesn't exist
        self.assertIsNone(result)

    # ========== CANCEL INVALID STOP ==========
    def test_cancel_nonexistent_stop(self):
        try:
            self.resident.cancel_stop(9999)  # no crash expected
            success = True
        except:
            success = False
        self.assertTrue(success)

    # ========== VIEW DRIVER INVALID ==========
    def test_view_driver_stats_invalid_driver(self):
        result = self.resident.view_driver_stats(9999)
        self.assertIsNone(result)

    def test_inbox_max_size_limit(self):
        for i in range(25):  # exceeds max size of 20
            self.resident.receive_notif(f"msg{i}")

        self.assertEqual(len(self.resident.inbox), 20)
        self.assertTrue("msg5" in self.resident.inbox[0])  # first 5 dropped

    def test_create_resident_invalid_area(self):
        with self.assertRaises(Exception):
            Resident("new", "pass", None, self.street.id, 15)

    def test_create_resident_invalid_house_number(self):
        with self.assertRaises(Exception):
            Resident("new", "pass", self.area.id, self.street.id, "not-a-number")

    def test_view_inbox_empty(self):
        inbox = self.resident.view_inbox()
        self.assertIsInstance(inbox, list)
        self.assertEqual(len(inbox), 0)
