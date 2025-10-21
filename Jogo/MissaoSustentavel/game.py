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
        self._carregar_nivel()

    def _carregar_nivel(self):
        lvl = self.niveis[self.atual]
        lvl.spawn()

        lvl.coletados = 0

        start_col = 1
        start_row = lvl.map_rows // 2
        found = lvl.encontrar_celula_caminho_proxima(start_col, start_row)
        if found:
            bx, by = found

            px = bx * TILE + TILE // 2
            py = by * TILE + TILE // 2
            player_rect = self.jogador.rect.copy()
            player_rect.center = (px, py)
            if hasattr(lvl, 'centros'):
                blocked = any(c.rect.colliderect(player_rect) for c in lvl.centros)
            else:
                blocked = False
            if not blocked:
                self.jogador.rect.center = (px, py)
            else:

                safe_found = None
                for r in range(1, 6):
                    for dy in range(-r, r + 1):
                        for dx in range(-r, r + 1):
                            nx = bx + dx
                            ny = by + dy
                            if 0 <= nx < lvl.map_cols and 0 <= ny < lvl.map_rows and lvl.bg_map[ny][nx] != 2:
                                candx = nx * TILE + TILE // 2
                                candy = ny * TILE + TILE // 2
                                crect = self.jogador.rect.copy()
                                crect.center = (candx, candy)
                                if hasattr(lvl, 'centros') and any(c.rect.colliderect(crect) for c in lvl.centros):
                                    continue
                                safe_found = (candx, candy)
                                break
                        if safe_found:
                            break
                    if safe_found:
                        break
                if safe_found:
                    self.jogador.rect.center = safe_found
                else:

                    self.jogador.rect.topleft = (60, 60)
        else:
            self.jogador.rect.topleft = (60, 60)
        self.jogador.mochila.clear()
        self.estado = "jogando"