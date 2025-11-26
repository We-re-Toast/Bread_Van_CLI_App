from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from App.views.auth import auth_views
from App.controllers import driver as driver_controller
from App.controllers import user as user_controller
from App.views import user as user_views
from App.api.security import role_required, current_user_id

driver_views = Blueprint('driver_views', __name__)


@driver_views.route('/driver/me', methods=['GET'])
@jwt_required()
@role_required('Driver')
def me():
    uid = current_user_id()
    return jsonify({'id': uid}), 200


@driver_views.route('/driver/drives', methods=['GET'])
@jwt_required()
@role_required('Driver')
def list_drives():
    params = request.args
    page = int(params.get('page', 1))
    page_size = int(params.get('page_size', 20))
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    drives = driver_controller.driver_view_drives(driver)
    total = len(drives) if drives else 0
    start = (page - 1) * page_size
    items = [d.get_json() if hasattr(d, 'get_json') else d for d in (drives or [])[start:start+page_size]]
    return jsonify({'items': items, 'page': page, 'total': total}), 200


@driver_views.route('/driver/drives', methods=['POST'])
@jwt_required()
@role_required('Driver')
def create_drive():
    data = request.get_json() or {}
    area_id = data.get('area_id')
    street_id = data.get('street_id')
    date = data.get('date')
    time = data.get('time')
    if not street_id or not date or not time:
        return jsonify({'error': {'code': 'validation_error', 'message': 'street_id, date and time required'}}), 422
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    drive = driver_controller.driver_schedule_drive(driver, area_id, street_id, date, time)
    out = drive.get_json() if hasattr(drive, 'get_json') else drive
    return jsonify(out), 201


@driver_views.route('/driver/drives/<int:drive_id>/start', methods=['POST'])
@jwt_required()
@role_required('Driver')
def start_drive(drive_id):
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    driver_controller.driver_start_drive(driver, drive_id)
    return jsonify({'id': drive_id, 'status': 'started'}), 200


@driver_views.route('/driver/drives/<int:drive_id>/end', methods=['POST'])
@jwt_required()
@role_required('Driver')
def end_drive(drive_id):
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    res = driver_controller.driver_end_drive(driver)
    return jsonify({'id': getattr(res, 'id', drive_id), 'status': 'ended'}), 200


@driver_views.route('/driver/drives/<int:drive_id>/cancel', methods=['POST'])
@jwt_required()
@role_required('Driver')
def cancel_drive(drive_id):
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    driver_controller.driver_cancel_drive(driver, drive_id)
    return jsonify({'id': drive_id, 'status': 'cancelled'}), 200


@driver_views.route('/driver/drives/<int:drive_id>/requested-stops', methods=['GET'])
@jwt_required()
@role_required('Driver')
def requested_stops(drive_id):
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    stops = driver_controller.driver_view_requested_stops(driver, drive_id)
    items = [s.get_json() if hasattr(s, 'get_json') else s for s in (stops or [])]
    return jsonify({'items': items}), 200
