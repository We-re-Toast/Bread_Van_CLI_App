from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from App.api.security import role_required, current_user_id
from App.controllers import resident as resident_controller

bp = Blueprint("api_resident", __name__, url_prefix="/resident")


@bp.get("/me")
@jwt_required()
@role_required("resident")
def me():
    uid = current_user_id()
    return jsonify({"id": uid}), 200


@bp.post("/stops")
@jwt_required()
@role_required("resident")
def create_stop():
    data = request.get_json() or {}
    drive_id = data.get("drive_id")
    if not drive_id:
        return jsonify({"error": {"code": "validation_error", "message": "drive_id required"}}), 422
    uid = current_user_id()
    try:
        stop = resident_controller.resident_request_stop(uid, drive_id)
    except ValueError as e:
        return jsonify({"error": {"code": "validation_error", "message": str(e)}}), 400
    out = stop.get_json() if hasattr(stop, "get_json") else stop
    return jsonify(out), 201


@bp.delete("/stops/<int:stop_id>")
@jwt_required()
@role_required("resident")
def delete_stop(stop_id):
    uid = current_user_id()
    try:
        resident_controller.resident_cancel_stop(uid, stop_id)
    except ValueError as e:
        return jsonify({"error": {"code": "resource_not_found", "message": str(e)}}), 404
    return "", 204


@bp.get("/inbox")
@jwt_required()
@role_required("resident")
def inbox():
    uid = current_user_id()
    items = resident_controller.resident_view_inbox(uid)
    items = [i.get_json() if hasattr(i, "get_json") else i for i in (items or [])]
    return jsonify({"items": items}), 200


@bp.get("/driver-stats")
@jwt_required()
@role_required("resident")
def driver_stats():
    params = request.args
    street_id = params.get("street_id")
    from_date = params.get("from")
    to_date = params.get("to")
    uid = current_user_id()
    stats = resident_controller.resident_view_driver_stats(uid, street_id, from_date, to_date)
    return jsonify({"stats": stats}), 200
