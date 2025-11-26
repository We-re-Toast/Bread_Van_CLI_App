from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers.resident import (
    update_area_info,
    update_street_info,
    update_house_number,
    update_resident_username,
)
from App.controllers.stop_request import (
    request_stop,
    get_requested_stops,
    cancel_stop
)
from App.controllers.driver import get_driver_status_and_location
from App.exceptions import ResourceNotFound, ValidationError, DuplicateEntity

resident_views = Blueprint('resident_views', __name__, template_folder='../templates')

@resident_views.route('/api/resident/stops', methods=['POST'])
@jwt_required()
def request_stop_api():
    if current_user.role != 'resident':
        return jsonify(error="Unauthorized"), 403
    
    data = request.json
    try:
        stop = request_stop(current_user.id, data['drive_id'], data.get('message', ''))
        return jsonify(message="Stop requested", id=stop.id), 201
    except (ResourceNotFound, ValidationError) as e:
        return jsonify(error=str(e)), 400

@resident_views.route('/api/resident/stops', methods=['GET'])
@jwt_required()
def get_stops_api():
    if current_user.role != 'resident':
        return jsonify(error="Unauthorized"), 403
    
    stops = get_requested_stops(current_user.id)
    # Assuming StopRequest has get_json or we construct it
    return jsonify([{
        "id": stop.id,
        "drive_id": stop.drive_id,
        "message": stop.message,
        "status": "Pending" # Assuming default status
    } for stop in stops])

@resident_views.route('/api/resident/stops/<int:stop_id>', methods=['DELETE'])
@jwt_required()
def cancel_stop_api(stop_id):
    if current_user.role != 'resident':
        return jsonify(error="Unauthorized"), 403
    
    try:
        cancel_stop(stop_id, current_user.id)
        return jsonify(message="Stop request cancelled")
    except (ResourceNotFound, ValidationError) as e:
        return jsonify(error=str(e)), 400

@resident_views.route('/api/resident/area', methods=['PUT'])
@jwt_required()
def update_area_api():
    if current_user.role != 'resident':
        return jsonify(error="Unauthorized"), 403
    
    data = request.json
    try:
        area = update_area_info(current_user.id, data['area_id'])
        return jsonify(area.to_json()), 200
    except (ResourceNotFound, ValidationError) as e:
        return jsonify(error=str(e)), 400

@resident_views.route('/api/resident/street', methods=['PUT'])
@jwt_required()
def update_street_api():
    if current_user.role != 'resident':
        return jsonify(error="Unauthorized"), 403
    
    data = request.json
    try:
        street = update_street_info(current_user.id, data['street_id'])
        return jsonify(street.to_json()), 200
    except (ResourceNotFound, ValidationError) as e:
        return jsonify(error=str(e)), 400

@resident_views.route('/api/resident/house_number', methods=['PUT'])
@jwt_required()
def update_house_number_api():
    if current_user.role != 'resident':
        return jsonify(error="Unauthorized"), 403
    
    data = request.json
    try:
        house_number = update_house_number(current_user.id, data['house_number'])
        return jsonify(house_number.to_json()), 200
    except (ResourceNotFound, ValidationError) as e:
        return jsonify(error=str(e)), 400

@resident_views.route('/api/resident/username', methods=['PUT'])
@jwt_required()
def update_username_api():
    if current_user.role != 'resident':
        return jsonify(error="Unauthorized"), 403
    
    data = request.json
    try:
        username = update_resident_username(current_user.id, data['username'])
        return jsonify(username.to_json()), 200
    except (ResourceNotFound, ValidationError) as e:
        return jsonify(error=str(e)), 400

@resident_views.route('/api/resident/get-driver-status/<int:driver_id>', methods=['GET'])
@jwt_required()
def get_driver_status_api(driver_id):
    if current_user.role != 'resident':
        return jsonify(error="Unauthorized"), 403
    try:
        driver_status = get_driver_status_and_location(driver_id)
        return jsonify(driver_status), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404