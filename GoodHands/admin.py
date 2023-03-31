from django.contrib import admin
from GoodHands.models import Institution

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')  # Wyświetla pola 'name' i 'type' na liście rekordów.
    list_filter = ('type',)  # Dodaje filtr po polu 'type'.
    search_fields = ('name',)  # Dodaje pole wyszukiwania po nazwie instytucji.

admin.site.register(Institution, InstitutionAdmin)
