from django.db import models

from .user import CustomUser


class Link(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True, unique=True)
    image = models.URLField(blank=True, null=True)
    link_type = models.CharField(max_length=255)
    collections = models.ManyToManyField("Collection", related_name="links")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
