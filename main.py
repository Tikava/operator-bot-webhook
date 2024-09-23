from http import HTTPStatus
from flask import Flask, jsonify, request, Response
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)

SERVICE_URL = getenv('SERVICE_URL')
CERTIFICATE_PATH = getenv('CERTIFICATE_PATH')

@app.post('/<token>')
def webhook(token) -> Response:
    # Print all the request data
    print(request.json)
    return jsonify({"status": "ok"}), HTTPStatus.OK  # Return JSON response

@app.post('/setWebhook')
def set_webhook() -> Response:
    # Get the token from the request body
    token = request.json.get('token')
    
    if not token:
        return jsonify({"error": "Missing token"}), HTTPStatus.BAD_REQUEST

    try:
        with open(CERTIFICATE_PATH, 'rb') as file:
            files = {'certificate': file}
            data = {'url': f'{SERVICE_URL}/webhook/{token}'}
            
            response = requests.post(f'https://api.telegram.org/bot{token}/setWebhook', files=files, data=data)
            return jsonify({"response": response.json()}), response.status_code  # Return JSON response
    except FileNotFoundError:
        return jsonify({"error": "Certificate file not found"}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred while setting the webhook"}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.get('/health')
def health() -> Response:
    """For the health endpoint, reply with a simple JSON message."""
    return jsonify({"status": "The bot is still running fine :)"})  # Return JSON response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Change to 0.0.0.0 to make it accessible externally
