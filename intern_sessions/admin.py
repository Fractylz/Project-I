from django.contrib import admin
from .models import Session

# Register your models here.


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
