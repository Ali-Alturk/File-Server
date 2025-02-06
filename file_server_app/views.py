# fileupload/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import FileUpload
from .serializers import FileUploadSerializer

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def get_queryset(self):
        return FileUpload.objects.filter(uploaded_by=self.request.user)