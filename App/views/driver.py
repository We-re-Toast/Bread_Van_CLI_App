from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers.drive import (
    schedule_drive,
    get_all_drives,
    update_drive,
    view_drives,
    start_drive,
    complete_drive
)
from App.controllers.driver import update_driver_status
from App.models import Drive
from App.exceptions import ResourceNotFound, ValidationError

drive_views = Blueprint("drive_views", __name__, template_folder="../templates")


@drive_views.route("/api/driver/schedule-drive", methods=["POST"])
@jwt_required()
def create_drive_api():
    if current_user.role != "driver":
        return jsonify(error="Unauthorized"), 403

    data = request.json
    try:
        drive = schedule_drive(
            driver_id=current_user.id,
            area_id=data["area_id"],
            street_id=data["street_id"],
            date_str=data["date"],
            time_str=data["time"],
            status="Scheduled",
        )
        return jsonify(drive.get_json()), 201
    except ValidationError as e:
        return jsonify(error=str(e)), 400


@drive_views.route("/api/driver/drives", methods=["GET"])
@jwt_required()
def get_drives_api():
    if current_user.role == "driver":
        try:
            drives = view_drives(current_user.id)
            return jsonify([drive.get_json() for drive in drives])
        except ResourceNotFound as e:
            return jsonify(error=str(e)), 404
    return jsonify(error="Unauthorized"), 403


@drive_views.route("/api/driver/drives/<int:drive_id>/start", methods=["PUT"])
@jwt_required()
def start_drive_api(drive_id):
    if current_user.role != "driver":
        return jsonify(error="Unauthorized"), 403
    try:
        drive = start_drive(current_user.id, drive_id)
        return jsonify(drive.get_json()), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404


@drive_views.route("/api/driver/drives/<int:drive_id>/complete", methods=["PUT"])
@jwt_required()
def complete_drive_api(drive_id):
    if current_user.role != "driver":
        return jsonify(error="Unauthorized"), 403
    try:
        drive = complete_drive(current_user.id, drive_id)
        return jsonify(drive.get_json()), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404


@drive_views.route("/api/driver/status", methods=["PUT"])
@jwt_required()
def update_status_api():
    if current_user.role != "driver":
        return jsonify(error="Unauthorized"), 403
    data = request.json
    try:
        driver = update_driver_status(current_user.id, data["status"])
        return jsonify(message="Status updated", status=driver.status)
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404