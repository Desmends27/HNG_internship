import requests
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
""" Returns an api response  with user name, ip and temperature """

app = Flask(__name__)


@app.route("/api/hello", methods=['GET'])
def hello():
    """ main api endpoint for request """
    username = request.args.get('visitor_name', 'visitor').strip('"')

    client_ip = request.remote_addr
    ip_info_url = f"http://ip-api.com/json/{client_ip}"
    # Request for ip address
    try:
        response = requests.get(ip_info_url).json()
    except requests.RequestException as e:
        return jsonify({"error": "Could not retrieve location data"}), 500
    location = response["city"]

    # Request for temperature
    try:
        payload = {'apikey': os.getenv('API_KEY'), 'location': location}
        headers = {"accept": "application/json"}
        url = "https://api.tomorrow.io/v4/weather/realtime"
        response = requests.get(url, headers=headers, params=payload).json()
        temperature = response["data"]['values']["temperature"]
    except requests.RequestException as e:
        return jsonify({"error": "Could not retrieve location data"}), 500
    
    greeting = f"Hello, {username}!, the temperature is {temperature} degrees Celcius in {location}"

    return jsonify({
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting,
    })


@app.errorhandler(404)
def page_not_found(e):
    """ Handle requests to other endpoints """
    return jsonify({"status": 404, "message": "Not Found"}), 404


if __name__ == "__main__":
    app.run(DEBUG=True)
