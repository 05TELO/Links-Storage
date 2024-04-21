from typing import Any

from django.db import IntegrityError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Link
from api.og_parser import ParserOG
from api.serializers import LinkSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def perform_create(self, serializer: LinkSerializer) -> None:
        serializer.save(user=self.request.user)

    def get_queryset(self) -> Any:
        user = self.request.user
        return Link.objects.filter(user=user)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
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
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Link deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
