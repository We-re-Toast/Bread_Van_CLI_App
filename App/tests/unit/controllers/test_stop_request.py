import pytest
from App.controllers.stop_request import request_stop, cancel_stop
from App.exceptions import ResourceNotFound, ValidationError

def test_request_stop_success(mocker):
    # Arrange
    resident_id = 1
    drive_id = 1
    message = "Stop here"
    street_id = 10
    
    mock_resident = mocker.Mock()
    mock_resident.id = resident_id
    mock_resident.street_id = street_id
    
    mock_drive = mocker.Mock()
    mock_drive.id = drive_id
    mock_drive.street_id = street_id # Same street

    MockResident = mocker.patch("App.controllers.stop_request.Resident")
    MockDrive = mocker.patch("App.controllers.stop_request.Drive")
    MockStopRequest = mocker.patch("App.controllers.stop_request.StopRequest")
    mock_session = mocker.patch("App.controllers.stop_request.db.session")

    MockResident.query.get.return_value = mock_resident
    MockDrive.query.get.return_value = mock_drive

    # Act
    request_stop(resident_id, drive_id, message)

    # Assert
    MockStopRequest.assert_called_once_with(resident_id=resident_id, drive_id=drive_id, message=message)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_request_stop_wrong_street(mocker):
    # Arrange
    resident_id = 1
    drive_id = 1
    
    mock_resident = mocker.Mock()
    mock_resident.street_id = 10
    
    mock_drive = mocker.Mock()
    mock_drive.street_id = 20 # Different street

    MockResident = mocker.patch("App.controllers.stop_request.Resident")
    MockDrive = mocker.patch("App.controllers.stop_request.Drive")
    
    MockResident.query.get.return_value = mock_resident
    MockDrive.query.get.return_value = mock_drive

    # Act & Assert
    with pytest.raises(ValidationError):
        request_stop(resident_id, drive_id, "msg")

def test_cancel_stop_success(mocker):
    # Arrange
    stop_id = 1
    resident_id = 1
    mock_stop = mocker.Mock()
    mock_stop.resident_id = resident_id

    MockStopRequest = mocker.patch("App.controllers.stop_request.StopRequest")
    mock_session = mocker.patch("App.controllers.stop_request.db.session")
    
    MockStopRequest.query.get.return_value = mock_stop

    # Act
    result = cancel_stop(stop_id, resident_id)

    # Assert
    assert result is True
    mock_session.delete.assert_called_once_with(mock_stop)
    mock_session.commit.assert_called_once()
