from typing import Any

from rest_framework import authentication
from rest_framework import permissions
from django.db import IntegrityError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Link
from api.og_parser import ParserOG
from api.serializers import LinkSerializer


class LinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing links.
    """

    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
    ]


    def perform_create(self, serializer: LinkSerializer) -> None:
        """
        Perform creation of a new link with user association.

        :param serializer: Serializer instance for link data.
        :type serializer: LinkSerializer
        """
        serializer.save(user=self.request.user)

    def get_queryset(self) -> Any:
        """
        Get queryset of links associated with the current user.

        :returns: QuerySet of links.
        :rtype: QuerySet
        """
        user = self.request.user
        return Link.objects.filter(user=user)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new link by extracting data from the URL.

        :param request: HTTP request object.
        :type request: Request

        :returns: JSON response with link data or error message.
        :rtype: Response
        """
        try:
            link = request.data["url"]
            data = ParserOG.extract_data_from_html(link)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except IntegrityError:
            return Response(
                {"error": "URL should be unique"}, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Delete a link.

        :param request: HTTP request object.
        :type request: Request

        :returns: JSON response with success message.
        :rtype: Response
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Link deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
