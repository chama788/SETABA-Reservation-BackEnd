from django.core.management.base import BaseCommand
from apps.geography.models import Pays, Ville, Commune

class Command(BaseCommand):
    help = 'Charge les données géographiques de base'

    def handle(self, *args, **options):
        # Pays de base
        pays_data = [
            {
                'nom': "Côte d'Ivoire",
                'code_iso_2': 'CI',
                'code_iso_3': 'CIV',
                'indicatif_tel': '+225',
                'devise': 'XOF',
                'fuseau_horaire': 'GMT'
            },
            {
                'nom': 'France',
                'code_iso_2': 'FR',
                'code_iso_3': 'FRA',
                'indicatif_tel': '+33',
                'devise': 'EUR',
                'fuseau_horaire': 'CET'
            },
            {
                'nom': 'Sénégal',
                'code_iso_2': 'SN',
                'code_iso_3': 'SEN',
                'indicatif_tel': '+221',
                'devise': 'XOF',
                'fuseau_horaire': 'GMT'
            },
            {
                'nom': 'Mali',
                'code_iso_2': 'ML',
                'code_iso_3': 'MLI',
                'indicatif_tel': '+223',
                'devise': 'XOF',
                'fuseau_horaire': 'GMT'
            },
            {
                'nom': 'Burkina Faso',
                'code_iso_2': 'BF',
                'code_iso_3': 'BFA',
                'indicatif_tel': '+226',
                'devise': 'XOF',
                'fuseau_horaire': 'GMT'
            },
        ]

        for pays_info in pays_data:
            pays, created = Pays.objects.get_or_create(
                code_iso_2=pays_info['code_iso_2'],
                defaults=pays_info
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Pays "{pays.nom}" créé avec succès')
                )

        # Villes principales de Côte d'Ivoire
        try:
            ci = Pays.objects.get(code_iso_2='CI')
            villes_ci = [
                {
                    'nom': 'Abidjan',
                    'latitude': 5.3364,
                    'longitude': -4.0267,
                    'population': 4395243
                },
                {
                    'nom': 'Bouaké',
                    'latitude': 7.6939,
                    'longitude': -5.0300,
                    'population': 832371
                },
                {
                    'nom': 'Yamoussoukro',
                    'latitude': 6.8205,
                    'longitude': -5.2767,
                    'population': 355573
                },
                {
                    'nom': 'Daloa',
                    'latitude': 6.8775,
                    'longitude': -6.4503,
                    'population': 319427
                },
            ]

            for ville_info in villes_ci:
                ville, created = Ville.objects.get_or_create(
                    pays=ci,
                    nom=ville_info['nom'],
                    defaults=ville_info
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Ville "{ville.nom}" créée avec succès')
                    )

            # Communes d'Abidjan
            try:
                abidjan = Ville.objects.get(pays=ci, nom='Abidjan')
                communes_abidjan = [
                    {'nom': 'Plateau', 'latitude': 5.3194, 'longitude': -4.0267},
                    {'nom': 'Cocody', 'latitude': 5.3547, 'longitude': -3.9864},
                    {'nom': 'Yopougon', 'latitude': 5.3364, 'longitude': -4.0878},
                    {'nom': 'Marcory', 'latitude': 5.2892, 'longitude': -4.0019},
                    {'nom': 'Treichville', 'latitude': 5.2969, 'longitude': -4.0267},
                    {'nom': 'Koumassi', 'latitude': 5.2875, 'longitude': -3.9647},
                    {'nom': 'Adjamé', 'latitude': 5.3694, 'longitude': -4.0267},
                    {'nom': 'Abobo', 'latitude': 5.4167, 'longitude': -4.0167},
                ]

                for commune_info in communes_abidjan:
                    commune, created = Commune.objects.get_or_create(
                        ville=abidjan,
                        nom=commune_info['nom'],
                        defaults=commune_info
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Commune "{commune.nom}" créée avec succès')
                        )

            except Ville.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING('Ville Abidjan non trouvée pour créer les communes')
                )

        except Pays.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('Pays Côte d\'Ivoire non trouvé pour créer les villes')
            )