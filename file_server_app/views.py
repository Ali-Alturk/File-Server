# fileupload/views.py
import logging
from celery.result import AsyncResult
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FileUpload
from .serializers import FileUploadSerializer
from .tasks import process_uploaded_file, process_multiple_files

logger = logging.getLogger(__name__)


class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FileUpload.objects.filter(
            uploaded_by=self.request.user,
            is_deleted=False
        )

    @action(detail=False, methods=['POST'])
    def upload_file(self, request):
        if request.FILES['file'].size > 52428800:
            return HttpResponse("Maximum file size allowed is 50MB", status=400)
        try:
            file_obj = request.FILES.get('file')
            if not file_obj:
                return Response(
                    {'error': 'No file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create and save the file upload
            file_upload = FileUpload(
                file=file_obj,
                uploaded_by=request.user,
                original_filename=file_obj.name,
                status='pending'
            )
            file_upload.save()

            # Use file_hash as the primary key
            file_hash = file_upload.file_hash
            logger.info(f"Dispatching task for file hash: {file_hash}")

            # Pass the file_hash as the ID
            task = process_uploaded_file.delay(file_hash)
            logger.info(f"Task dispatched with ID: {task.id}")

            return Response({
                'task_id': task.id,
                'file_hash': file_hash,
                'status': 'processing'
            }, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            logger.error(f"Error in upload_file: {str(e)}")
            return Response({
                'error': f"Failed to process file: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'])
    def upload_multiple(self, request):
        try:
            files = request.FILES.getlist('files')
            if not files:
                return Response(
                    {'error': 'No files provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Maximum file size in bytes (50MB)
            max_size = 52428800

            # Check all files for size limit
            oversize_files = []
            for file_obj in files:
                if file_obj.size > max_size:
                    oversize_files.append(file_obj.name)

            # If any files are too large, return error
            if oversize_files:
                error_message = "The following files exceed the 50MB limit: " + ", ".join(oversize_files)
                return Response(
                    {'error': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save all files and collect their hashes
            file_hashes = []
            for file_obj in files:
                file_upload = FileUpload(
                    file=file_obj,
                    uploaded_by=request.user,
                    original_filename=file_obj.name,
                    status='pending'
                )
                file_upload.save()
                file_hashes.append(file_upload.file_hash)
                logger.info(f"Saved file with hash: {file_upload.file_hash}")

            # Process all files by hash
            logger.info(f"Dispatching task for multiple files: {file_hashes}")
            task = process_multiple_files.delay(file_hashes)
            logger.info(f"Task dispatched with ID: {task.id}")

            return Response({
                'task_id': task.id,
                'file_hashes': file_hashes,
                'status': 'processing'
            }, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.error(f"Error in upload_multiple: {str(e)}")
            return Response({
                'error': f"Failed to process files: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'])
    def check_task_status(self, request):
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response(
                {'error': 'No task_id provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get task result from Celery
        task = AsyncResult(task_id)
        return Response({
            'task_id': task_id,
            'status': task.status,
            'result': task.result if task.ready() else None
        })