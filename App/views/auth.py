from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies


from.index import index_views

from App.controllers import (
    login,
    create_user,
)
from App.controllers import resident as resident_controller

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response


@auth_views.route('/api/signup', methods=['POST'])
@auth_views.route('/auth/signup', methods=['POST'])
def signup_api():
    """Create a new account. JSON body: {username, password, role?, area_id?, street_id?, house_number?}
    role defaults to 'resident' which will call resident creation (requires area_id, street_id, house_number).
    Any other role will create a base User via create_user.
    """
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'resident')
    if not username or not password:
        return jsonify({'error': {'code': 'validation_error', 'message': 'username and password required'}}), 422

    try:
        if role == 'resident':
            area_id = data.get('area_id')
            street_id = data.get('street_id')
            house_number = data.get('house_number')
            if area_id is None or street_id is None or house_number is None:
                return jsonify({'error': {'code': 'validation_error', 'message': 'area_id, street_id and house_number required for resident'}}), 422
            resident = resident_controller.resident_create(username, password, area_id, street_id, house_number)
            out = resident.get_json() if hasattr(resident, 'get_json') else {'id': resident.id}
            return jsonify(out), 201
        else:
            user = create_user(username, password)
            out = user.get_json() if hasattr(user, 'get_json') else {'id': user.id}
            return jsonify(out), 201
    except Exception as e:
        return jsonify({'Error': 'user cannot be created'}), 400
