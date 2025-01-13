from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Site, JobExecution
from .serializers import SiteSerializer
from .tasks import execute_task
import logging

logger = logging.getLogger(__name__)

class JobExecutionView(APIView):
    def post(self, request, *args, **kwargs):
        site_id = request.data.get("site_id")
        task_type = request.data.get("task_type")
        
        # Validate input
        if not site_id or not task_type:
            return Response({"error": "site_id and task_type are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            site = Site.objects.get(id=site_id)
        except Site.DoesNotExist:
            return Response(
                {"error": "Site with id {} does not exist".format(site_id)},
                status=status.HTTP_404_NOT_FOUND
            )

        # Save job execution request
        job = JobExecution.objects.create(
            site=site,
            task_type=task_type,
            status="Pending"  # Job is pending until executed
        )

        # Log the request
        logger.info("Job execution request saved: task_type={}, site_id={}".format(task_type, site_id))

        # Trigger the asynchronous task
        execute_task.delay(task_type, site_id)

        return Response(
            {
                "message": "Task {} scheduled for site {}".format(task_type, site_id),
                "job_id": job.id
            },
            status=status.HTTP_202_ACCEPTED
        )

class SiteListView(APIView):
    def get(self, request, *args, **kwargs):
        sites = Site.objects.all()
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
