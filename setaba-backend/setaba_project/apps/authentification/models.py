"""
Modèles utilisateur personnalisés avec gestion des rôles, profils, sessions,
OTP et sécurité renforcée (MFA, RGPD, connexions sécurisées).
"""

import secrets
import uuid
import string
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Role(models.Model):
    """Rôles utilisateurs avec hiérarchie et permissions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    libelle = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    niveau = models.IntegerField(default=0, help_text="Niveau hiérarchique (0-100)")
    permissions = models.JSONField(default=dict, help_text="Permissions spécifiques en format JSON")
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Table des rôles avec contraintes d'unicité et ordre"""
        db_table = 'roles'
        verbose_name = 'Rôle'
        verbose_name_plural = 'Rôles'
        ordering = ['-niveau', 'libelle']

    def __str__(self):
        return str(self.libelle)

class Utilisateur(AbstractUser):
    """Utilisateur personnalisé avec sécurité renforcée"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    email_verifie = models.BooleanField(default=False)
    telephone = PhoneNumberField(unique=True)
    telephone_verifie = models.BooleanField(default=False)

    # Sécurité MFA
    mfa_active = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=100, blank=True)
    mfa_type = models.CharField(max_length=20, default='SMS', choices=[
        ('SMS', 'SMS'),
        ('EMAIL', 'Email'),
        ('TOTP', 'TOTP'),
        ('APP', 'Application')
    ])
    cles_de_recuperation = models.JSONField(default=list, help_text="Clés de récupération MFA")

    # Connexion et sécurité
    derniere_connexion = models.DateTimeField(null=True, blank=True)
    ip_derniere_connexion = models.GenericIPAddressField(null=True, blank=True)
    tentatives_connexion = models.IntegerField(default=0)
    bloque_jusqu = models.DateTimeField(null=True, blank=True)
    actif = models.BooleanField(default=True)
    bloque = models.BooleanField(default=False)
    raison_blocage = models.TextField(blank=True)

    # Mot de passe
    derniere_maj_mdp = models.DateTimeField(default=timezone.now)
    force_changement_mdp = models.BooleanField(default=False)

    # Consentements RGPD
    accepte_conditions = models.BooleanField(default=False)
    version_conditions = models.CharField(max_length=10, blank=True)
    accepte_marketing = models.BooleanField(default=False)

    # Préférences
    langue_preferee = models.CharField(max_length=10, default='fr')

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['telephone']

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Table des utilisateurs avec contraintes d'unicité et options de gestion"""
        db_table = 'utilisateurs'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.email

    def is_account_verified(self):
        """Vérifie si le compte est complètement vérifié"""
        return self.email_verifie and self.telephone_verifie

class Profil(models.Model):
    """Profil détaillé des utilisateurs"""
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre')
    ]

    VISIBILITE_CHOICES = [
        ('public', 'Public'),
        ('prive', 'Privé'),
        ('amis', 'Amis seulement')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='profil')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, blank=True)
    photo_url = models.URLField(max_length=500, blank=True)

    # Adresse
    adresse = models.TextField(blank=True)
    ville = models.ForeignKey('geography.Ville', on_delete=models.SET_NULL, null=True, blank=True)
    pays = models.ForeignKey('geography.Pays', on_delete=models.PROTECT)
    code_postal = models.CharField(max_length=20, blank=True)
    coordonnees_gps = models.JSONField(
        null=True, blank=True, help_text="Coordonnées GPS {lat, lng}")

    # Professionnel
    profession = models.CharField(max_length=100, blank=True)
    societe = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    site_web = models.URLField(blank=True)

    # Notifications
    notification_email = models.BooleanField(default=True)
    notification_sms = models.BooleanField(default=True)
    notification_push = models.BooleanField(default=True)

    # Confidentialité
    visibilite_profil = models.CharField(
        max_length=20, choices=VISIBILITE_CHOICES, default='public')

    # Activité
    derniere_activite = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Table des profils utilisateurs avec contraintes d'unicité et options de gestion"""
        db_table = 'profils'
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    @property
    def nom_complet(self):
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.prenom} {self.nom}"

