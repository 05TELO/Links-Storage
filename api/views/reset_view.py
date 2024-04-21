import random
import string

from django.contrib.auth.models import User
from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ResetView(APIView):
    def post(self, request: Request) -> Response:
        email = request.data.get("email")
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+=-"
        new_password = "".join(random.choices(characters, k=12))
        user = get_object_or_404(User, email=email)
        user.set_password(new_password)
        user.save()

        try:
            send_mail(
                "Your new password",
                f"Your new password is: {new_password}",
                "from@example.com",
                [user.email],
                fail_silently=False,
            )
        except BadHeaderError:
            return Response(
                {"message": "Email not sent. Invalid header found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Email not sent. Error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "New password generated and sent to email"},
            status=status.HTTP_200_OK,
        )
