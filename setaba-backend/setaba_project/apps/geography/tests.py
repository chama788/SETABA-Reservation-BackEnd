from django.test import TestCase
from .models import Pays, Ville, Commune

class GeographyTestCase(TestCase):
    def setUp(self):
        self.pays = Pays.objects.create(
            nom="Côte d'Ivoire",
            code_iso_2='CI',
            code_iso_3='CIV',
            indicatif_tel='+225'
        )

    def test_creation_pays(self):
        """Test de création de pays"""
        self.assertEqual(self.pays.nom, "Côte d'Ivoire")
        self.assertEqual(self.pays.code_iso_2, 'CI')
        self.assertTrue(self.pays.actif)

    def test_creation_ville(self):
        """Test de création de ville"""
        ville = Ville.objects.create(
            pays=self.pays,
            nom='Abidjan',
            latitude=5.3364,
            longitude=-4.0267,
            population=4395243
        )
        
        self.assertEqual(ville.nom, 'Abidjan')
        self.assertEqual(ville.pays, self.pays)
        self.assertEqual(str(ville), 'Abidjan, Côte d\'Ivoire')

    def test_creation_commune(self):
        """Test de création de commune"""
        ville = Ville.objects.create(
            pays=self.pays,
            nom='Abidjan'
        )
        
        commune = Commune.objects.create(
            ville=ville,
            nom='Cocody',
            latitude=5.3547,
            longitude=-3.9864
        )
        
        self.assertEqual(commune.nom, 'Cocody')
        self.assertEqual(commune.ville, ville)
        self.assertEqual(str(commune), 'Cocody, Abidjan')
