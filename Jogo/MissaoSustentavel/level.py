import pygame
from .config import LARGURA, ALTURA, TILE

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
        center_w, center_h = 220, 120
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

        cx = max(8, min(cx, LARGURA - center_w - 8))
        cy = max(8, min(cy, ALTURA - center_h - 8))

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