from email.message import Message
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Partner)
admin.site.register(Admin)
admin.site.register(Playlist)
admin.site.register(Video)
admin.site.register(Ecran)
admin.site.register(VideoEcran)

