from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from App.api.security import role_required, current_user_id
from App.controllers import driver as driver_controller

bp = Blueprint("api_driver", __name__, url_prefix="/driver")


@bp.get("/me")
@jwt_required()
@role_required("driver")
def me():
    uid = current_user_id()
    # driver_controller should expose a way to get driver by user id; try user.get
    driver = None
    try:
        driver = driver_controller.driver_view_drives.__self__ if hasattr(driver_controller.driver_view_drives, "__self__") else None
    except Exception:
        driver = None
    # Fallback: return id only
    return jsonify({"id": uid}), 200


@bp.get("/drives")
@jwt_required()
@role_required("driver")
def list_drives():
    params = request.args
    status = params.get("status")
    date = params.get("date")
    page = int(params.get("page", 1))
    page_size = int(params.get("page_size", 20))
    uid = current_user_id()
    # controller: driver_view_drives(driver) returns list; repository may expect driver instance
    drives = driver_controller.driver_view_drives(uid)
    # naive pagination
    total = len(drives)
    start = (page - 1) * page_size
    items = [d.get_json() if hasattr(d, "get_json") else d for d in drives[start:start + page_size]]
    return jsonify({"items": items, "page": page, "total": total}), 200


@bp.post("/drives")
@jwt_required()
@role_required("driver")
def create_drive():
    data = request.get_json() or {}
    street_id = data.get("street_id")
    date = data.get("date")
    time = data.get("time")
    if not street_id or not date or not time:
        return jsonify({"error": {"code": "validation_error", "message": "street_id, date and time required"}}), 422
    uid = current_user_id()
    try:
        drive = driver_controller.driver_schedule_drive(uid, None, street_id, date, time)
    except ValueError as e:
        return jsonify({"error": {"code": "validation_error", "message": str(e)}}), 422

    out = drive.get_json() if hasattr(drive, "get_json") else drive
    return jsonify(out), 201


@bp.post("/drives/<int:drive_id>/start")
@jwt_required()
@role_required("driver")
def start_drive(drive_id):
    uid = current_user_id()
    try:
        driver_controller.driver_start_drive(uid, drive_id)
    except ValueError as e:
        return jsonify({"error": {"code": "validation_error", "message": str(e)}}), 400
    return jsonify({"id": drive_id, "status": "started"}), 200


@bp.post("/drives/<int:drive_id>/end")
@jwt_required()
@role_required("driver")
def end_drive(drive_id):
    uid = current_user_id()
    try:
        res = driver_controller.driver_end_drive(uid)
    except ValueError as e:
        return jsonify({"error": {"code": "validation_error", "message": str(e)}}), 400
    return jsonify({"id": getattr(res, "id", drive_id), "status": "ended"}), 200


@bp.post("/drives/<int:drive_id>/cancel")
@jwt_required()
@role_required("driver")
def cancel_drive(drive_id):
    uid = current_user_id()
    try:
        driver_controller.driver_cancel_drive(uid, drive_id)
    except ValueError as e:
        return jsonify({"error": {"code": "validation_error", "message": str(e)}}), 400
    return jsonify({"id": drive_id, "status": "cancelled"}), 200


@bp.get("/drives/<int:drive_id>/requested-stops")
@jwt_required()
@role_required("driver")
def requested_stops(drive_id):
    uid = current_user_id()
    stops = driver_controller.driver_view_requested_stops(uid, drive_id)
    items = [s.get_json() if hasattr(s, "get_json") else s for s in (stops or [])]
    return jsonify({"items": items}), 200
