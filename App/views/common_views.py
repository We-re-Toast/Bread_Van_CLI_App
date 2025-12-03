from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from App.api.security import role_required
from App.controllers import area as area_controller
from App.controllers import street as street_controller
from App.controllers import drive as drive_controller
from App.models import DriverStock

common_views = Blueprint('common_views', __name__)


@common_views.route('/areas', methods=['GET'])
def get_areas():
    areas = area_controller.admin_view_all_areas() if hasattr(area_controller, 'admin_view_all_areas') else []
    items = [a.get_json() if hasattr(a, 'get_json') else a for a in (areas or [])]
    return jsonify({'items': items}), 200


@common_views.route('/streets', methods=['GET'])
def get_streets():
    area_id = request.args.get('area_id')
    streets = []
    if area_id and hasattr(street_controller, 'get_streets_for_area'):
        streets = street_controller.get_streets_for_area(area_id)
    elif hasattr(street_controller, 'admin_view_all_streets'):
        streets = street_controller.admin_view_all_streets()
    items = [s.get_json() if hasattr(s, 'get_json') else s for s in (streets or [])]
    return jsonify({'items': items}), 200


@common_views.route('/streets/drives', methods=['POST'])
@jwt_required()
@role_required('Resident', 'Driver', 'Admin')
def street_drives():
    data = request.get_json() or {}
    street_id = data.get('street_id')
    date = data.get('date')
    if street_id is None:
        return jsonify({'error': {'code': 'validation_error', 'message': 'street_id required'}}), 422
    drives = []
    if hasattr(drive_controller, 'get_drives_for_street'):
        drives = drive_controller.get_drives_for_street(street_id, date)
    items = [d.get_json() if hasattr(d, 'get_json') else d for d in (drives or [])]
    return jsonify({'items': items}), 200

@common_views.route('/drivers/stock', methods=['POST'])
@jwt_required()
@role_required('Resident', 'Driver', 'Admin')
def driver_stock():
    data = request.get_json() or {}
    driver_id = data.get('driver_id')
    if driver_id is None:
        return jsonify({'error': {'code': 'validation_error', 'message': 'driver_id required'}}), 422
    stocks = DriverStock.query.filter_by(driverId=driver_id).all()
    items = [s.get_json() if hasattr(s, 'get_json') else s for s in (stocks or [])]
    return jsonify({'items': items}), 200
