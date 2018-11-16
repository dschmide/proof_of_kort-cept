from django.contrib import admin
from .models import UserAttributes
from .models import solvedMission
from .models import PlacedTower
from .models import PlacedLandmark

# Register all required Django DB Models
admin.site.register(UserAttributes)
admin.site.register(solvedMission)
admin.site.register(PlacedTower)
admin.site.register(PlacedLandmark)
