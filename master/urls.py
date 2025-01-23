from django.urls import path
from .views import TokenView, ValidateTokenView

urlpatterns = [
    path('token/', TokenView.as_view(), name='token'),
    path('validate_token/', ValidateTokenView.as_view(), name='validate_token'),
]
