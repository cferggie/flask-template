from flask import Blueprint, request, jsonify

routes = Blueprint('routes', __name__)

# health check endpoint
@routes.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})
