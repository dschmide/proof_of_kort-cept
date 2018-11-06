from rest_framework import serializers
from restful_api.models import UserAttributes

from restful_api.models import solvedMission


from django.contrib.auth import get_user_model
User = get_user_model()


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
        fields = ('koins', 'experience', 'towers', 'creator', 'id', 'tower_range', 'sight_range')


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
        fields = ('osmID', 'answer', 'creator', 'id')

