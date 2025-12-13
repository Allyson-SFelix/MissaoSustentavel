from enum import Enum, auto
import os
import pygame

class TipoLixo(Enum):
    GENERICO = auto()
    ORGANICO = auto()
    PLASTICO = auto()
    PAPEL = auto()
    VIDRO = auto()
    METAL = auto()
    PERIGOSO = auto()



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE_DIR, "../../Jogo/assets",)

TIPO_IMAGENS = {
    TipoLixo.GENERICO: pygame.image.load(os.path.join(IMG,"generico.png")),
    TipoLixo.ORGANICO: pygame.image.load(os.path.join(IMG,"organico.png")),
    TipoLixo.PLASTICO: pygame.image.load(os.path.join(IMG,"plastico.png")),
    TipoLixo.PAPEL: pygame.image.load(os.path.join(IMG,"papel.png")),
    TipoLixo.VIDRO: pygame.image.load(os.path.join(IMG,"vidro.png")),
    TipoLixo.METAL: pygame.image.load(os.path.join(IMG,"metal.png")),
    TipoLixo.PERIGOSO: pygame.image.load(os.path.join(IMG,"perigoso.png")),
}


IMAGEM_PERSONAGEM = pygame.image.load(os.path.join(IMG,"Personagem2d.png"))
IMAGEM_MONSTRO = pygame.image.load(os.path.join(IMG,"Monstro2d.png"))

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