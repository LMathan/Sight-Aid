from flask import Flask, request, jsonify 
import os

from features.PageRoute.controller import user_bp 
from features.Search.controller import user_bpSearch
from features.Navigate.controller import nav_bp

from core.Network import connection_checker
from core.Custom_Errors import NetworkError



app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(user_bpSearch, url_prefix='/api')
app.register_blueprint(nav_bp, url_prefix='/api')


@app.route('/rpi_register', methods=['GET'])
def register_rpi():
    rpi_ip = request.remote_addr
    
    os.environ["RPI_IP"] = F"{rpi_ip}"

    print(f"Raspberry-pi registered - {rpi_ip}")
    
    return jsonify({"message": "Raspberry Pi registered", "rpi_ip": rpi_ip}), 200


if __name__ == '__main__':
    
    try:
        if(connection_checker.check_network_connection()):
            raise NetworkError.Network_Error("No Internet")
            
        app.run(host='0.0.0.0', port=5000,debug=True)
    except Exception as e:
        print(e)