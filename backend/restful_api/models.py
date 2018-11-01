from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAttributes(models.Model):
    koins = models.DecimalField(..., max_digits=10, decimal_places=0)
    experience = models.DecimalField(..., max_digits=10, decimal_places=0)
    towers = models.DecimalField(..., max_digits=10, decimal_places=0)
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
        

class Vegetation(models.Model):
    ek72 = models.CharField(max_length=10)
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.ek72


class UserArea(models.Model):
    label = models.CharField(max_length=50)
    public = models.BooleanField()
    polygon = models.MultiPolygonField(4326)
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
        return request.user.is_authenticated

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        print(self.creator)
        return request.user == self.creator