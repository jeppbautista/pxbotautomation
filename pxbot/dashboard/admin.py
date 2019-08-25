from django.contrib import admin

from .models import TransactionLog, User, Config

admin.site.register(TransactionLog)
admin.site.register(User)
admin.site.register(Config)