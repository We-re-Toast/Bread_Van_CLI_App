import pytest
from App.controllers.driver import update_driver_status
from App.controllers.drive import (
    schedule_drive,
    view_drives,
    start_drive,
    complete_drive,
)
from App.models.enums import DriveStatus, DriverStatus
from App.exceptions import ResourceNotFound, DuplicateEntity, ValidationError


def test_schedule_drive(db_session, driver_user, area, street):
    # Arrange
    date = "2030-01-01"
    time = "10:00"
    # Act
    drive = schedule_drive(
        driver_user.id, area.id, street.id, date, time, DriveStatus.SCHEDULED
    )

    # Assert
    assert drive.driver_id == driver_user.id
    assert drive.status == DriveStatus.SCHEDULED
    assert drive.id is not None


def test_schedule_drive_past_date(db_session, driver_user, area, street):
    # Arrange
    date = "2020-01-01"
    time = "10:00"
    # Act & Assert
    with pytest.raises(ValidationError):
        schedule_drive(
            driver_user.id, area.id, street.id, date, time, DriveStatus.SCHEDULED
        )


def test_view_drives(db_session, driver_user, area, street):
    # Arrange
    schedule_drive(
        driver_user.id, area.id, street.id, "2030-01-01", "10:00", DriveStatus.SCHEDULED
    )

    # Act
    drives = view_drives(driver_user.id)

    # Assert
    assert len(drives) == 1


def test_start_drive(db_session, driver_user, area, street):
    # Arrange
    drive = schedule_drive(
        driver_user.id, area.id, street.id, "2030-01-01", "10:00", DriveStatus.SCHEDULED
    )

    # Act
    updated_drive = start_drive(driver_user.id, drive.id)

    # Assert
    assert updated_drive.status == DriveStatus.IN_PROGRESS


def test_complete_drive(db_session, driver_user, area, street):
    # Arrange
    drive = schedule_drive(
        driver_user.id, area.id, street.id, "2030-01-01", "10:00", DriveStatus.SCHEDULED
    )

    # Act
    updated_drive = complete_drive(driver_user.id, drive.id)

    # Assert
    assert updated_drive.status == DriveStatus.COMPLETED


def test_update_driver_status(db_session, driver_user):
    # Arrange
    status = DriverStatus.ON_DUTY

    # Act
    updated_driver = update_driver_status(driver_user.id, status)

    # Assert
    assert updated_driver.status == status
