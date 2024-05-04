from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:4200")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

from APITest.longResponse import LongResponse
import time
from threading import Thread

# def background_task(sid):
#     """ Example of a long-running task that emits SocketIO messages """
#     socketio.sleep(5)  # Simulate a delay
#     for i in range(1, 11):
#         socketio.emit('my_response', {'data': f'Processing {i*10}%'}, room=sid)
#         socketio.sleep(1)  # Simulate work being done
#     socketio.emit('my_response', {'data': 'Task Completed'}, room=sid)

@app.route('/')
def index():
    return "Hello from Flask!"

@socketio.on('connect')
def test_connect():
    emit('my_response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('/test')
def handle_start_task(inputs):
    sid = request.sid  # pyright: ignore
    thread = Thread(target=LongResponse.post, args=(sid, socketio, inputs))
    thread.start()
    emit('response', [0, {'message': 'Task started'}])

if __name__ == '__main__':
    # socketio.run(app, port=5000, debug=True)
    app.run(port=5000, debug=True)
    