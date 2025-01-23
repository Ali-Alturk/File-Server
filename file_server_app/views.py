from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import validate_token  # Assuming this function validates the token

class FileUploadView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', '').replace('Token ', '')

        # Validate the token using your custom validation logic
        if not validate_token(token):
            return Response({"error": "Invalid token"}, status=401)

        # Process the uploaded file
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=400)

        # Save the file or process as needed
        return Response({"message": "File uploaded successfully"}, status=200)

