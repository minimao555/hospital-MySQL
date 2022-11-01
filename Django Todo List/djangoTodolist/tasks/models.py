from django.db import models
from django.utils import timezone


# Create your models here.
class Task(models.Model):
	title = models.CharField(max_length=20)
	description = models.CharField(max_length=200, blank=True)
	complete = models.BooleanField(default=False)
	has_due_date = models.BooleanField(default=False)
	due_date = models.DateField(default=timezone.now)
	create_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title
