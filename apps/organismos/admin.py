from django.contrib import admin
from .models import Organism

class OrganismAdmin(admin.ModelAdmin):
    list_filter = (
        'organism_name',
    )

admin.site.register(Organism, OrganismAdmin)