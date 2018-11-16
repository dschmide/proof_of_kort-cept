from rest_framework import serializers
from restful_api.models import UserAttributes

from restful_api.models import solvedMission

from restful_api.models import PlacedTower

from restful_api.models import PlacedLandmark

from django.contrib.auth import get_user_model
User = get_user_model()


class PlacedLandmarksSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Or User.objects.filter(active=True)
        required=False,
        allow_null=True,
        default=None,
    )

    # Get the current user from request context
    def validate_creator(self, value):
        return self.context['request'].user

    class Meta:
        model = PlacedLandmark
        fields = ('location', 'label', 'owner', 'creator', 'id')


class PlacedTowersSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Or User.objects.filter(active=True)
        required=False,
        allow_null=True,
        default=None,
    )

    # Get the current user from request context
    def validate_creator(self, value):
        return self.context['request'].user

    class Meta:
        model = PlacedTower
        fields = ('location', 'creator', 'id')


class UserAttributesSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Or User.objects.filter(active=True)
        required=False,
        allow_null=True,
        default=None,
    )

    # Get the current user from request context
    def validate_creator(self, value):
        return self.context['request'].user

    class Meta:
        model = UserAttributes
        fields = ('koins', 'experience', 'towers', 'landmarks', 'creator', 'id', 'tower_range', 'sight_range')


class solvedMissionSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Or User.objects.filter(active=True)
        required=False,
        allow_null=True,
        default=None,
    )

    # Get the current user from request context
    def validate_creator(self, value):
        return self.context['request'].user

    class Meta:
        model = solvedMission
        fields = ('osmID', 'answer', 'solved_by', 'timestamp', 'creator', 'id')

