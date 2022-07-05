from django.db import models
from django.utils import timezone

class Item(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    # timezone.now respects in USE_TZ in settings.py
    modified_at = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)