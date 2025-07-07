from ninja import Schema
from typing import List, Optional

class PaysSchema(Schema):
    id: str
    nom: str
    code_iso_2: str
    code_iso_3: str
    indicatif_tel: str
    devise: str

class VilleSchema(Schema):
    id: str
    nom: str
    code_postal: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    pays: PaysSchema

class CommuneSchema(Schema):
    id: str
    nom: str
    code_postal: Optional[str]
    ville: VilleSchema