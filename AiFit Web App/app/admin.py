from django.contrib import admin
from app.models import *
from django.contrib.sessions.models import Session

admin.site.register(UserData)
admin.site.register(Record)
admin.site.register(Trainer_form)
admin.site.register(BlogModel)
admin.site.register(Session)

