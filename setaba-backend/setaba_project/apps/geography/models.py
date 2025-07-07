import uuid
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator

class Pays(models.Model):
    """Référentiel des pays avec codes ISO"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    code_iso_2 = models.CharField(
        max_length=2,
        unique=True,
        validators=[MinLengthValidator(2), MaxLengthValidator(2)],
        help_text="Code ISO 3166-1 alpha-2 (2 caractères)"
    )
    code_iso_3 = models.CharField(
        max_length=3,
        unique=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(3)],
        help_text="Code ISO 3166-1 alpha-3 (3 caractères)"
    )
    indicatif_tel = models.CharField(
        max_length=10, help_text="Indicatif téléphonique international")
    devise = models.CharField(max_length=10, default='XOF')
    fuseau_horaire = models.CharField(max_length=50, default='UTC')
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Table des pays avec contraintes d'unicité et options de gestion"""
        db_table = 'pays'
        verbose_name = 'Pays'
        verbose_name_plural = 'Pays'
        ordering = ['nom']

    def __str__(self):
        return str(self.nom)

class Ville(models.Model):
    """Villes avec coordonnées géographiques"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pays = models.ForeignKey(Pays, on_delete=models.RESTRICT, related_name='villes')
    nom = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude en degrés décimaux (-90 à +90)"
    )
    longitude = models.DecimalField(
        max_digits=11, 
        decimal_places=8, 
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude en degrés décimaux (-180 à +180)"
    )
    altitude = models.IntegerField(
        default=0, help_text="Altitude en mètres au-dessus du niveau de la mer")
    population = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Table des villes avec contraintes d'unicité et options de gestion"""
        db_table = 'villes'
        unique_together = ['pays', 'nom']
        verbose_name = 'Ville'
        verbose_name_plural = 'Villes'
        ordering = ['pays__nom', 'nom']

    def __str__(self):
        """Retourne une représentation lisible de la ville"""

        nom_pays = getattr(self.pays, 'nom', 'Inconnu')
        return f"{self.nom}, {nom_pays}"

class Commune(models.Model):
    """Communes/arrondissements avec localisation précise"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ville = models.ForeignKey(Ville, on_delete=models.RESTRICT, related_name='communes')
    nom = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=11, 
        decimal_places=8, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Table des communes avec contraintes d'unicité et options de gestion"""
        db_table = 'communes'
        unique_together = ['ville', 'nom']
        verbose_name = 'Commune'
        verbose_name_plural = 'Communes'
        ordering = ['ville__nom', 'nom']

    def __str__(self):
        """Retourne une représentation lisible de la commune"""

        nom_ville = getattr(self.ville, 'nom', 'Inconnu')
        return f"{self.nom}, {nom_ville}"
