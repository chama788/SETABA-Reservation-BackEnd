from ninja import Schema
from typing import Optional
from datetime import datetime

class UtilisateurCreateSchema(Schema):
    email: str
    telephone: str
    password: str
    nom: str
    prenom: str
    pays_id: str
    accepte_conditions: bool = True
    accepte_marketing: bool = False

class UtilisateurResponseSchema(Schema):
    id: str
    email: str
    telephone: str
    email_verifie: bool
    telephone_verifie: bool
    actif: bool
    profil: Optional[dict] = None

class OTPVerificationSchema(Schema):
    email: str
    code: str
    type_code: str

class LoginSchema(Schema):
    email: str
    password: str