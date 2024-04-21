from rest_framework import permissions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import UserSerializer


class UserRegister(APIView):
    """
    API endpoint for user registration.

    :permission_classes: [permissions.AllowAny]

    :param request: The HTTP request object.
    :type request: Request

    :returns: JSON response with registration status message or error.
    :rtype: Response
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request) -> Response:
        """
        Register a new user.

        :param request: HTTP request object containing user data.
        :type request: Request

        :returns: JSON response with registration status message or error.
        :rtype: Response
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": f"{user} successfully registered"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
