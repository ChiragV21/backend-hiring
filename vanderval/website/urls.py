from django.urls import path
from .views import JobExecutionView, SiteListView

urlpatterns = [
    path("jobs/", JobExecutionView.as_view(), name="job-execution"),
    path("sites/", SiteListView.as_view(), name="site-list"),
]
