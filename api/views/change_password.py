from rest_framework import permissions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ChangePassword(APIView):
    """
    API endpoint for changing user password.

    :permission_classes: [permissions.IsAuthenticated]

    :param request: The HTTP request object.
    :type request: Request

    :returns: JSON response with a message indicating the success of password change.
    :rtype: Response
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Change user password.

        :param request: HTTP request object containing user data and new password.
        :type request: Request

        :returns: JSON response with a message indicating the success of password change.
        :rtype: Response
        """
        user = request.user
        new_password = str(request.data.get("new_password"))

        if user.check_password(new_password):
            return Response(
                {"message": "New password cannot be the same as the old password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully"})
