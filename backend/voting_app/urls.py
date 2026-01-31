"""URL configuration for voting_app project"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tools/", include("tools.urls")),
    path(
        "api/",
        include(("authentication.urls", "authentication"), namespace="authentication"),
    ),
]
