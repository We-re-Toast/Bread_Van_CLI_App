from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt

from App.controllers import auth as auth_controller
from App.controllers import user as user_controller

bp = Blueprint("api_auth", __name__, url_prefix="/auth")


@bp.post("/login")
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": {"code": "validation_error", "message": "username and password required"}}), 422

    try:
        user = user_controller.user_login(username, password)
    except ValueError as e:
        return jsonify({"error": {"code": "validation_error", "message": str(e)}}), 401

    # create tokens with role and sub claims
    additional_claims = {"role": getattr(user, "role", None)}
    access = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    refresh = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

    return jsonify({"access_token": access, "refresh_token": refresh, "user": {"id": user.id, "role": getattr(user, "role", None)}}), 200


@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    jwt = get_jwt()
    identity = jwt.get("sub") or jwt.get("identity")
    role = jwt.get("role")
    access = create_access_token(identity=str(identity), additional_claims={"role": role})
    return jsonify({"access_token": access}), 200
