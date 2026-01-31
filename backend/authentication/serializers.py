from rest_framework import serializers
from django.utils import timezone
from .models import Election, Choice


def status_for_election(obj: Election, now=None) -> str:
    """Return textual status for an election: 'archive' | 'upcoming' | 'active'

    If `now` is not provided, uses timezone.now(). Allowing `now` to be injected via
    serializer context ensures consistent computation across list/detail responses
    """
    _now = now or timezone.now()
    if obj.end_date < _now:
        return "archive"
    if obj.start_date > _now:
        return "upcoming"
    return "active"


class ElectionListSerializer(serializers.ModelSerializer):
    """Serializer for listing elections with status field"""

    status = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = ["id", "name", "description", "start_date", "end_date", "status"]

    def get_status(self, obj):
        now = self.context.get("now")
        return status_for_election(obj, now)


class ChoiceSerializer(serializers.ModelSerializer):
    """Serializer for election choices/options"""

    class Meta:
        model = Choice
        fields = ("id", "name", "description")


class ElectionDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed election view including choices and status"""

    choices = ChoiceSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "status",
            "choices",
        ]

    def get_status(self, obj):
        now = self.context.get("now")
        return status_for_election(obj, now)
