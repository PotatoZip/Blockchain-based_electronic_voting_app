"""URL configurations for the authentication app, including election-related endpoints"""

from django.urls import path
from .views import (
    ElectionListView,
    ElectionDetailView,
    VerifyView,
    CastVoteView,
    ChallengeView,
    ElectionResultsView,
)

urlpatterns = [
    path("elections/", ElectionListView.as_view(), name="election-list"),
    path("elections/<int:pk>/", ElectionDetailView.as_view(), name="election-detail"),
    path("auth/verify/", VerifyView.as_view(), name="verify"),
    path(
        "elections/<int:election_id>/vote/",
        CastVoteView.as_view(),
        name="cast-vote",
    ),
    path("auth/challenge/", ChallengeView.as_view(), name="auth-challenge"),
    path(
        "elections/<int:election_id>/results/",
        ElectionResultsView.as_view(),
        name="election-results",
    ),
]
