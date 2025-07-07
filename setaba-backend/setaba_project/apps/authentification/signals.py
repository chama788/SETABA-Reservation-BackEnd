from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Utilisateur, Profil, SessionUtilisateur
from django.utils import timezone

@receiver(post_save, sender=Utilisateur)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil lors de la création d'un utilisateur"""
    if created and not hasattr(instance, 'profil'):
        # Le profil sera créé manuellement lors de l'inscription
        pass

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """Traite la connexion utilisateur"""
    # Mettre à jour les informations de connexion
    user.derniere_connexion = timezone.now()
    user.ip_derniere_connexion = get_client_ip(request)
    user.tentatives_connexion = 0  # Reset des tentatives
    user.save()

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    """Traite la déconnexion utilisateur"""
    if user and user.is_authenticated:
        # Désactiver toutes les sessions actives de l'utilisateur
        SessionUtilisateur.objects.filter(
            utilisateur=user,
            actif=True
        ).update(actif=False)

def get_client_ip(request):
    """Récupère l'IP réelle du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip