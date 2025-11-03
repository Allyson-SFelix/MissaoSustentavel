import random
import pygame
from typing import List, Optional, Tuple
from .enums import TipoLixo
from .entities import Item, Lixeira, Inimigo, CentroReciclagem
from .config import LARGURA, ALTURA, TILE

class Nivel:
    """Gerencia o cenário, inimigo, lixeiras e lixo do jogo."""

    def __init__(self, numero: int, tipos_bilhetes: List[TipoLixo], meta_itens: int, inimigo: bool = False):
        self.background_image = pygame.transform.scale(
            pygame.image.load("assets/cenario.png").convert(),
            (LARGURA, ALTURA)
        )
        self.numero = numero
        self.tipos_bilhetes = tipos_bilhetes or [TipoLixo.GENERICO]
        self.meta_itens = meta_itens
        self.itens: List[Item] = []
        self.lixeiras: List[Lixeira] = []
        self.centros: List[CentroReciclagem] = []
        self.coletados = 0
        self.com_inimigo = inimigo
        self.inimigo: Optional[Inimigo] = Inimigo(pygame.Rect(LARGURA - 80, ALTURA - 80, 28, 28), velocidade=2.2) if inimigo else None

        # mapa de tiles: 0=chão, 2=água
        self.map_cols = LARGURA // TILE
        self.map_rows = ALTURA // TILE
        self.bg_map = [[0 for _ in range(self.map_cols)] for __ in range(self.map_rows)]

    # =========================================================
    # MÉTODOS PRINCIPAIS
    # =========================================================
    def spawn(self):
        """Gera o mapa, água, centros de reciclagem, inimigo e itens."""
        self._gerar_agua()
        self.centros.clear()
        self.lixeiras.clear()
        self.itens.clear()

        self._criar_centro_reciclagem()

        if self.inimigo:
            self.inimigo.rect.topleft = (LARGURA - 80, ALTURA - 80)
            self._garantir_inimigo_fora_centros()

        self._gerar_itens()

    def atualizar_inimigo(self, jogador_rect: pygame.Rect, limites: pygame.Rect) -> bool:
        if not self.inimigo:
            return False

        self.inimigo.atualizar(jogador_rect, limites)

        for cent in self.centros:
            attempts = 0
            while cent.rect.colliderect(self.inimigo.rect) and attempts < 200:
                dx = self.inimigo.rect.centerx - cent.rect.centerx
                dy = self.inimigo.rect.centery - cent.rect.centery
                import math
                dist = math.hypot(dx, dy) or 1.0
                self.inimigo.rect.x += int(round(2 * dx / dist))
                self.inimigo.rect.y += int(round(2 * dy / dist))
                self.inimigo.rect.clamp_ip(limites)
                attempts += 1
        return self.inimigo.rect.colliderect(jogador_rect)

    def _gerar_agua(self):
        """Cria uma faixa de água no topo do mapa."""
        sea_height = max(4, self.map_rows // 5)
        for ry in range(sea_height):
            for rx in range(self.map_cols):
                self.bg_map[ry][rx] = 2

    def _criar_centro_reciclagem(self):
        """Cria um centro de reciclagem com lixeiras."""
        center_w, center_h = 215, 170
        pref_col = max(1, self.map_cols - 3)
        pref_row = max(1, self.map_rows - 5)
        found = self.encontrar_celula_caminho_proxima(pref_col, pref_row)

        if found:
            bx, by = found
            cx = bx * TILE + TILE // 2 - center_w // 2
            cy = by * TILE + TILE // 2 - center_h // 2 - TILE * 2
        else:
            cx = LARGURA - center_w - 24
            cy = ALTURA - center_h - 24 - TILE * 2

        cx, cy = 740, 220


        lixeiras_internas = []
        bw, bh = 40, 48
        padding_x, padding_y = 16, 40
        types = self.tipos_bilhetes
        spacing = (center_w - 2 * padding_x - (bw * len(types))) // max(1, len(types) - 1) if len(types) > 1 else 0

        for i, t in enumerate(types):
            bx = cx + padding_x + i * (bw + spacing)
            by = cy + padding_y
            lixeiras_internas.append(Lixeira(pygame.Rect(bx, by, bw, bh), t))

        centro_rect = pygame.Rect(cx, cy, center_w, center_h)
        centro = CentroReciclagem(centro_rect, lixeiras_internas)
        self.centros.append(centro)

        for l in lixeiras_internas:
            setattr(l, "centro_pai", centro)
            self.lixeiras.append(l)

    def _garantir_inimigo_fora_centros(self):
        """Garante que o inimigo não esteja dentro de um centro."""
        for cent in self.centros:
            if cent.rect.colliderect(self.inimigo.rect):
                for pos in [(40, 40), (LARGURA - 80, 40), (40, ALTURA - 80), (LARGURA - 80, ALTURA - 80)]:
                    self.inimigo.rect.topleft = pos
                    if not cent.rect.colliderect(self.inimigo.rect):
                        return
                # fallback
                self.inimigo.rect.topleft = (cent.rect.left - 40, cent.rect.top - 40)

    def _gerar_itens(self):
        """Gera os itens com distribuição uniforme por tipo de lixo."""
        LIXO_TAM = 60
        
        # Calcular quantos itens de cada tipo
        num_tipos = len(self.tipos_bilhetes)
        itens_por_tipo = self.meta_itens // num_tipos
        
        # Criar lista de tipos com distribuição uniforme
        tipos_distribuidos = []
        for tipo in self.tipos_bilhetes:
            tipos_distribuidos.extend([tipo] * itens_por_tipo)
        
        # Embaralhar para não seguir ordem fixa
        random.shuffle(tipos_distribuidos)
        
        # Gerar os itens
        for t in tipos_distribuidos:
            for _try in range(200):
                px = random.randrange(40, LARGURA - LIXO_TAM - 40)
                py = random.randrange(40, ALTURA - LIXO_TAM - 40)
                cell_x, cell_y = px // TILE, py // TILE
                if not (0 <= cell_x < self.map_cols and 0 <= cell_y < self.map_rows):
                    continue
                if self.bg_map[cell_y][cell_x] == 2:
                    continue
                item_rect = pygame.Rect(px, py, LIXO_TAM, LIXO_TAM)
                if any(cent.rect.colliderect(item_rect) for cent in self.centros):
                    continue
                self.itens.append(Item(item_rect, t))
                break
            else:
                print(f"[AVISO] Não foi possível posicionar o item {t}")

    def encontrar_celula_caminho_proxima(self, col: int, row: int, raio_max: int = 8) -> Optional[Tuple[int, int]]:
        if 0 <= row < self.map_rows and 0 <= col < self.map_cols and self.bg_map[row][col] != 2:
            return col, row
        for r in range(1, raio_max + 1):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if abs(dx) != r and abs(dy) != r:
                        continue
                    ny, nx = row + dy, col + dx
                    if 0 <= ny < self.map_rows and 0 <= nx < self.map_cols and self.bg_map[ny][nx] != 2:
                        return nx, ny
        return None

    def eh_agua(self, rect: pygame.Rect) -> bool:
        left, right = rect.left // TILE, rect.right // TILE
        top, bottom = rect.top // TILE, rect.bottom // TILE
        for ry in range(top, bottom + 1):
            for rx in range(left, right + 1):
                if self.bg_map[ry][rx] == 2:
                    return True
        return False

    def esta_bloqueado(self, rect: pygame.Rect, jogador=None) -> bool:
        for cent in self.centros:
            if cent.rect.colliderect(rect):
                if jogador and getattr(jogador, 'dentro_centro', None) is cent and cent.rect.contains(rect):
                    return False
                return True
        cx, cy = rect.centerx // TILE, rect.centery // TILE
        if not (0 <= cx < self.map_cols and 0 <= cy < self.map_rows):
            return True
        return self.bg_map[cy][cx] == 2

    def desenhar(self, surf: pygame.Surface):
        surf.blit(self.background_image, (0, 0))
        for c in self.centros:
            c.desenhar(surf)
        for l in self.lixeiras:
            l.desenhar(surf)
        for it in self.itens:
            it.desenhar(surf)
        if self.inimigo:
            self.inimigo.desenhar(surf)