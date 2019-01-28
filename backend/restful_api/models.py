from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

# Array Field for Tower locations
from django.contrib.postgres.fields import ArrayField


User = get_user_model()


class PlacedLandmark(models.Model):
    location = ArrayField(models.DecimalField(max_digits=18, decimal_places=15), size=2)
    label = models.CharField(max_length=99)
    owner = models.CharField(max_length=99)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('creator',)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_create_permission(request):
        return True

    @staticmethod
    def has_write_permission(request):
        return request.user.is_authenticated

    def has_object_write_permission(self, request):
        return request.user == self.creator


class PlacedTower(models.Model):
    location = ArrayField(models.DecimalField(max_digits=18, decimal_places=15), size=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('creator',)

    @staticmethod
    def has_read_permission(request):
        return request.user.is_authenticated

    def has_object_read_permission(self, request):
        return request.user.is_authenticated

    @staticmethod
    def has_create_permission(request):
        return True

    @staticmethod
    def has_write_permission(request):
        return request.user.is_authenticated

    def has_object_write_permission(self, request):
        return request.user == self.creator


class UserAttributes(models.Model):
    koins = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    experience = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    towers = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    landmarks = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tower_range = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    sight_range = models.DecimalField(default=0, max_digits=10, decimal_places=0)

    class Meta:
        ordering = ('creator',)

    @staticmethod
    def has_read_permission(request):
        return request.user.is_authenticated

    def has_object_read_permission(self, request):
        return request.user.is_authenticated

    @staticmethod
    def has_create_permission(request):
        return True

    @staticmethod
    def has_write_permission(request):
        return request.user.is_authenticated

    def has_object_write_permission(self, request):
        return request.user == self.creator


class solvedMission(models.Model):
    osmID = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    answer = models.CharField(max_length=99)
    solved_by = models.CharField(default=0, max_length=99)
    timestamp = models.DecimalField(default=0, max_digits=16, decimal_places=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('osmID', 'creator')

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_create_permission(request):
        return True

    @staticmethod
    def has_write_permission(request):
        return request.user.is_authenticated

    def has_object_write_permission(self, request):
        return request.user.is_authenticated
