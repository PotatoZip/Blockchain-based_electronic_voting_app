from django.urls import path
from .views import send_view

urlpatterns = [
    path("send-emails/<int:voting_id>/", send_view),
]
