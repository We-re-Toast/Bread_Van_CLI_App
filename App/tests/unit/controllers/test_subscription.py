import pytest
from App.controllers.subscription import subscribe_to_street, unsubscribe_from_street
from App.exceptions import ResourceNotFound

def test_subscribe_to_street_new(mocker):
    # Arrange
    resident_id = 1
    street_id = 1
    
    MockSubscription = mocker.patch("App.controllers.subscription.Subscription")
    mock_session = mocker.patch("App.controllers.subscription.db.session")
    
    MockSubscription.query.filter_by.return_value.first.return_value = None

    # Act
    subscribe_to_street(resident_id, street_id)

    # Assert
    MockSubscription.assert_called_once_with(resident_id=resident_id, street_id=street_id)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_subscribe_to_street_existing(mocker):
    # Arrange
    resident_id = 1
    street_id = 1
    mock_existing = mocker.Mock()
    
    MockSubscription = mocker.patch("App.controllers.subscription.Subscription")
    mock_session = mocker.patch("App.controllers.subscription.db.session")
    
    MockSubscription.query.filter_by.return_value.first.return_value = mock_existing

    # Act
    result = subscribe_to_street(resident_id, street_id)

    # Assert
    assert result == mock_existing
    mock_session.add.assert_not_called()

def test_unsubscribe_from_street_success(mocker):
    # Arrange
    resident_id = 1
    street_id = 1
    mock_sub = mocker.Mock()
    
    MockSubscription = mocker.patch("App.controllers.subscription.Subscription")
    mock_session = mocker.patch("App.controllers.subscription.db.session")
    
    MockSubscription.query.filter_by.return_value.first.return_value = mock_sub

    # Act
    result = unsubscribe_from_street(resident_id, street_id)

    # Assert
    assert result is True
    mock_session.delete.assert_called_once_with(mock_sub)
    mock_session.commit.assert_called_once()
