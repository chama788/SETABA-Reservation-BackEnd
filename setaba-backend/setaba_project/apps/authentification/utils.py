import re
from phonenumber_field.phonenumber import PhoneNumber
from django.core.exceptions import ValidationError

def valider_telephone_afrique_francophone(telephone):
    """Valide les numéros de téléphone pour l'Afrique francophone"""
    
    # Indicatifs des pays francophones d'Afrique
    indicatifs_valides = [
        '+225',  # Côte d'Ivoire
        '+221',  # Sénégal
        '+223',  # Mali
        '+226',  # Burkina Faso
        '+228',  # Togo
        '+229',  # Bénin
        '+224',  # Guinée
        '+227',  # Niger
        '+235',  # Tchad
        '+236',  # République centrafricaine
        '+237',  # Cameroun
        '+241',  # Gabon
        '+242',  # Congo
        '+243',  # RD Congo
        '+261',  # Madagascar
        '+262',  # Réunion/Mayotte
        '+33',   # France
    ]
    
    try:
        phone_number = PhoneNumber.from_string(telephone)
        
        # Vérifier que le numéro est valide
        if not phone_number.is_valid():
            raise ValidationError("Numéro de téléphone invalide")
        
        # Vérifier l'indicatif
        country_code = f"+{phone_number.country_code}"
        if country_code not in indicatifs_valides:
            raise ValidationError(
                f"Indicatif {country_code} non supporté. "
                f"Indicatifs acceptés: {', '.join(indicatifs_valides)}"
            )
        
        return phone_number
        
    except Exception as e:
        raise ValidationError(f"Erreur de validation du téléphone: {str(e)}")

def generer_nom_utilisateur_unique(email):
    """Génère un nom d'utilisateur unique à partir de l'email"""
    base_username = email.split('@')[0]
    base_username = re.sub(r'[^a-zA-Z0-9]', '', base_username)
    
    if len(base_username) < 3:
        base_username = f"user{base_username}"
    
    username = base_username
    counter = 1
    
    from .models import Utilisateur
    while Utilisateur.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    
    return username