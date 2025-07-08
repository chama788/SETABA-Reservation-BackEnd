"""
Module de tests pour les fonctionnalités d'authentification et de gestion des utilisateurs.
Les tests incluent : création d'utilisateurs, vérification des OTP, et gestion des statuts vérifiés.
"""

from django.test import TestCase
from django.contrib.auth import authenticate

from .models import Utilisateur, CodeOTP
from .services import OTPService
from apps.geography.models import Pays


class UtilisateurTestCase(TestCase):
    """Cas de test pour les fonctionnalités liées au modèle Utilisateur"""

    def setUp(self):
        """Initialisation des données communes aux tests"""
        self.pays = Pays.objects.create(
            nom="Côte d'Ivoire",
            code_iso_2='CI',
            code_iso_3='CIV',
            indicatif_tel='+225'
        )

    def test_creation_utilisateur(self):
        """Test de création d'un utilisateur et vérification des champs par défaut"""
        utilisateur = Utilisateur.objects.create_user(
            email='test@example.com',
            telephone='+2250701234567',
            password='testpass123'
        )

        self.assertEqual(utilisateur.email, 'test@example.com')
        self.assertFalse(utilisateur.email_verifie)
        self.assertFalse(utilisateur.telephone_verifie)
        self.assertFalse(utilisateur.is_account_verified())

    def test_verification_otp(self):
        """Test du processus de génération et vérification d’un code OTP"""
        utilisateur = Utilisateur.objects.create_user(
            email='test@example.com',
            telephone='+2250701234567',
            password='testpass123'
        )

        # Générer OTP email
        otp = OTPService.generer_et_envoyer_otp(
            utilisateur, 'email_verification'
        )

        self.assertIsNotNone(otp)
        self.assertEqual(len(otp.code), 6)
        self.assertTrue(otp.is_utilisable())

        # Vérifier OTP
        success, message = OTPService.verifier_otp(
            utilisateur, otp.code, 'email_verification'
        )

        self.assertTrue(success)
        utilisateur.refresh_from_db()
        self.assertTrue(utilisateur.email_verifie)
