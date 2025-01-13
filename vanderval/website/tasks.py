from celery import shared_task
from .models import Site, UserRecords, JobExecution
import logging
from time import sleep
from django.utils import timezone

logger = logging.getLogger(__name__)

from celery import shared_task

@shared_task
def execute_task(task_type, site_id):
    if not task_type or not site_id:
        logger.error("Error: site_id and task_type are required")
        return {"error": "site_id and task_type are required"}

    TASK_MULTIPLIERS = {
        "task_01": 0.001,
        "task_02": 0.01,
        "task_03": 0.1,
        "task_04": 1,
        "task_05": 10,
    }

    time_multiplier = TASK_MULTIPLIERS.get(task_type)
    logger.info("Time multiplier: {}".format(time_multiplier))
    if not time_multiplier:
        logger.error("Invalid task type: {}".format(task_type))
        return False

    try:
        site = Site.objects.get(id=site_id)
        logger.info("Site: {}".format(site))
        records = UserRecords.objects.filter(site=site)
        logger.info("Records: {}".format(records))

        # Ensure job is created and status is set to 'Pending'
        job, created = JobExecution.objects.get_or_create(site=site, task_type=task_type, status="Pending")

        # Update job status to 'Started' and set the current time as started_at
        job.status = "Started"
        job.started_at = timezone.now()  # Set the current time here
        job.save()

        logger.info("Job {} started for site {}.".format(task_type, site_id))

        # Log the number of records to check the process duration
        logger.info("Processing {} records for site {}.".format(records.count(), site_id))

        # If there are records, sleep the total time for task_05
        logger.info("Records exist: {}".format(records.exists()))
        if records.exists():
            # Adjust sleep time for task_05 to total 60 seconds
            sleep(time_multiplier)

        # After completing task, update the job status to 'Completed'
        job.status = "Completed"
        job.finished_at = timezone.now()  # Set the current time when the task is finished
        job.save()

        logger.info("Job {} completed for site {}.".format(task_type, site_id))
        return True
    except Site.DoesNotExist:
        logger.error("Site with id {} does not exist".format(site_id))
        return False