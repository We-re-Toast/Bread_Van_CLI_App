import pytest
from App.controllers.notification import notify_subscribers, mark_notification_as_read
from App.exceptions import ValidationError

def test_notify_subscribers(mocker):
    # Arrange
    drive = mocker.Mock()
    drive.street_id = 1
    drive.street.name = "Main St"
    drive.date = "2030-01-01"
    drive.time = "10:00"
    
    sub1 = mocker.Mock()
    sub1.resident_id = 10
    sub2 = mocker.Mock()
    sub2.resident_id = 11
    
    MockSubscription = mocker.patch("App.controllers.notification.Subscription")
    MockNotification = mocker.patch("App.controllers.notification.Notification")
    mock_session = mocker.patch("App.controllers.notification.db.session")
    
    MockSubscription.query.filter_by.return_value.all.return_value = [sub1, sub2]

    # Act
    notify_subscribers(drive)

    # Assert
    assert MockNotification.call_count == 2
    assert mock_session.add.call_count == 2
    mock_session.commit.assert_called_once()

def test_mark_notification_as_read_success(mocker):
    # Arrange
    notification_id = 1
    resident_id = 10
    mock_notif = mocker.Mock()
    mock_notif.resident_id = resident_id
    mock_notif.is_read = False
    
    MockNotification = mocker.patch("App.controllers.notification.Notification")
    mock_session = mocker.patch("App.controllers.notification.db.session")
    
    MockNotification.query.get.return_value = mock_notif

    # Act
    result = mark_notification_as_read(notification_id, resident_id)

    # Assert
    assert result is True
    assert mock_notif.is_read is True
    mock_session.commit.assert_called_once()

def test_mark_notification_as_read_unauthorized(mocker):
    # Arrange
    notification_id = 1
    resident_id = 10
    mock_notif = mocker.Mock()
    mock_notif.resident_id = 99 # Different resident
    
    MockNotification = mocker.patch("App.controllers.notification.Notification")
    
    MockNotification.query.get.return_value = mock_notif

    # Act & Assert
    with pytest.raises(ValidationError):
        mark_notification_as_read(notification_id, resident_id)
