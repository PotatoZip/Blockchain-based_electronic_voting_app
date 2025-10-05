from django.shortcuts import render
from django.utils import timezone
from django.db.models import QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from datetime import datetime, time
from .models import Election
from .serializers import ElectionListSerializer


def parse_date(d: str | None):
    if not d:
        return None
    try:
        dt = datetime.strptime(d, "%Y-%m-%d")
        return timezone.make_aware(dt)
    except ValueError:
        return None


class ElectionListView(ListAPIView):
    serializer_class = ElectionListSerializer

    def get_queryset(self) -> QuerySet[Election]:
        qs = Election.objects.all().order_by("-start_date")
        now = timezone.now()

        status_param = (self.request.query_params.get("status") or "all").lower()
        if status_param == "active":
            qs = qs.filter(start_date__lte=now, end_date__gte=now)
        elif status_param == "archive":
            qs = qs.filter(end_date__lt=now)
        elif status_param == "upcoming":
            qs = qs.filter(start_date__gt=now)

        date_from = parse_date(self.request.query_params.get("date_from"))
        date_to = parse_date(self.request.query_params.get("date_to"))
        if date_from:
            qs = qs.filter(start_date__gte=date_from)
        if date_to:
            end_of_day = timezone.make_aware(
                datetime.combine(date_to.date(), time(23, 59, 59))
            )
            qs = qs.filter(start_date__lte=end_of_day)

        return qs


class ElectionDetailView(RetrieveAPIView):
    queryset = Election.objects.all()
    serializer_class = ElectionListSerializer
