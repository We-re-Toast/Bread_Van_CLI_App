import pytest
from App.controllers.subscription import subscribe_to_street, unsubscribe_from_street, view_subscriptions
from App.models import Subscription

def test_subscribe_to_street(db_session, resident_user, street):
    # Act
    sub = subscribe_to_street(resident_user.id, street.id)

    # Assert
    assert sub.resident_id == resident_user.id
    assert sub.street_id == street.id
    assert sub.id is not None
    assert Subscription.query.get(sub.id) is not None

def test_subscribe_to_street_duplicate(db_session, resident_user, street):
    # Arrange
    subscribe_to_street(resident_user.id, street.id)

    # Act
    sub = subscribe_to_street(resident_user.id, street.id)

    # Assert
    assert sub is not None # Should return existing
    assert Subscription.query.filter_by(resident_id=resident_user.id, street_id=street.id).count() == 1

def test_unsubscribe_from_street(db_session, resident_user, street):
    # Arrange
    subscribe_to_street(resident_user.id, street.id)

    # Act
    result = unsubscribe_from_street(resident_user.id, street.id)

    # Assert
    assert result is True
    assert Subscription.query.filter_by(resident_id=resident_user.id, street_id=street.id).first() is None

def test_view_subscriptions(db_session, resident_user, street):
    # Arrange
    subscribe_to_street(resident_user.id, street.id)

    # Act
    subs = view_subscriptions(resident_user.id)

    # Assert
    assert len(subs) == 1
    assert subs[0].street_id == street.id
