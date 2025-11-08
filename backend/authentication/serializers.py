from rest_framework import serializers
from django.utils import timezone
from .models import Election, Choice


class ElectionListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = ["id", "name", "description", "start_date", "end_date", "status"]

    def get_status(self, obj):
        now = timezone.now()
        if obj.end_date < now:
            return "archive"
        if obj.start_date > now:
            return "upcoming"
        return "active"


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "name", "description")


class ElectionDetailSerializer(serializers.ModelSerializer):
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
        now = timezone.now()
        if obj.end_date < now:
            return "archive"
        if obj.start_date > now:
            return "upcoming"
        return "active"
