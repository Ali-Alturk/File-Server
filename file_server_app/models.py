# fileupload/models.py
import hashlib
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_file_size(value):
    filesize = value.size
    if filesize > 52428800:  # 50MB in bytes
        raise ValidationError("Maximum file size allowed is 50MB")


class FileUpload(models.Model):
    file_hash = models.CharField(
        max_length=64,
        primary_key=True,
        editable=False
    )
    file = models.FileField(
        upload_to='uploads/',
        validators=[validate_file_size]
    )
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def generate_file_hash(self):
        import time
        import random
        import string
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        hash_string = f"{time.time()}{random_string}{self.file.name}"
        return hashlib.sha256(hash_string.encode()).hexdigest()

    def save(self, *args, **kwargs):
        if not self.file_hash:
            self.file_hash = self.generate_file_hash()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file_hash} - {self.file.name}"


# fileupload/models.py
class TaskStatus(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    result = models.JSONField(null=True)

    class Meta:
        ordering = ['-created_at']