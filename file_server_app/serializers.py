# fileupload/serializers.py
from rest_framework import serializers
from .models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ('file_hash', 'file', 'created_at', 'uploaded_by_id', 'is_deleted')
        read_only_fields = ('file_hash', 'uploaded_by')

class MultipleFileUploadSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(
            max_length=None,
            allow_empty_file=False
        ),
        write_only=True
    )