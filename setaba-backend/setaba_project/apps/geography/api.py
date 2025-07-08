from ninja import Router
from typing import List
from .models import Pays, Ville, Commune
from .schemas import *

router = Router()

@router.get("/pays", response=List[PaysSchema])
def liste_pays(request):
    """Liste des pays actifs"""
    return Pays.objects.filter(actif=True)

@router.get("/pays/{pays_id}/villes", response=List[VilleSchema])
def villes_par_pays(request, pays_id: str):
    """Villes d'un pays"""
    villes = Ville.objects.filter(pays_id=pays_id, actif=True).select_related('pays')
    return [
        {
            "id": str(v.id),
            "nom": v.nom,
            "code_postal": v.code_postal,
            "latitude": float(v.latitude) if v.latitude else None,
            "longitude": float(v.longitude) if v.longitude else None,
            "pays": {
                "id": str(v.pays.id),
                "nom": v.pays.nom,
                "code_iso_2": v.pays.code_iso_2,
                "code_iso_3": v.pays.code_iso_3,
                "indicatif_tel": v.pays.indicatif_tel,
                "devise": v.pays.devise
            }
        }
        for v in villes
    ]

@router.get("/villes/{ville_id}/communes", response=List[CommuneSchema])
def communes_par_ville(request, ville_id: str):
    """Communes d'une ville"""
    communes = Commune.objects.filter(ville_id=ville_id, actif=True).select_related('ville__pays')
    return communes