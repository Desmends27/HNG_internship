import requests
from flask import Flask, request, jsonify
""" Returns an api response  with user name, ip and temperature """

app = Flask(__name__)

@app.route("/api/hello", methods=['GET'])
def hello():
    """ main api endpoint for request """
    username = request.args.get('visitor_name')

    client_ip = request.remote_addr
    ip_info_url = f"http://ip-api.com/json/{client_ip}"
    try:
        response = requests.get(ip_info_url).json()
    except requests.RequestException as e:
        return jsonify({"error": "Could not retrieve location data"}), 500
    
    return (response)


@app.errorhandler(404)
def page_not_found(e):
    """ Handle requests to other endpoints """
    return jsonify({"status": 404, "message": "Not Found"}), 404

if __name__ == "__main__":
    app.run(DEBUG=True)
