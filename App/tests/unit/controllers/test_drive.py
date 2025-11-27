import pytest
from datetime import datetime, date, time
from App.controllers.drive import schedule_drive, start_drive, complete_drive
from App.models.enums import DriveStatus
from App.exceptions import ResourceNotFound, ValidationError, DuplicateEntity

@pytest.mark.parametrize("date_str, time_str", [
    ("2030-01-01", "10:00"),
    ("2030-12-31", "23:59")
])
def test_schedule_drive_success(mocker, date_str, time_str):
    # Arrange
    driver_id = 1
    area_id = 1
    street_id = 1
    status = DriveStatus.SCHEDULED
    
    mock_driver = mocker.Mock()
    mock_driver.id = driver_id
    
    mock_street = mocker.Mock()
    mock_street.id = street_id
    mock_street.name = "Test Street"

    MockDriver = mocker.patch("App.controllers.drive.Driver")
    MockStreet = mocker.patch("App.controllers.drive.Street")
    MockDrive = mocker.patch("App.controllers.drive.Drive")
    mock_session = mocker.patch("App.controllers.drive.db.session")
    mock_notify = mocker.patch("App.controllers.drive.notify_subscribers")
    
    MockDriver.query.get.return_value = mock_driver
    MockStreet.query.filter_by.return_value.first.return_value = mock_street
    MockDrive.query.filter_by.return_value.first.return_value = None # No existing drive

    # Act
    result = schedule_drive(driver_id, area_id, street_id, date_str, time_str, status)

    # Assert
    # Verify Drive constructor was called with correct arguments
    MockDrive.assert_called_once()
    call_args = MockDrive.call_args[1] # kwargs
    assert call_args['driver_id'] == driver_id
    assert call_args['status'] == status
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_notify.assert_called_once()

def test_schedule_drive_past_date(mocker):
    # Arrange
    driver_id = 1
    area_id = 1
    street_id = 1
    date_str = "2020-01-01"
    time_str = "10:00"
    status = DriveStatus.SCHEDULED

    MockDriver = mocker.patch("App.controllers.drive.Driver")
    MockStreet = mocker.patch("App.controllers.drive.Street")
    
    MockDriver.query.get.return_value = mocker.Mock()
    MockStreet.query.filter_by.return_value.first.return_value = mocker.Mock()

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        schedule_drive(driver_id, area_id, street_id, date_str, time_str, status)
    
    assert "Cannot schedule a drive in the past" in str(exc_info.value)

def test_start_drive_success(mocker):
    # Arrange
    driver_id = 1
    drive_id = 1
    mock_drive = mocker.Mock()
    mock_drive.id = drive_id
    mock_drive.status = DriveStatus.SCHEDULED

    MockDrive = mocker.patch("App.controllers.drive.Drive")
    mock_session = mocker.patch("App.controllers.drive.db.session")
    
    MockDrive.query.filter_by.return_value.first.return_value = mock_drive

    # Act
    result = start_drive(driver_id, drive_id)

    # Assert
    assert result.status == DriveStatus.IN_PROGRESS
    mock_session.commit.assert_called_once()

def test_start_drive_not_found(mocker):
    # Arrange
    driver_id = 1
    drive_id = 1

    MockDrive = mocker.patch("App.controllers.drive.Drive")
    MockDrive.query.filter_by.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(ResourceNotFound):
        start_drive(driver_id, drive_id)
