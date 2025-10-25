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

TIPO_IMAGENS = {
    TipoLixo.GENERICO: pygame.image.load("assets/generico.png"),
    TipoLixo.ORGANICO: pygame.image.load("assets/organico.png"),
    TipoLixo.PLASTICO: pygame.image.load("assets/plastico.png"),
    TipoLixo.PAPEL: pygame.image.load("assets/papel.png"),
    TipoLixo.VIDRO: pygame.image.load("assets/vidro.png"),
    TipoLixo.METAL: pygame.image.load("assets/metal.png"),
    TipoLixo.PERIGOSO: pygame.image.load("assets/perigoso.png"),
}

TIPO_NOMES = {
    TipoLixo.GENERICO: "Geral",
    TipoLixo.ORGANICO: "Orgânico",
    TipoLixo.PLASTICO: "Plástico",
    TipoLixo.PAPEL: "Papel",
    TipoLixo.VIDRO: "Vidro",
    TipoLixo.METAL: "Metal",
    TipoLixo.PERIGOSO: "Perigoso",
}

CORES_LIXEIRA = {
    TipoLixo.PAPEL: (0, 0, 255),
    TipoLixo.PLASTICO: (80, 140, 128),
    TipoLixo.VIDRO: (0, 128, 0),
    TipoLixo.METAL: (184, 115, 51),
    TipoLixo.ORGANICO: (139, 69, 19),
    TipoLixo.GENERICO: (100, 100, 100),
}