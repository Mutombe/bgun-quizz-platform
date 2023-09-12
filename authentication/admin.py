from django.contrib import admin
from .models import UserProfile
class AdminProfileOverview(admin.ModelAdmin):
    list_display = ("location","user",)
    search_fields = ("interests",)
    ordering = ("location", "user",)
    list_filter = ("user",)
    


admin.site.register(UserProfile, AdminProfileOverview)
