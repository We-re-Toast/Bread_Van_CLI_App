import pytest
from App.controllers.notification import get_notification_history
from App.models import Notification
from App.models import Notification
from App.exceptions import ValidationError
from datetime import datetime


def test_get_notification_history(db_session, resident_user):
    # Arrange
    msg1 = Notification(
        resident_id=resident_user.id, message="Message 1", timestamp=datetime.now()
    )
    msg2 = Notification(
        resident_id=resident_user.id, message="Message 2", timestamp=datetime.now()
    )
    db_session.session.add(msg1)
    db_session.session.add(msg2)
    db_session.session.commit()

    # Act
    history = get_notification_history(resident_user.id)

    # Assert
    assert len(history) == 2
    assert history[0]["message"] == "Message 1"
    assert history[1]["message"] == "Message 2"


def test_mark_notification_as_read(db_session, resident_user):
    # Arrange
    from App.controllers.notification import mark_notification_as_read

    msg = Notification(
        resident_id=resident_user.id, message="Message 1", timestamp=datetime.now()
    )
    db_session.session.add(msg)
    db_session.session.commit()

    # Act
    mark_notification_as_read(msg.id, resident_user.id)

    # Assert
    updated_msg = Notification.query.get(msg.id)
    assert updated_msg.is_read is True


def test_mark_notification_as_read_unauthorized(db_session, resident_user):
    # Arrange
    from App.controllers.notification import mark_notification_as_read

    # Create another resident
    from App.controllers.resident import create_resident
    from App.controllers.area import create_area
    from App.controllers.street import create_street

    area = create_area("Other Area")
    street = create_street("Other Street", area.id)
    other_resident = create_resident("other", "pass", area.id, street.id, 1)

    msg = Notification(
        resident_id=resident_user.id, message="Message 1", timestamp=datetime.now()
    )
    db_session.session.add(msg)
    db_session.session.commit()

    # Act & Assert
    with pytest.raises(ValidationError):
        mark_notification_as_read(msg.id, other_resident.id)
