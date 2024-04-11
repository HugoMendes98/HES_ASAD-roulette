from flask import Flask, render_template
from flask_sock import Sock as WebSocket

app = Flask(__name__)
sock = WebSocket(app)


@app.route('/')
def index():
    return render_template('index.html')


@sock.route('/echo')
def echo(sock):
    while True:
        data = sock.receive()
        sock.send(data)

app.run("0.0.0.0", 5000, debug=True)