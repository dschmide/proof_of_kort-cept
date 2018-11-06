from django.db.models import Q
from rest_framework import viewsets

# User Attributes
from restful_api.models import UserAttributes
from restful_api.serializers import UserAttributesSerializer

# User Attributes
from restful_api.models import solvedMission
from restful_api.serializers import solvedMissionSerializer

# DRY Permission package
from dry_rest_permissions.generics import DRYPermissions


class UserAttributesViewSet(viewsets.ModelViewSet):
    permission_classes = (DRYPermissions,)
    queryset = UserAttributes.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserAttributes.objects.filter(Q(creator=self.request.user))  # noqa
    serializer_class = UserAttributesSerializer
    http_method_names = ['get', 'put', 'delete', 'post']

class solvedMissionViewSet(viewsets.ModelViewSet):
    permission_classes = (DRYPermissions,)
    queryset = solvedMission.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return solvedMission.objects.filter(Q(creator=self.request.user))  # noqa
    serializer_class = solvedMissionSerializer
    http_method_names = ['get', 'put', 'delete', 'post']
