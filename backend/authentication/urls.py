from django.urls import path
from .views import ElectionListView, ElectionDetailView, VerifyVoterView

app_name = "authentication"

urlpatterns = [
    path("elections/", ElectionListView.as_view(), name="election-list"),
    path("elections/<int:pk>/", ElectionDetailView.as_view(), name="election-detail"),
    path(
        "elections/<int:election_id>/verify/", VerifyVoterView.as_view(), name="verify"
    ),
]
