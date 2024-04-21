from django.contrib import admin

from api.models import Collection
from api.models import CustomUser
from api.models import Link


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email",)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "description",
        "url",
        "image",
        "link_type",
        "created_at",
        "updated_at",
    )


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "description", "created_at", "updated_at")
