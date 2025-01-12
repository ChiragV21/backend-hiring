# Project Overview

This Django project integrates Celery for asynchronous task execution. It exposes API endpoints to manage `Site` and `JobExecution` models and trigger tasks based on a specified `site_id` and `task_type`.

## Setup and Execution

1. **Migrations**:
   - Run the following commands to create and apply migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

2. **Start Celery Worker**:
   - Start a Celery worker for your Django project (solo mode for development):
     ```bash
     celery -A vanderval worker --loglevel=info --pool=solo
     ```

3. **Run Django Server**:
   - Start the development server:
     ```bash
     python manage.py runserver
     ```

## API Endpoints

- **Get all Sites**:
  - URL: `http://127.0.0.1:8000/website/sites/`
  
- **Post Job Execution**:
  - URL: `http://127.0.0.1:8000/website/jobs/`
  - Request body:
    ```json
    {
        "site_id": 1,
        "task_type": "task_05"
    }
    ```

## Key Files and Features

1. **models.py**:
   - Defines the `Site`, `UserRecord`, and `JobExecution` models.

2. **tasks.py**:
   - Contains the `execute_task` function, a Celery shared task that processes tasks for a given `site_id`. It handles job status updates and adjusts processing duration based on task type.

3. **admin.py**:
   - Customizes the Django admin interface for `Site`, `UserRecord`, and `JobExecution` models, adding search, filters, and read-only fields for timestamps.

4. **views.py**:
   - **JobExecutionView**: Handles `POST` requests to schedule a job and trigger Celery tasks.
   - **SiteListView**: Handles `GET` requests to retrieve a list of all sites.

5. **urls.py**:
   - Maps URL patterns to views, enabling job execution and site listing APIs.

6. **serializers.py**:
   - `SiteSerializer`: Converts `Site` model instances into JSON data and vice versa.

---

