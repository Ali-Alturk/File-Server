# fileupload/tasks.py
import hashlib
import os
import logging
from celery import shared_task
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


@shared_task
def process_uploaded_file(file_hash):
    from .models import FileUpload  # Import here to avoid circular imports

    try:
        logger.info(f"Processing file upload with hash: {file_hash}")

        # Get the FileUpload by its file_hash primary key
        file_upload = FileUpload.objects.get(file_hash=file_hash)

        # Read file content for processing (if needed)
        with file_upload.file.open('rb') as f:
            file_content = f.read()

        # Update the status
        file_upload.status = 'processed'
        file_upload.save()

        logger.info(f"Successfully processed file: {file_hash}")
        return {
            'status': 'success',
            'file_hash': file_hash
        }
    except Exception as e:
        logger.error(f"Error processing file {file_hash}: {str(e)}")
        return {
            'status': 'error',
            'file_hash': file_hash,
            'error': str(e)
        }


@shared_task
def process_multiple_files(file_hashes):
    results = []
    logger.info(f"Processing multiple files with hashes: {file_hashes}")

    for file_hash in file_hashes:
        try:
            # Process each file
            result = process_uploaded_file(file_hash)
            results.append(result)
        except Exception as e:
            logger.error(f"Error in multiple files task for file {file_hash}: {str(e)}")
            results.append({
                'status': 'error',
                'file_hash': file_hash,
                'error': str(e)
            })

    return results