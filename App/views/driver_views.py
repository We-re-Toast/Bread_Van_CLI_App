from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from App.views.auth import auth_views
from App.controllers import driver as driver_controller
from App.controllers import user as user_controller
from App.views import user as user_views
from App.api.security import role_required, current_user_id
from App.models import DriverStock, Resident
from App.database import db

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


@driver_views.route('/driver/drives/start', methods=['POST'])
@jwt_required()
@role_required('Driver')
def start_drive():
    data = request.get_json() or {}
    drive_id = data.get('drive_id')
    if drive_id is None:
        return jsonify({'error': {'code': 'validation_error', 'message': 'drive_id required'}}), 422
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    driver_controller.driver_start_drive(driver, drive_id)
    return jsonify({'id': drive_id, 'status': 'started'}), 200


@driver_views.route('/driver/drives/end', methods=['POST'])
@jwt_required()
@role_required('Driver')
def end_drive():
    # end the current in-progress drive for this driver
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    res = driver_controller.driver_end_drive(driver)
    return jsonify({'id': getattr(res, 'id', None), 'status': 'ended'}), 200


@driver_views.route('/driver/drives/cancel', methods=['POST'])
@jwt_required()
@role_required('Driver')
def cancel_drive():
    data = request.get_json() or {}
    drive_id = data.get('drive_id')
    if drive_id is None:
        return jsonify({'error': {'code': 'validation_error', 'message': 'drive_id required'}}), 422
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    driver_controller.driver_cancel_drive(driver, drive_id)
    return jsonify({'id': drive_id, 'status': 'cancelled'}), 200


@driver_views.route('/driver/drives/requested-stops', methods=['POST'])
@jwt_required()
@role_required('Driver')
def requested_stops():
    data = request.get_json() or {}
    drive_id = data.get('drive_id')
    if drive_id is None:
        return jsonify({'error': {'code': 'validation_error', 'message': 'drive_id required'}}), 422
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    stops = driver_controller.driver_view_requested_stops(driver, drive_id)
    items = [s.get_json() if hasattr(s, 'get_json') else s for s in (stops or [])]
    return jsonify({'items': items}), 200


@driver_views.route('/driver/stock', methods=['GET'])
@jwt_required()
@role_required('Driver')
def view_stock():
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    stocks = driver_controller.driver_view_stock(driver)
    items = [s.get_json() if hasattr(s, 'get_json') else s for s in (stocks or [])]
    return jsonify({'items': items}), 200


@driver_views.route('/driver/stock', methods=['POST'])
@jwt_required()
@role_required('Driver')
def create_or_update_stock():
    data = request.get_json() or {}
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    if item_id is None or quantity is None:
        return jsonify({'error': {'code': 'validation_error', 'message': 'item_id and quantity required'}}), 422
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    try:
        stock = driver_controller.driver_update_stock(driver, item_id, int(quantity))
    except Exception as e:
        return jsonify({'error': {'code': 'server_error', 'message': str(e)}}), 500
    out = stock.get_json() if hasattr(stock, 'get_json') else {'id': getattr(stock, 'id', None)}
    return jsonify(out), 201


@driver_views.route('/driver/stock', methods=['PATCH'])
@jwt_required()
@role_required('Driver')
def patch_stock():
    data = request.get_json() or {}
    stock_id = data.get('stock_id')
    quantity = data.get('quantity')
    if stock_id is None or quantity is None:
        return jsonify({'error': {'code': 'validation_error', 'message': 'stock_id and quantity required'}}), 422
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    stock = DriverStock.query.get(stock_id)
    if not stock or stock.driverId != driver.id:
        return jsonify({'error': {'code': 'not_found', 'message': 'Stock not found'}}), 404
    try:
        stock.quantity = int(quantity)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': {'code': 'server_error', 'message': str(e)}}), 500
    return jsonify(stock.get_json() if hasattr(stock, 'get_json') else {'id': stock.id, 'quantity': stock.quantity}), 200


@driver_views.route('/driver/stock', methods=['DELETE'])
@jwt_required()
@role_required('Driver')
def delete_stock():
    data = request.get_json() or {}
    stock_id = data.get('stock_id')
    if stock_id is None:
        return jsonify({'error': {'code': 'validation_error', 'message': 'stock_id required'}}), 422
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    stock = DriverStock.query.get(stock_id)
    if not stock or stock.driverId != driver.id:
        return jsonify({'error': {'code': 'not_found', 'message': 'Stock not found'}}), 404
    try:
        db.session.delete(stock)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': {'code': 'server_error', 'message': str(e)}}), 500
    return '', 204


@driver_views.route('/driver/notify', methods=['POST'])
@jwt_required()
@role_required('Driver')
def notify():
    data = request.get_json() or {}
    message = data.get('message')
    if not message:
        return jsonify({'error': {'code': 'validation_error', 'message': 'message required'}}), 422
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    try:
        driver.notify_observers(message)
    except Exception as e:
        return jsonify({'error': {'code': 'server_error', 'message': str(e)}}), 500
    return jsonify({'message': 'notified'}), 200


@driver_views.route('/driver/subscribers', methods=['GET'])
@jwt_required()
@role_required('Driver')
def list_subscribers():
    uid = current_user_id()
    driver = user_controller.get_user(uid)
    subs = []
    # residents store subscriptions as list of driver ids
    for r in Resident.query.all():
        if r.subscriptions and driver.id in r.subscriptions:
            subs.append(r)
    items = [r.get_json() if hasattr(r, 'get_json') else {'id': r.id} for r in subs]
    return jsonify({'items': items}), 200
