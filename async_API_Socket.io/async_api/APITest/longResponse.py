# APITest/longResponse.py
import os
from flask_restful import Resource
from flask import request, jsonify
import time
from APITest.longTesting import Testing

class LongResponse(Resource):
    # def post(self):
    #     data = request.json['data']
    #     data = range(1, data)
    #     for index, item in enumerate(data):
    #         print(item)
    #         self.process_item(item)
    #     #     socketio.emit('status_update', {'progress': f"Processed {index + 1} of {len(data)} items"})
    #     # return jsonify({"status": "Processing started"})

    # def process_item(self, item):
    #     import time
    #     time.sleep(1)  # Simulating processing delay

    # def get(self):
    #     data = range(1, 5)
    #     for index, item in enumerate(data):
    #         self.process_item(item)
    #         socketio.emit('status_update', {'progress': f"Processed {index + 1} of {len(data)} items"})
    #     return jsonify({"status": "Processing started"})

    def background_task(sid, socketio, inputs):
        """ Example of a long-running task that emits SocketIO messages """
        socketio.sleep(5)  # Simulate a delay
        for i in range(1, 11):
            socketio.emit('my_response', {'data': f'Processing {i*10}%'}, room=sid)
            socketio.sleep(1)  # Simulate work being done
        socketio.emit('my_response', {'data': 'Task Completed'}, room=sid)

    def post(sid, socketio, inputs):
        test = Testing(sid, socketio, inputs)
        socketio.emit('response', {'data': [0, f'Initilaized Testing Class.']}, room=sid)
        aTest = test.moreTest()
        print(aTest)
        socketio.emit('response', {'data': [1, aTest]}, room=sid)

