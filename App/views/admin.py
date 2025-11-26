from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers.driver import create_driver, get_all_drivers_json, delete_driver
from App.controllers.resident import create_resident, get_all_residents_json, delete_resident
from App.controllers.area import create_area, get_all_areas_json, delete_area
from App.controllers.street import create_street, get_all_streets_json, delete_street
from App.exceptions import DuplicateEntity, ResourceNotFound, ValidationError

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

def setup_admin(app):
    return

def admin_required():
    if not current_user or current_user.role != 'admin':
        return False
    return True

@admin_views.route('/api/admin/drivers', methods=['POST'])
@jwt_required()
def create_driver_api():
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    data = request.json
    try:
        driver = create_driver(data['username'], data['password'], data.get('status', 'Off Duty'), data.get('area_id'), data.get('street_id'))
        return jsonify(driver.get_json()), 201
    except DuplicateEntity as e:
        return jsonify(error=str(e)), 409
    except ValidationError as e:
        return jsonify(error=str(e)), 400

@admin_views.route('/api/admin/drivers', methods=['GET'])
@jwt_required()
def get_drivers_api():
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    return jsonify(get_all_drivers_json()), 200

@admin_views.route('/api/admin/drivers/<int:driver_id>', methods=['DELETE'])
@jwt_required()
def delete_driver_api(driver_id):
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    try:
        delete_driver(driver_id)
        return jsonify(message="Driver deleted"), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@admin_views.route('/api/admin/residents', methods=['POST'])
@jwt_required()
def create_resident_api():
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    data = request.json
    try:
        resident = create_resident(data['username'], data['password'], data['area_id'], data['street_id'], data['house_number'])
        return jsonify(resident.get_json()), 201
    except DuplicateEntity as e:
        return jsonify(error=str(e)), 409
    except (ResourceNotFound, ValidationError) as e:
        return jsonify(error=str(e)), 400

@admin_views.route('/api/admin/residents', methods=['GET'])
@jwt_required()
def get_residents_api():
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    return jsonify(get_all_residents_json()), 200

@admin_views.route('/api/admin/residents/<int:resident_id>', methods=['DELETE'])
@jwt_required()
def delete_resident_api(resident_id):
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    try:
        delete_resident(resident_id)
        return jsonify(message="Resident deleted"), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@admin_views.route('/api/admin/areas', methods=['POST'])
@jwt_required()
def create_area_api():
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    data = request.json
    try:
        area = create_area(data['name'])
        return jsonify(area.get_json()), 201
    except DuplicateEntity as e:
        return jsonify(error=str(e)), 409
    except ValidationError as e:
        return jsonify(error=str(e)), 400

@admin_views.route('/api/admin/areas', methods=['GET'])
@jwt_required()
def get_areas_api():
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    return jsonify(get_all_areas_json()), 200

@admin_views.route('/api/admin/areas/<int:area_id>', methods=['DELETE'])
@jwt_required()
def delete_area_api(area_id):
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    try:
        delete_area(area_id)
        return jsonify(message="Area deleted"), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@admin_views.route('/api/admin/streets', methods=['POST'])
@jwt_required()
def create_street_api():
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    data = request.json
    try:
        street = create_street(data['name'], data['area_id'])
        return jsonify(street.get_json()), 201
    except DuplicateEntity as e:
        return jsonify(error=str(e)), 409
    except (ResourceNotFound, ValidationError) as e:
        return jsonify(error=str(e)), 400

@admin_views.route('/api/admin/streets', methods=['GET'])
@jwt_required()
def get_streets_api():
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    return jsonify(get_all_streets_json()), 200

@admin_views.route('/api/admin/streets/<int:street_id>', methods=['DELETE'])
@jwt_required()
def delete_street_api(street_id):
    if not admin_required(): return jsonify(error="Unauthorized"), 403
    try:
        delete_street(street_id)
        return jsonify(message="Street deleted"), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404
