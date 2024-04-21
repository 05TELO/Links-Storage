from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserLogin(APIView):
    """
    API endpoint for user login.

    :param request: The HTTP request object.
    :type request: Request

    :returns: JSON response with user authentication status and token if successful.
    :rtype: Response
    """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """
        Authenticate user based on email and password.

        :param request: HTTP request object containing user email and password.
        :type request: Request

        :returns: JSON response with user authentication status and token if successful.
        :rtype: Response
        """
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"message": "User authenticated successfully", "token": token.key},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )
