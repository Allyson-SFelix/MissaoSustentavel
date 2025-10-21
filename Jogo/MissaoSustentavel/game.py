import pygame
from typing import List
from .config import LARGURA, ALTURA, FPS, COR_FUNDO, COR_GRADE, NOME_FONTE, TILE
from .enums import TipoLixo
#from .entities import Jogador
#from .level import Nivel

class Jogo:
    def __init__(self,usuario):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Missão Sustentável")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(NOME_FONTE, 18)

        self.limites = pygame.Rect(0,0,LARGURA,ALTURA)
        self.jogador = Jogador(pygame.Rect(60,60,28,28))

        self.niveis: List[Nivel] = [
            Nivel(1, [TipoLixo.GENERICO], meta_itens=5, inimigo=False),
            Nivel(2, [TipoLixo.ORGANICO, TipoLixo.PLASTICO], meta_itens=8, inimigo=False),
            Nivel(3, [TipoLixo.PAPEL, TipoLixo.VIDRO, TipoLixo.METAL], meta_itens=10, inimigo=False),
            Nivel(4, [TipoLixo.ORGANICO, TipoLixo.PLASTICO, TipoLixo.PAPEL, TipoLixo.VIDRO], meta_itens=12, inimigo=True),
        ]
        self.usuario=usuario
        self.atual = 0
        self.estado = "jogando"
        #self._carregar_nivel()