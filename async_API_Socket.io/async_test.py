from flask import Flask, jsonify, request
from flask_restful import Api
from celery import Celery

from APITest import longResponse

app = Flask(__name__)
api = Api(app)
# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:5000/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:5000/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

api.add_resource(longResponse, '/test/')

# Define an asynchronous task using Celery
@celery.task(bind=True)
def long_running_task(self, x):
    """Example of a long-running task."""
    import time
    for i in range(x):
        time.sleep(1)  # Simulate a task taking some time
        self.update_state(state='PROGRESS', meta={'current': i, 'total': x})
    return {'current': x, 'total': x, 'status': 'Task completed'}

@app.route('/start_task', methods=['POST'])
def start_task():
    x = int(request.form.get('x', 10))  # Number of iterations, default is 10
    task = long_running_task.apply_async(args=[x])
    return jsonify({'task_id': task.id}), 202

@app.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = long_running_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'status': 'In Progress...',
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1)
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'status': task.info.get('status', ''),
            'result': task.info
        }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
