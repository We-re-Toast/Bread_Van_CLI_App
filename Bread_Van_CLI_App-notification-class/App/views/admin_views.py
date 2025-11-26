from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from App.api.security import role_required
from App.controllers import admin as admin_controller
from App.controllers import resident as resident_controller
from App.controllers import user as user_controller

admin_views = Blueprint('admin_views', __name__)


@admin_views.route('/admin/users', methods=['GET'])
@jwt_required()
@role_required('Admin')
def list_users():
    role = request.args.get('role')
    users = user_controller.get_all_users_json() if hasattr(user_controller, 'get_all_users_json') else []
    # repo has no unified users listing in admin module; leave empty or hook to user.get_all_users if desired
    return jsonify({'items': users}), 200


@admin_views.route('/admin/drivers', methods=['POST'])
@jwt_required()
@role_required('Admin')
def create_driver():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': {'code': 'validation_error', 'message': 'username and password required'}}), 422
    driver = admin_controller.admin_create_driver(username, password)
    out = driver.get_json() if hasattr(driver, 'get_json') else driver
    return jsonify(out), 201


@admin_views.route('/admin/drivers/<int:driver_id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin')
def delete_driver(driver_id):
    admin_controller.admin_delete_driver(driver_id)
    return '', 204


@admin_views.route('/admin/residents', methods=['POST'])
@jwt_required()
@role_required('Admin')
def create_resident():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': {'code': 'validation_error', 'message': 'username and password required'}}), 422
    area_id = data.get('area_id')
    street_id = data.get('street_id')
    house_number = data.get('house_number')
    if area_id is None or street_id is None or house_number is None:
        return jsonify({'error': {'code': 'validation_error', 'message': 'area_id, street_id and house_number required'}}), 422
    resident = resident_controller.resident_create(username, password, area_id, street_id, house_number)
    out = resident.get_json() if hasattr(resident, 'get_json') else {'id': resident.id}
    return jsonify(out), 201


@admin_views.route('/admin/areas', methods=['POST'])
@jwt_required()
@role_required('Admin')
def create_area():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': {'code': 'validation_error', 'message': 'name required'}}), 422
    area = admin_controller.admin_add_area(name)
    out = area.get_json() if hasattr(area, 'get_json') else area
    return jsonify(out), 201


@admin_views.route('/admin/areas/<int:area_id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin')
def delete_area(area_id):
    admin_controller.admin_delete_area(area_id)
    return '', 204


@admin_views.route('/admin/streets', methods=['POST'])
@jwt_required()
@role_required('Admin')
def create_street():
    data = request.get_json() or {}
    name = data.get('name')
    area_id = data.get('area_id')
    if not name or not area_id:
        return jsonify({'error': {'code': 'validation_error', 'message': 'name and area_id required'}}), 422
    street = admin_controller.admin_add_street(area_id, name)
    out = street.get_json() if hasattr(street, 'get_json') else street
    return jsonify(out), 201


@admin_views.route('/admin/streets/<int:area_id>/<int:street_id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin')
def delete_street(area_id, street_id):
    admin_controller.admin_delete_street(area_id, street_id)
    return '', 204


@admin_views.route('/admin/areas', methods=['GET'])
@jwt_required()
@role_required('Admin')
def list_areas():
    areas = admin_controller.admin_view_all_areas()
    items = [a.get_json() if hasattr(a, 'get_json') else a for a in (areas or [])]
    return jsonify({'items': items}), 200


@admin_views.route('/admin/streets', methods=['GET'])
@jwt_required()
@role_required('Admin')
def list_streets():
    streets = admin_controller.admin_view_all_streets()
    items = [s.get_json() if hasattr(s, 'get_json') else s for s in (streets or [])]
    return jsonify({'items': items}), 200
