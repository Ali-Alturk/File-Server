import requests
from django.conf import settings

def validate_token(token):
    response = requests.post(f"{settings.MASTER_URL}/master/validate_token/", data={"token": token})
    return response.status_code == 200
