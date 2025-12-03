from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from App.api.security import role_required
from App.controllers import admin as admin_controller

bp = Blueprint("api_admin", __name__, url_prefix="/admin")


@bp.post("/drivers")
@jwt_required()
@role_required("Admin")
def create_driver():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": {"code": "validation_error", "message": "username and password required"}}), 422
    try:
        driver = admin_controller.admin_create_driver(username, password)
    except ValueError as e:
        return jsonify({"error": {"code": "conflict", "message": str(e)}}), 409
    out = driver.get_json() if hasattr(driver, "get_json") else driver
    return jsonify(out), 201


@bp.delete("/drivers/<int:driver_id>")
@jwt_required()
@role_required("Admin")
def delete_driver(driver_id):
    try:
        admin_controller.admin_delete_driver(driver_id)
    except ValueError as e:
        return jsonify({"error": {"code": "resource_not_found", "message": str(e)}}), 404
    return "", 204

@bp.post("/areas")
@jwt_required()
@role_required("Admin")
def create_area():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": {"code": "validation_error", "message": "name required"}}), 422
    area = admin_controller.admin_add_area(name)
    return jsonify(area.get_json()), 201


@bp.delete("/areas/<int:area_id>")
@jwt_required()
@role_required("Admin")
def delete_area(area_id):
    try:
        admin_controller.admin_delete_area(area_id)
    except ValueError as e:
        return jsonify({"error": {"code": "resource_not_found", "message": str(e)}}), 404
    return "", 204


@bp.post("/streets")
@jwt_required()
@role_required("Admin")
def create_street():
    data = request.get_json() or {}
    area_id = data.get("area_id")
    name = data.get("name")
    if not area_id or not name:
        return jsonify({"error": {"code": "validation_error", "message": "area_id and name required"}}), 422
    try:
        street = admin_controller.admin_add_street(area_id, name)
    except ValueError as e:
        return jsonify({"error": {"code": "resource_not_found", "message": str(e)}}), 404
    return jsonify(street.get_json()), 201


@bp.delete("/streets/<int:street_id>")
@jwt_required()
@role_required("Admin")
def delete_street(street_id):
    try:
        admin_controller.admin_delete_street(street_id)
    except ValueError as e:
        return jsonify({"error": {"code": "resource_not_found", "message": str(e)}}), 404
    return "", 204


@bp.get("/areas")
@jwt_required()
@role_required("Admin")
def list_areas():
    areas = admin_controller.admin_view_all_areas()
    items = [a.get_json() if hasattr(a, "get_json") else a for a in areas]
    return jsonify({"items": items}), 200


@bp.get("/streets")
@jwt_required()
@role_required("Admin")
def list_streets():
    streets = admin_controller.admin_view_all_streets()
    items = [s.get_json() if hasattr(s, "get_json") else s for s in streets]
    return jsonify({"items": items}), 200

@bp.post("/items")
@jwt_required()
@role_required("Admin")
def add_item():
    data = request.get_json() or {}
    name = data.get("name")
    price = data.get("price")
    description = data.get("description")
    tags = data.get("tags", "")

    if not name or price is None:
        return jsonify({"error": {"code": "validation_error", "message": "name and price required"}}), 422
    
    try:
        item = admin_controller.admin_add_item(name, price, description, tags)
    except Exception as e:
        return jsonify({"error": {"code": "conflict", "message": str(e)}}), 409
    
    return jsonify(item.get_json() if hasattr(item, "get_json") else item.__dict__), 201

@bp.delete("/items/<int:item_id>")
@jwt_required()
@role_required("Admin")
def delete_item(item_id):
    try:
        admin_controller.admin_delete_item(item_id)
    except ValueError as e:
        return jsonify({"error": {"code": "resource_not_found", "message": str(e)}}), 404
    return "", 204

@bp.get("/items")
@jwt_required()
@role_required("Admin")
def view_all_items():
    items = admin_controller.admin_view_all_items()
    return jsonify({"items": [i.get_json() if hasattr(i, "get_json") else i.__dict__ for i in items]}), 200