from rest_framework import serializers

from api.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "id",
            "user",
            "title",
            "description",
            "url",
            "image",
            "link_type",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user"]
