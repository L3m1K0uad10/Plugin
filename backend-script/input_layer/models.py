from django.db import models
from django.utils import timezone


class Input(models.Model):
    code = models.TextField(blank = False)
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(auto_now = True)

    def __code__(self):
        return f"code {self.id}"