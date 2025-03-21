from django.contrib import admin
from .models import Company

# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
