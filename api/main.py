import os
import requests
import logging
from waitress import serve
from flask import Flask, request, send_from_directory, jsonify

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)

# Get the secret API key from environment variable
my_secret = os.environ.get('ST_API_KEY')


@app.route('/environments', methods=['POST'])
def create_environment():
  try:
    # Parse the JSON request data
    data = request.get_json()
    name = data.get('name')
    chain_id = data.get('chainId')
    networks = data.get('networks')

    # URL and headers for the POST request
    url = 'https://api.nameless.io/v1/environments'
    headers = {'x-api-key': my_secret, 'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the response is successful (HTTP 200)
    if response.status_code == 201:  # I updated this to 201 as per your response codes
      result = response.json()
      return jsonify(result)
    else:
      raise Exception(f"Error: {response.status_code}, {response.text}")
  except Exception as e:
    # Log the exception message
    logging.error(f"Exception occurred: {str(e)}")
    # Return the exception message as a response
    return str(e)


@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


# Run the Flask app
if __name__ == '__main__':
  serve(app, host="0.0.0.0", port=8080)
