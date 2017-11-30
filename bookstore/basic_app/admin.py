from django.contrib import admin
from basic_app.models import UserProfileInfo, User, BookCatalogue

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(BookCatalogue)
