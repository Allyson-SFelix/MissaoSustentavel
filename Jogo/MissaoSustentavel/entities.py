import pygame
from dataclasses import dataclass, field
from typing import List, Optional
from .enums import TipoLixo, TIPO_IMAGENS, CORES_LIXEIRA
from .config import TILE, VELOCIDADE_JOGADOR

@dataclass
class Item:
    rect: pygame.Rect
    tipo: TipoLixo

    def desenhar(self, surf: pygame.Surface):
        imagem = TIPO_IMAGENS[self.tipo]
        imagem_redimensionada = pygame.transform.scale(imagem, (self.rect.w, self.rect.h))
        surf.blit(imagem_redimensionada, self.rect)

@dataclass
class Lixeira:
    rect: pygame.Rect
    tipo: TipoLixo

    def desenhar(self, surf: pygame.Surface):

        cor = CORES_LIXEIRA.get(self.tipo, (200, 200, 200))

        pygame.draw.rect(surf, cor, self.rect, border_radius=6)
        inner = self.rect.inflate(-8, -8)
        pygame.draw.rect(surf, (240, 240, 240), inner, border_radius=6)

        faixa_altura = 8
        faixa = pygame.Rect(self.rect.x, self.rect.y - faixa_altura, self.rect.w, faixa_altura)
        pygame.draw.rect(surf, cor, faixa, border_radius=3)

        # Dicionário de abreviações para os nomes
        abreviacoes = {
            TipoLixo.GENERICO: "Geral",
            TipoLixo.ORGANICO: "Org",
            TipoLixo.PLASTICO: "Plas",
            TipoLixo.PAPEL: "Pap",
            TipoLixo.VIDRO: "Vid",
            TipoLixo.METAL: "Met",
            TipoLixo.PERIGOSO: "Per"
        }

        # Usar fonte menor e nome abreviado
        font = pygame.font.SysFont(None, 12)  # Reduzindo o tamanho da fonte
        txt = font.render(abreviacoes[self.tipo], True, (30, 30, 30))
        # Centralizar o texto acima da lixeira
        texto_x = self.rect.x + (self.rect.width - txt.get_width()) // 2
        surf.blit(txt, (texto_x, self.rect.y - 15))

@dataclass
class CentroReciclagem:
    rect: pygame.Rect
    lixeiras: List[Lixeira]

    def desenhar(self, surf: pygame.Surface):
        pygame.draw.rect(surf, (150, 150, 150), self.rect, border_radius=8)
        inner = self.rect.inflate(-10, -10)
        pygame.draw.rect(surf, (200, 200, 200), inner, border_radius=6)

        door = pygame.Rect(self.rect.centerx - 16, self.rect.bottom - 28, 32, 24)
        pygame.draw.rect(surf, (90, 60, 40), door, border_radius=3)

        font = pygame.font.SysFont(None, 16)
        txt = font.render("Centro Reciclável", True, (30, 30, 30))
        surf.blit(txt, (self.rect.x + 8, self.rect.y + 6))

        for l in self.lixeiras:
            l.desenhar(surf)

@dataclass
class Jogador:
    rect: pygame.Rect
    velocidade: float = VELOCIDADE_JOGADOR
    saco_lixo: List[TipoLixo] = field(default_factory=list)
    capacidade: int = 5
    dentro_centro: Optional['CentroReciclagem'] = None
    posicao_antes_centro: Optional[pygame.Rect] = None

    def mover(self, keys, limites: pygame.Rect, nivel=None):
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx -= self.velocidade
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += self.velocidade
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy -= self.velocidade
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy += self.velocidade

        if dx:
            new_rect = self.rect.copy()
            new_rect.x += int(dx)
            new_rect.clamp_ip(limites)
            if nivel is None or not nivel.esta_bloqueado(new_rect, jogador=self):
                self.rect.x = new_rect.x
        if dy:
            new_rect = self.rect.copy()
            new_rect.y += int(dy)
            new_rect.clamp_ip(limites)
            if nivel is None or not nivel.esta_bloqueado(new_rect, jogador=self):
                self.rect.y = new_rect.y

    def tentar_coletar(self, itens: List['Item']) -> Optional['Item']:
        if len(self.saco_lixo) >= self.capacidade:
            return None
        for it in itens:
            if self.rect.colliderect(it.rect):
                self.saco_lixo.append(it.tipo)
                return it
        return None

    def tentar_depositar(self, lixeiras: List['Lixeira']) -> int:
        depositado = 0
        for l in lixeiras:
            if self.rect.colliderect(l.rect) and self.saco_lixo:
                parent = getattr(l, 'centro_pai', None)
                if parent is not None and parent is not self.dentro_centro:
                    continue
                restantes = []
                for t in self.saco_lixo:
                    if l.tipo == TipoLixo.GENERICO or t == l.tipo:
                        depositado += 1
                    else:
                        restantes.append(t)
                self.saco_lixo = restantes
        return depositado

    def desenhar(self, surf: pygame.Surface):
        pygame.draw.rect(surf, (255, 255, 0), self.rect, border_radius=6)
        bar_w = 40
        filled = int(bar_w * (len(self.saco_lixo) / self.capacidade))
        bar = pygame.Rect(self.rect.centerx - bar_w//2, self.rect.top - 12, bar_w, 6)
        pygame.draw.rect(surf, (70,70,70), bar, border_radius=3)
        if filled > 0:
            fill_rect = pygame.Rect(bar.x, bar.y, filled, bar.h)
            pygame.draw.rect(surf, (0,200,0), fill_rect, border_radius=3)

class Inimigo:
    def __init__(self, rect: pygame.Rect, velocidade: float = 2.2):
        self.rect = rect
        self.velocidade = velocidade

    def atualizar(self, alvo: pygame.Rect, limites: pygame.Rect):
        import math
        dx = alvo.centerx - self.rect.centerx
        dy = alvo.centery - self.rect.centery
        dist = math.hypot(dx, dy) or 1.0
        vx = self.velocidade * dx / dist
        vy = self.velocidade * dy / dist
        self.rect.x += int(vx)
        self.rect.y += int(vy)
        self.rect.clamp_ip(limites)

    def desenhar(self, surf: pygame.Surface):
        pygame.draw.rect(surf, (255, 60, 60), self.rect, border_radius=6)
