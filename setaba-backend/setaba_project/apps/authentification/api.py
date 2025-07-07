from ninja import Router
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import Utilisateur, Profil
from .schemas import *
from .services import OTPService
from apps.geography.models import Pays

router = Router()

@router.post("/inscription", response=UtilisateurResponseSchema)
def inscription(request, data: UtilisateurCreateSchema):
    """Inscription avec envoi de codes OTP"""
    
    # Vérifier que l'email et téléphone sont uniques
    if Utilisateur.objects.filter(email=data.email).exists():
        return {"error": "Email déjà utilisé"}
    
    if Utilisateur.objects.filter(telephone=data.telephone).exists():
        return {"error": "Téléphone déjà utilisé"}
    
    # Créer l'utilisateur
    pays = get_object_or_404(Pays, id=data.pays_id)
    
    utilisateur = Utilisateur.objects.create_user(
        email=data.email,
        telephone=data.telephone,
        password=data.password,
        accepte_conditions=data.accepte_conditions,
        accepte_marketing=data.accepte_marketing,
        is_active=False  # Inactif jusqu'à vérification OTP
    )
    
    # Créer le profil
    Profil.objects.create(
        utilisateur=utilisateur,
        nom=data.nom,
        prenom=data.prenom,
        pays=pays
    )
    
    # Envoyer les codes OTP
    OTPService.generer_et_envoyer_otp(utilisateur, 'email_verification')
    OTPService.generer_et_envoyer_otp(utilisateur, 'phone_verification')
    
    return {
        "id": str(utilisateur.id),
        "email": utilisateur.email,
        "telephone": str(utilisateur.telephone),
        "email_verifie": utilisateur.email_verifie,
        "telephone_verifie": utilisateur.telephone_verifie,
        "actif": utilisateur.is_active
    }

@router.post("/verifier-otp")
def verifier_otp(request, data: OTPVerificationSchema):
    """Vérification des codes OTP"""
    
    try:
        utilisateur = Utilisateur.objects.get(email=data.email)
    except Utilisateur.DoesNotExist:
        return {"success": False, "message": "Utilisateur introuvable"}
    
    success, message = OTPService.verifier_otp(utilisateur, data.code, data.type_code)
    
    # Activer le compte si email ET téléphone vérifiés
    if success and utilisateur.is_account_verified():
        utilisateur.is_active = True
        utilisateur.save()
    
    return {"success": success, "message": message}

@router.post("/connexion")
def connexion(request, data: LoginSchema):
    """Connexion utilisateur"""
    
    utilisateur = authenticate(email=data.email, password=data.password)
    
    if not utilisateur:
        return {"success": False, "message": "Identifiants invalides"}
    
    if not utilisateur.is_active:
        return {"success": False, "message": "Compte non activé"}
    
    if not utilisateur.is_account_verified():
        return {"success": False, "message": "Veuillez vérifier votre email et téléphone"}
    
    # Créer session, etc.
    
    return {
        "success": True,
        "user": {
            "id": str(utilisateur.id),
            "email": utilisateur.email,
            "nom_complet": utilisateur.profil.nom_complet
        }
    }