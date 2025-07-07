from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('email', 'get_nom_complet', 'email_verifie', 'telephone_verifie', 'is_active', 'created_at')
    list_filter = ('email_verifie', 'telephone_verifie', 'is_active', 'mfa_active', 'created_at')
    search_fields = ('email', 'telephone', 'profil__nom', 'profil__prenom')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('telephone', 'langue_preferee')}),
        ('Vérifications', {'fields': ('email_verifie', 'telephone_verifie')}),
        ('Sécurité MFA', {'fields': ('mfa_active', 'mfa_type', 'mfa_secret')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Sécurité avancée', {'fields': ('bloque', 'raison_blocage', 'tentatives_connexion', 'bloque_jusqu')}),
        ('Consentements', {'fields': ('accepte_conditions', 'version_conditions', 'accepte_marketing')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined', 'derniere_maj_mdp')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'telephone', 'password1', 'password2'),
        }),
    )
    
    def get_nom_complet(self, obj):
        try:
            return obj.profil.nom_complet
        except:
            return "Profil non créé"
    get_nom_complet.short_description = 'Nom complet'

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'utilisateur_email', 'pays', 'ville', 'profession', 'visibilite_profil')
    list_filter = ('genre', 'pays', 'ville', 'visibilite_profil', 'created_at')
    search_fields = ('nom', 'prenom', 'utilisateur__email', 'profession', 'societe')
    autocomplete_fields = ('utilisateur', 'pays', 'ville')
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('utilisateur', 'nom', 'prenom', 'date_naissance', 'genre', 'photo_url')
        }),
        ('Localisation', {
            'fields': ('adresse', 'pays', 'ville', 'code_postal', 'coordonnees_gps')
        }),
        ('Professionnel', {
            'fields': ('profession', 'societe', 'bio', 'site_web')
        }),
        ('Notifications', {
            'fields': ('notification_email', 'notification_sms', 'notification_push')
        }),
        ('Confidentialité', {
            'fields': ('visibilite_profil',)
        }),
    )
    
    def utilisateur_email(self, obj):
        return obj.utilisateur.email
    utilisateur_email.short_description = 'Email utilisateur'

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'code', 'niveau', 'actif', 'created_at')
    list_filter = ('actif', 'niveau', 'created_at')
    search_fields = ('code', 'libelle', 'description')
    ordering = ('-niveau', 'libelle')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('code', 'libelle', 'description')
        }),
        ('Hiérarchie et permissions', {
            'fields': ('niveau', 'permissions')
        }),
        ('Statut', {
            'fields': ('actif',)
        }),
    )

@admin.register(UtilisateurRole)
class UtilisateurRoleAdmin(admin.ModelAdmin):
    list_display = ('utilisateur_email', 'role_libelle', 'date_attribution', 'date_expiration', 'actif')
    list_filter = ('role', 'actif', 'date_attribution', 'date_expiration')
    search_fields = ('utilisateur__email', 'role__libelle', 'attribue_par__email')
    autocomplete_fields = ('utilisateur', 'role', 'attribue_par')
    
    def utilisateur_email(self, obj):
        return obj.utilisateur.email
    utilisateur_email.short_description = 'Utilisateur'
    
    def role_libelle(self, obj):
        return obj.role.libelle
    role_libelle.short_description = 'Rôle'

@admin.register(CodeOTP)
class CodeOTPAdmin(admin.ModelAdmin):
    list_display = ('utilisateur_email', 'type_code', 'code', 'is_utilise', 'is_expired', 'created_at')
    list_filter = ('type_code', 'created_at', 'expire_at', 'utilise_at')
    search_fields = ('utilisateur__email', 'code', 'email_cible', 'telephone_cible')
    readonly_fields = ('code', 'utilise_at')
    
    fieldsets = (
        ('Code OTP', {
            'fields': ('utilisateur', 'code', 'type_code')
        }),
        ('Cibles', {
            'fields': ('email_cible', 'telephone_cible')
        }),
        ('Sécurité', {
            'fields': ('tentatives_utilisation', 'max_tentatives', 'expire_at', 'utilise_at')
        }),
        ('Traçabilité', {
            'fields': ('adresse_ip_creation',)
        }),
    )
    
    def utilisateur_email(self, obj):
        return obj.utilisateur.email
    utilisateur_email.short_description = 'Utilisateur'
    
    def is_utilise(self, obj):
        return obj.utilise_at is not None
    is_utilise.boolean = True
    is_utilise.short_description = 'Utilisé'
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expiré'

@admin.register(SessionUtilisateur)
class SessionUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur_email', 'adresse_ip', 'date_creation', 'date_expiration', 'actif', 'is_expired')
    list_filter = ('actif', 'date_creation', 'date_expiration')
    search_fields = ('utilisateur__email', 'adresse_ip', 'user_agent')
    readonly_fields = ('token_session',)
    
    def utilisateur_email(self, obj):
        return obj.utilisateur.email
    utilisateur_email.short_description = 'Utilisateur'
