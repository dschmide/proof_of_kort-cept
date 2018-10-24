from django.core.management.base import BaseCommand
import os
from django.contrib.gis.utils import LayerMapping
from restful_api.models import Vegetation