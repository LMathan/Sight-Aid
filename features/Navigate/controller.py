from flask import Blueprint, jsonify, request
from features.Navigate.service import coordinatesService,CommandService

nav_bp = Blueprint('nav_bp', __name__)


@nav_bp.route('/navigate', methods=['POST'])
def add_user():

    print("Navigetion service called")
    data = request.json
    print(data)

    place = f"{data['place']}, Erode, India"

    dest_service = coordinatesService(place)  # Create instance
    dest_coordinates = dest_service.coordinates  # Get coordinates

    if dest_coordinates:

        latitude, longitude = dest_coordinates

        cmd_service = CommandService(dest_coordinates, data['curr'])

        res = cmd_service.command()

        return jsonify({'command': res.cmd}), 201

    return jsonify({'error': 'Location not found'}), 400
