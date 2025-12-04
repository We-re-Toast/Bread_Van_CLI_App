from App.models import StopRequest, Drive, Resident
from App.database import db
from App.exceptions import ResourceNotFound, ValidationError


def request_stop(resident_id, drive_id, message):
    resident = Resident.query.get(resident_id)
    if not resident:
        raise ResourceNotFound("Resident not found")

    drive = Drive.query.get(drive_id)
    if not drive:
        raise ResourceNotFound("Drive not found")

    if drive.street_id != resident.street_id:
        raise ValidationError("You can only request stops for drives on your street")

    new_stop_request = StopRequest(
        resident_id=resident.id, drive_id=drive.id, message=message
    )
    db.session.add(new_stop_request)
    db.session.commit()
    return new_stop_request


def cancel_stop(stop_request_id, resident_id):
    stop_request = StopRequest.query.get(stop_request_id)
    if not stop_request:
        raise ResourceNotFound("Stop request not found")

    if stop_request.resident_id != resident_id:
        raise ValidationError("You can only cancel your own stop requests")

    db.session.delete(stop_request)
    db.session.commit()
    return True


def get_requested_stops(resident_id):
    stops = StopRequest.query.filter_by(resident_id=resident_id).all()
    if not stops:
        raise ResourceNotFound("No stop requests found")
    return stops
