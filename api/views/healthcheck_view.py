from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthcheckView(APIView):
    """
    Perform health check.

    :param request: HTTP request object.
    :type request: Request

    :returns: JSON response with a health status message.
    :rtype: Response
    """

    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        return Response({"message": "healthy"})
