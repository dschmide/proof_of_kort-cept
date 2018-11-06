from django.contrib import admin
from .models import UserAttributes
from .models import solvedMission

# Register all required Django DB Models
admin.site.register(UserAttributes)
admin.site.register(solvedMission)