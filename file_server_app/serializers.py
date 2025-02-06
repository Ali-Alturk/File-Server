from rest_framework import serializers
from .models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ('id', 'file', 'is_deleted', 'uploaded_at')
        read_only_fields = ('uploaded_by',)