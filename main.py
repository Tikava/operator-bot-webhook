from http import HTTPStatus
from flask import Flask, Response, request, make_response
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
    return Response(status=HTTPStatus.OK)

@app.post('/setWebhook')
def set_webhook() -> Response:
    # Get the token from the request body
    token = request.json.get('token')

    with open(CERTIFICATE_PATH, 'rb') as file:
        files = {'certificate': file}
        data = {'url': f'{SERVICE_URL}/webhook/{token}'}
        
        requests.post(f'https://api.telegram.org/bot{token}/setWebhook', files=files, data=data)


@app.get('/health')
def health() -> Response:
    """For the health endpoint, reply with a simple plain text message."""
    response = make_response("The bot is still running fine :)", HTTPStatus.OK)
    response.mimetype = "text/plain"
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
