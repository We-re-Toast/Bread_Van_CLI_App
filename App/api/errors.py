from flask import jsonify


class APIError(Exception):
    def __init__(self, code="validation_error", message="", status=400):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(err):
        return jsonify({"error": {"code": err.code, "message": err.message}}), err.status

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": {"code": "resource_not_found", "message": "Not found"}}), 404

    @app.errorhandler(401)
    def unauthorized(_):
        return jsonify({"error": {"code": "forbidden", "message": "Unauthorized"}}), 401
