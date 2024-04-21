from typing import Any

from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Collection
from api.serializers import CollectionSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing collections.
    """

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer: CollectionSerializer) -> None:
        """
        Perform creation of a new collection with associated links.

        :param serializer: Serializer instance for collection data.
        :type serializer: CollectionSerializer
        """
        links = self.request.data.get("links", [])
        collection = serializer.save(user=self.request.user)
        collection.links.add(*links)

    def get_queryset(self) -> Any:
        """
        Get queryset of collections associated with the current user.

        :returns: QuerySet of collections.
        :rtype: QuerySet
        """
        user = self.request.user
        return Collection.objects.filter(user=user)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Delete a collection.

        :param request: HTTP request object.
        :type request: Request

        :returns: JSON response with success message.
        :rtype: Response
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Collection deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
