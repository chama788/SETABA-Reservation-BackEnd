from django.core.management.base import BaseCommand
from apps.authentification.models import Role

class Command(BaseCommand):
    help = 'Crée les rôles par défaut'

    def handle(self, *args, **options):
        roles_default = [
            {
                'code': 'ADMIN',
                'libelle': 'Administrateur',
                'description': 'Administrateur système avec tous les droits',
                'niveau': 100,
                'permissions': {'all': True}
            },
            {
                'code': 'MODERATEUR',
                'libelle': 'Modérateur',
                'description': 'Modérateur de contenu et support',
                'niveau': 80,
                'permissions': {
                    'moderate_content': True,
                    'manage_support': True,
                    'view_reports': True
                }
            },
            {
                'code': 'PROPRIETAIRE',
                'libelle': 'Propriétaire',
                'description': 'Propriétaire de biens ou véhicules',
                'niveau': 50,
                'permissions': {
                    'manage_own_properties': True,
                    'manage_own_vehicles': True,
                    'view_own_bookings': True
                }
            },
            {
                'code': 'CLIENT',
                'libelle': 'Client',
                'description': 'Client standard de la plateforme',
                'niveau': 30,
                'permissions': {
                    'book_properties': True,
                    'book_vehicles': True,
                    'leave_reviews': True
                }
            },
            {
                'code': 'CHAUFFEUR',
                'libelle': 'Chauffeur',
                'description': 'Chauffeur professionnel',
                'niveau': 40,
                'permissions': {
                    'accept_missions': True,
                    'update_mission_status': True,
                    'view_own_missions': True
                }
            },
        ]

        for role_data in roles_default:
            role, created = Role.objects.get_or_create(
                code=role_data['code'],
                defaults=role_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Rôle "{role.libelle}" créé avec succès')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Rôle "{role.libelle}" existe déjà')
                )