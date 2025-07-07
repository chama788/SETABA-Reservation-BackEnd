import uuid
from django.utils import timezone
from django.http import JsonResponse
from .models import SessionUtilisateur

class SessionTrackingMiddleware:
    """Middleware pour traquer les sessions actives"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Mettre à jour la dernière activité
            session_key = request.session.session_key
            if session_key:
                SessionUtilisateur.objects.filter(
                    utilisateur=request.user,
                    token_session=session_key,
                    actif=True
                ).update(derniere_activite=timezone.now())

        response = self.get_response(request)
        return response

class SecurityHeadersMiddleware:
    """Middleware pour ajouter des headers de sécurité"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de sécurité
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response