from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Token
from django.shortcuts import get_object_or_404


class TokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({"token": str(token.token)})

class ValidateTokenView(APIView):
    def post(self, request):
        token = request.data.get('token')
        token_obj = get_object_or_404(Token, token=token)
        return Response({"valid": True})
