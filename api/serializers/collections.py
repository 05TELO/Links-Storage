from rest_framework import serializers

from api.models import Collection

from .links import LinkSerializer


class CollectionSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = [
            "id",
            "user",
            "title",
            "description",
            "links",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user"]
