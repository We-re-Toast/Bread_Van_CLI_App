import pytest
from App.controllers.driver import update_driver_status
from App.models.enums import DriverStatus
from App.exceptions import ResourceNotFound

@pytest.mark.parametrize("status", [
    DriverStatus.ON_DUTY,
    DriverStatus.OFF_DUTY,
    "On Duty",
    "Off Duty"
])
def test_update_driver_status_success(mocker, status):
    # Arrange
    driver_id = 1
    mock_driver = mocker.Mock()
    mock_driver.id = driver_id
    mock_driver.status = DriverStatus.OFF_DUTY

    MockDriver = mocker.patch("App.controllers.driver.Driver")
    mock_session = mocker.patch("App.controllers.driver.db.session")
    
    MockDriver.query.get.return_value = mock_driver

    # Act
    result = update_driver_status(driver_id, status)

    # Assert
    assert result.status == status
    MockDriver.query.get.assert_called_once_with(driver_id)
    mock_session.commit.assert_called_once()

def test_update_driver_status_driver_not_found(mocker):
    # Arrange
    driver_id = 999
    status = DriverStatus.ON_DUTY

    MockDriver = mocker.patch("App.controllers.driver.Driver")
    MockDriver.query.get.return_value = None

    # Act & Assert
    with pytest.raises(ResourceNotFound) as exc_info:
        update_driver_status(driver_id, status)
    
    assert str(exc_info.value) == f"Driver with ID '{driver_id}' does not exist"
    MockDriver.query.get.assert_called_once_with(driver_id)
