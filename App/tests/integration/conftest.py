import pytest
from App.main import create_app
from App.database import db
from App.models import *


@pytest.fixture(scope="session")
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    return app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture
def admin_user(db_session):
    user = Admin("admin", "adminpass")
    db_session.session.add(user)
    db_session.session.commit()
    return user


@pytest.fixture
def driver_user(db_session):
    user = Driver("driver1", "driverpass")
    db_session.session.add(user)
    db_session.session.commit()
    return user


@pytest.fixture
def area(db_session):
    area = Area(name="Test Area")
    db_session.session.add(area)
    db_session.session.commit()
    return area


@pytest.fixture
def street(db_session, area):
    street = Street(name="Test Street", area_id=area.id)
    db_session.session.add(street)
    db_session.session.commit()
    return street


@pytest.fixture
def resident_user(db_session, area, street):
    user = Resident(
        "resident1",
        "residentpass",
        area_id=area.id,
        street_id=street.id,
        house_number=101,
    )
    db_session.session.add(user)
    db_session.session.commit()
    return user
