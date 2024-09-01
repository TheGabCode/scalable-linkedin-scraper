from celery import Celery

# Create a Celery app instance with Redis as the broker
app = Celery(
    'hello_world',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0')

# Define a simple task
@app.task
def hello():
    return "Hello, World!"