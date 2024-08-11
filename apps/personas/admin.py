from django.contrib import admin

from .models import Province, Locality, Person

class LocalityAdmin(admin.ModelAdmin):
    list_filter = (
        'province_id',
        'locality_name'
    )

class ProvinceAdmin(admin.ModelAdmin):
    list_filter = (
        'province_name',
    )

class PersonAdmin(admin.ModelAdmin):
    list_filter = (
        'locality_id',
        'person_bg_center',
        'person_surname',
        'person_dni',
    )

admin.site.register(Province, ProvinceAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(Person, PersonAdmin)