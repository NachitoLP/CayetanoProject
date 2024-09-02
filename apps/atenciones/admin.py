from django.contrib import admin
from .models import Reason, Service, Headquarter
# Register your models here.

class ReasonAdmin(admin.ModelAdmin):
    list_filter = (
        'service_reason',
    )
class HeadquarterAdmin(admin.ModelAdmin):
    list_filter = (
        'headquarter_name',
    )

class ServiceAdmin(admin.ModelAdmin):
    list_filter = (
        'service_reason_id',
        'service_date',
        'service_status',
        'organism_id'
    )
    list_display = (
        'formatted_service_date',
        'person_id',
        'formatted_service_modified_date',
    )
    

admin.site.register(Reason, ReasonAdmin)
admin.site.register(Headquarter, HeadquarterAdmin)
admin.site.register(Service, ServiceAdmin)