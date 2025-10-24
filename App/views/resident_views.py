from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from App.api.security import role_required, current_user_id
from App.controllers import resident as resident_controller
from App.controllers import user as user_controller

resident_views = Blueprint('resident_views', __name__)


@resident_views.route('/resident/me', methods=['GET'])
@jwt_required()
@role_required('resident')
def me():
    uid = current_user_id()
    return jsonify({'id': uid}), 200


@resident_views.route('/resident/stops', methods=['POST'])
@jwt_required()
@role_required('resident')
def create_stop():
    data = request.get_json() or {}
    drive_id = data.get('drive_id')
    if not drive_id:
        return jsonify({'error': {'code': 'validation_error', 'message': 'drive_id required'}}), 422
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    stop = resident_controller.resident_request_stop(resident, drive_id)
    out = stop.get_json() if hasattr(stop, 'get_json') else stop
    return jsonify(out), 201


@resident_views.route('/resident/stops/<int:stop_id>', methods=['DELETE'])
@jwt_required()
@role_required('resident')
def delete_stop(stop_id):
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    resident_controller.resident_cancel_stop(resident, stop_id)
    return '', 204


@resident_views.route('/resident/inbox', methods=['GET'])
@jwt_required()
@role_required('resident')
def inbox():
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    items = resident_controller.resident_view_inbox(resident)
    items = [i.get_json() if hasattr(i, 'get_json') else i for i in (items or [])]
    return jsonify({'items': items}), 200


@resident_views.route('/resident/driver-stats', methods=['GET'])
@jwt_required()
@role_required('resident')
def driver_stats():
    params = request.args
    street_id = params.get('street_id')
    from_date = params.get('from')
    to_date = params.get('to')
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    stats = resident_controller.resident_view_driver_stats(resident, street_id)
    return jsonify({'stats': stats}), 200
