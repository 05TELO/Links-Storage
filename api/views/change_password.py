from rest_framework import permissions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ChangePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
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
