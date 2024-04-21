from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import ChangePassword
from .views import CollectionViewSet
from .views import HealthcheckView
from .views import LinkViewSet
from .views import ResetView
from .views import UserLogin
from .views import UserRegister
from .views import schema_view

router = routers.DefaultRouter()
router.register(r"links", LinkViewSet, basename="link")
router.register(r"collections", CollectionViewSet, basename="collection")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("healthcheck/", HealthcheckView.as_view(), name="healthcheck"),
    path("register/", UserRegister.as_view(), name="user_registration"),
    path("login/", UserLogin.as_view(), name="user_login"),
    path("change_pass/", ChangePassword.as_view(), name="change_password"),
    path("reset_pass/", ResetView.as_view(), name="reset_password"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema_swagger_ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema_redoc"),
]
