"""Routes."""

# Django
from django.urls import path

from . import __app_name__, views

app_name: str = __app_name__  # pylint: disable=invalid-name

urlpatterns = [
    path("", views.index, name="index"),
]
