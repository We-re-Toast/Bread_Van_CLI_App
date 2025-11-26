from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity


def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def inner(*a, **k):
            verify_jwt_in_request()
            claims = get_jwt()
            if roles and claims.get("role") not in roles:
                return jsonify({"error": {"code": "forbidden", "message": "insufficient role"}}), 403
            return fn(*a, **k)
        return inner
    return wrapper


def current_user_id():
    identity = get_jwt_identity()
    try:
        return int(identity) if identity is not None else None
    except (TypeError, ValueError):
        return None
