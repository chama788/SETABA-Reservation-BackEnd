import secrets
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from .models import CodeOTP, Utilisateur

class OTPService:
    """Service de gestion des codes OTP"""
    
    @staticmethod
    def generer_et_envoyer_otp(utilisateur, type_code, email_cible=None, telephone_cible=None):
        """Génère et envoie un code OTP"""
        # Supprimer les anciens codes non utilisés
        CodeOTP.objects.filter(
            utilisateur=utilisateur,
            type_code=type_code,
            utilise_at__isnull=True
        ).delete()
        
        # Générer nouveau code
        code = CodeOTP.generer_code()
        otp = CodeOTP.objects.create(
            utilisateur=utilisateur,
            code=code,
            type_code=type_code,
            email_cible=email_cible or utilisateur.email,
            telephone_cible=telephone_cible or utilisateur.telephone,
            expire_at=timezone.now() + timedelta(minutes=10)
        )
        
        # Envoyer par email et SMS
        if type_code in ['email_verification', 'password_reset']:
            OTPService.envoyer_email_otp(otp)
        
        if type_code in ['phone_verification', 'login_verification']:
            OTPService.envoyer_sms_otp(otp)
        
        return otp
    
    @staticmethod
    def envoyer_email_otp(otp):
        """Envoie le code OTP par email"""
        subject = f"Code de vérification SETABA: {otp.code}"
        message = f"""
        Bonjour,
        
        Votre code de vérification SETABA est: {otp.code}
        
        Ce code expire dans 10 minutes.
        
        L'équipe SETABA
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [otp.email_cible or otp.utilisateur.email]
        )
    
    @staticmethod
    def envoyer_sms_otp(otp):
        """Envoie le code OTP par SMS"""
        # Configuration Twilio ou autre service SMS
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message = client.messages.create(
                body=f"Votre code SETABA: {otp.code}. Expire dans 10 minutes.",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=str(otp.telephone_cible or otp.utilisateur.telephone)
            )
            
            return message.sid
        except Exception as e:
            # Log l'erreur
            print(f"Erreur envoi SMS: {e}")
            return None
    
    @staticmethod
    def verifier_otp(utilisateur, code, type_code):
        """Vérifie un code OTP"""
        try:
            otp = CodeOTP.objects.get(
                utilisateur=utilisateur,
                code=code,
                type_code=type_code,
                utilise_at__isnull=True
            )
            
            if not otp.is_utilisable():
                return False, "Code expiré ou invalide"
            
            # Marquer comme utilisé
            otp.marquer_utilise()
            
            # Actions spécifiques selon le type
            if type_code == 'email_verification':
                utilisateur.email_verifie = True
                if otp.email_cible:
                    utilisateur.email = otp.email_cible
                utilisateur.save()
            
            elif type_code == 'phone_verification':
                utilisateur.telephone_verifie = True
                if otp.telephone_cible:
                    utilisateur.telephone = otp.telephone_cible
                utilisateur.save()
            
            return True, "Code vérifié avec succès"
            
        except CodeOTP.DoesNotExist:
            return False, "Code invalide"