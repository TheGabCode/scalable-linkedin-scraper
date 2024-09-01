# run_task.py
from celery_app import hello

# Call the task asynchronously
result = hello.delay()

# Get the result (this will block until the task is completed)
print("Task result:", result.get())