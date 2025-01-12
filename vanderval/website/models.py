from django.db import models

# Create your models here.
class Site(models.Model):
    RECORD_CAPACITY_LOW = 1  # user records between 500-10000
    RECORD_CAPACITY_MEDIUM = 2  # user records between 10000-50000
    RECORD_CAPACITY_HIGH = 3  # user records between 50000-200000

    RECORD_CAPACITY_CHOICES = (
        (RECORD_CAPACITY_LOW, "Low"),
        (RECORD_CAPACITY_MEDIUM, "Medium"),
        (RECORD_CAPACITY_HIGH, "High"),
    )
    name = models.CharField(max_length=100)
    domain = models.URLField()
    url = models.URLField()
    description = models.TextField()
    record_capicity = models.IntegerField(choices=RECORD_CAPACITY_CHOICES)

class UserRecords(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # do not count for active records if false

class JobExecution(models.Model):
    TASK_TYPE_CHOICES = [
        ("task_01", "Task 01"),
        ("task_02", "Task 02"),
        ("task_03", "Task 03"),
        ("task_04", "Task 04"),
        ("task_05", "Task 05"),
    ]
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=10, choices=TASK_TYPE_CHOICES)
    status = models.CharField(max_length=50, default="Pending")  # To track job status
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Job {self.task_type} for site {self.site.name} ({self.status})"
