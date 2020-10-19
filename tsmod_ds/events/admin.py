from django.contrib import admin
from .models import UserScore, Token, NewEvents

admin.site.register(UserScore)
admin.site.register(Token)
admin.site.register(NewEvents)