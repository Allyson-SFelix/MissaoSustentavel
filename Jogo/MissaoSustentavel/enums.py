from enum import Enum, auto
import pygame

class TipoLixo(Enum):
    GENERICO = auto()
    ORGANICO = auto()
    PLASTICO = auto()
    PAPEL = auto()
    VIDRO = auto()
    METAL = auto()
    PERIGOSO = auto()

TIPO_NOMES = {
    TipoLixo.GENERICO: "Geral",
    TipoLixo.ORGANICO: "Orgânico",
    TipoLixo.PLASTICO: "Plástico",
    TipoLixo.PAPEL: "Papel",
    TipoLixo.VIDRO: "Vidro",
    TipoLixo.METAL: "Metal",
    TipoLixo.PERIGOSO: "Perigoso",
}