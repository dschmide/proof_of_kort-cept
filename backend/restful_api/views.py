from django.db.models import Q
from rest_framework import viewsets

# User Attributes
from restful_api.models import UserAttributes
from restful_api.serializers import UserAttributesSerializer

# solved Missions
from restful_api.models import solvedMission
from restful_api.serializers import solvedMissionSerializer

# placed Towers
from restful_api.models import PlacedTower
from restful_api.serializers import PlacedTowersSerializer

# placed Landmarks
from restful_api.models import PlacedLandmark
from restful_api.serializers import PlacedLandmarksSerializer

# DRY Permission package
from dry_rest_permissions.generics import DRYPermissions


class placedLandmarksViewSet(viewsets.ModelViewSet):
    permission_classes = (DRYPermissions,)
    queryset = PlacedLandmark.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return PlacedLandmark.objects.all()
    serializer_class = PlacedLandmarksSerializer
    http_method_names = ['get', 'put', 'delete', 'post']


class placedTowersViewSet(viewsets.ModelViewSet):
    permission_classes = (DRYPermissions,)
    queryset = PlacedTower.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return PlacedTower.objects.filter(Q(creator=self.request.user))  # noqa
    serializer_class = PlacedTowersSerializer
    http_method_names = ['get', 'put', 'delete', 'post']

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
