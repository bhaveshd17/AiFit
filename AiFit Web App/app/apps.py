from django.apps import AppConfig
from aifit.settings import BASE_DIR
from tensorflow.keras.models import load_model
import os

class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
    MODEL_PATH = os.path.join(BASE_DIR, 'best_model_V2.h5')
    aifit_lrcn_model = load_model(MODEL_PATH)
