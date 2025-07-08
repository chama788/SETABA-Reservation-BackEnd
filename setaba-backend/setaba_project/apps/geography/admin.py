from django.contrib import admin
from .models import *

@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code_iso_2', 'code_iso_3', 'indicatif_tel', 'devise', 'actif')
    list_filter = ('actif', 'devise', 'created_at')
    search_fields = ('nom', 'code_iso_2', 'code_iso_3', 'indicatif_tel')
    ordering = ('nom',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'code_iso_2', 'code_iso_3')
        }),
        ('Communication', {
            'fields': ('indicatif_tel', 'devise', 'fuseau_horaire')
        }),
        ('Statut', {
            'fields': ('actif',)
        }),
    )

@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'pays_nom', 'code_postal', 'population', 'actif')
    list_filter = ('pays', 'actif', 'created_at')
    search_fields = ('nom', 'pays__nom', 'code_postal')
    autocomplete_fields = ('pays',)
    ordering = ('pays__nom', 'nom')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('pays', 'nom', 'code_postal')
        }),
        ('Géolocalisation', {
            'fields': ('latitude', 'longitude', 'altitude')
        }),
        ('Démographie', {
            'fields': ('population',)
        }),
        ('Statut', {
            'fields': ('actif',)
        }),
    )
    
    def pays_nom(self, obj):
        return obj.pays.nom
    pays_nom.short_description = 'Pays'

@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville_nom', 'pays_nom', 'code_postal', 'actif')
    list_filter = ('ville__pays', 'ville', 'actif', 'created_at')
    search_fields = ('nom', 'ville__nom', 'ville__pays__nom', 'code_postal')
    autocomplete_fields = ('ville',)
    ordering = ('ville__pays__nom', 'ville__nom', 'nom')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('ville', 'nom', 'code_postal')
        }),
        ('Géolocalisation', {
            'fields': ('latitude', 'longitude')
        }),
        ('Statut', {
            'fields': ('actif',)
        }),
    )
    
    def ville_nom(self, obj):
        return obj.ville.nom
    ville_nom.short_description = 'Ville'
    
    def pays_nom(self, obj):
        return obj.ville.pays.nom
    pays_nom.short_description = 'Pays'
