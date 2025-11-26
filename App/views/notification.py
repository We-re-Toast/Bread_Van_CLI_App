from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers.notification import get_notification_history, mark_notification_as_read

notification_views = Blueprint('notification_views', __name__, template_folder='../templates')

@notification_views.route('/api/notifications', methods=['GET'])
@jwt_required()
def get_notifications_api():
    if current_user.role != 'resident':
        return jsonify(error="Unauthorized"), 403
    
    try:
        notifications = get_notification_history(current_user.id)
        return jsonify(notifications), 200
    except ValueError as e:
        return jsonify(error=str(e)), 400

@notification_views.route('/api/notifications/<int:notification_id>', methods=['PUT'])
@jwt_required()
def mark_notification_as_read_api(notification_id):
    if current_user.role != 'resident':
        return jsonify(error="Unauthorized"), 403
    
    try:
        mark_notification_as_read(notification_id)
        return jsonify(message="Notification marked as read"), 200
    except ValueError as e:
        return jsonify(error=str(e)), 400