class UtilisateurRole(models.Model):
    """Association utilisateurs-rôles avec traçabilité"""
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_attribution = models.DateTimeField(default=timezone.now)
    attribue_par = models.ForeignKey(
        Utilisateur, on_delete=models.SET_NULL, null=True, related_name='roles_attribues')
    date_expiration = models.DateTimeField(null=True, blank=True)
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Table des attributions de rôles avec contraintes d'unicité et options de gestion"""
        db_table = 'utilisateurs_roles'
        unique_together = ['utilisateur', 'role']
        verbose_name = 'Attribution de rôle'
        verbose_name_plural = 'Attributions de rôles'

    def __str__(self):
        """Retourne une représentation lisible de l'association utilisateur-rôle"""
        utilisateur_email = getattr(self.utilisateur, 'email', 'Inconnu')
        role_libelle = getattr(self.role, 'libelle', 'Rôle inconnu')
        return f"{utilisateur_email} - {role_libelle}"

class SessionUtilisateur(models.Model):
    """Gestion des sessions utilisateurs actives"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='sessions')
    token_session = models.CharField(max_length=255, unique=True)
    adresse_ip = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_expiration = models.DateTimeField()
    derniere_activite = models.DateTimeField(default=timezone.now)
    actif = models.BooleanField(default=True)

    class Meta:
        """Table des sessions utilisateurs avec contraintes d'unicité et options de gestion"""
        db_table = 'sessions_utilisateur'
        verbose_name = 'Session utilisateur'
        verbose_name_plural = 'Sessions utilisateurs'

    def __str__(self):
        email = getattr(self.utilisateur, 'email', 'Inconnu')
        token_part = str(self.token_session)[:6]
        return f"Session {email} ({token_part}...)"

    def is_expired(self):
        """Vérifie si la session a expiré"""
        return timezone.now() > self.date_expiration

class CodeOTP(models.Model):
    """Codes OTP pour vérification email/téléphone"""
    TYPE_CHOICES = [
        ('email_verification', 'Vérification email'),
        ('phone_verification', 'Vérification téléphone'),
        ('password_reset', 'Réinitialisation mot de passe'),
        ('login_verification', 'Vérification connexion'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='codes_otp')
    code = models.CharField(max_length=6)
    type_code = models.CharField(max_length=30, choices=TYPE_CHOICES)
    email_cible = models.EmailField(
        blank=True, help_text="Email à vérifier si différent de l'actuel")
    telephone_cible = PhoneNumberField(
        blank=True, help_text="Téléphone à vérifier si différent de l'actuel")
    tentatives_utilisation = models.IntegerField(default=0)
    max_tentatives = models.IntegerField(default=3)
    expire_at = models.DateTimeField()
    utilise_at = models.DateTimeField(null=True, blank=True)
    adresse_ip_creation = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Table des codes OTP avec contraintes d'unicité et options de gestion"""
        db_table = 'codes_otp'
        verbose_name = 'Code OTP'
        verbose_name_plural = 'Codes OTP'

    def __str__(self):
        """Retourne une représentation lisible du code OTP"""
        utilisateur_email = getattr(self.utilisateur, 'email', 'Inconnu')
        return f"OTP {self.type_code} - {utilisateur_email}"

    @classmethod
    def generer_code(cls):
        """Génère un code OTP de 6 chiffres"""
        return ''.join(secrets.choice(string.digits) for _ in range(6))

    def is_expired(self):
        """Vérifie si le code OTP a expiré"""
        return timezone.now() > self.expire_at

    def is_utilisable(self):
        """Vérifie si le code OTP peut être utilisé"""
        return (
            not self.is_expired() and 
            self.utilise_at is None and 
            self.tentatives_utilisation < self.max_tentatives
        )

    def marquer_utilise(self):
        """Marque le code OTP comme utilisé et enregistre l'heure d'utilisation"""
        self.utilise_at = timezone.now()
        self.save()
