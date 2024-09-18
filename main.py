from http import HTTPStatus
from flask import Flask, Response, request, make_response

app = Flask(__name__)

@app.post('/')
def webhook() -> Response:
    # Optionally, process or log the JSON request data
    # data = request.get_json()
    return Response(status=HTTPStatus.OK)

@app.get('/healthcheck')
def health() -> Response:
    """For the health endpoint, reply with a simple plain text message."""
    response = make_response("The bot is still running fine :)", HTTPStatus.OK)
    response.mimetype = "text/plain"
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
