from django.apps import AppConfig
from aifit.settings import BASE_DIR
import os

class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
