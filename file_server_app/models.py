from django.db import models
from django.contrib.auth.models import User


class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.file.name} - {self.uploaded_by.username}"