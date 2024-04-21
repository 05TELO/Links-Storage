from typing import Any

from django.core.management.base import BaseCommand

from api.models import CustomUser
from config_data import dirs
from config_data.config import load_config

conf = load_config(str(dirs.DIR_REPO / ".env"))


class Command(BaseCommand):
    """
    Create a superuser if none exist.
    Takes args from environment variables.
    """

    def handle(self, *args: Any, **options: Any) -> None:
        email = conf.django.superuser_email
        password = conf.django.superuser_password

        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(f"User '{email}' exists already")
            return

        CustomUser.objects.create_superuser(
            email=email,
            password=password,
        )

        self.stdout.write(f"Superuser '{email}' was created successfully")
        return
