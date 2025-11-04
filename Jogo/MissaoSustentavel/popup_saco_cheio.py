"""
Popup de Saco Cheio - Exibe uma pequena mensagem no canto superior direito
avisando o jogador para ir ao centro de reciclagem quando a mochila está cheia.
"""

import pygame
from .config import LARGURA, ALTURA, NOME_FONTE


class PopupSacoCheio:
    """Pequeno aviso no canto superior direito da tela"""

    def __init__(self):
        self.tempo_inicio = pygame.time.get_ticks()
        self.duracao = 3000  # 3 segundos em milissegundos
        self.mostrar = True

        # Fonte
        self.font_titulo = pygame.font.SysFont(NOME_FONTE, 26, bold=True)
        self.font_texto = pygame.font.SysFont(NOME_FONTE, 22)

    def desenhar(self, surf: pygame.Surface):
        """Desenha o pequeno popup no canto superior direito"""
        if not self.mostrar:
            return

        # Dimensões da caixinha
        largura_caixa = 320
        altura_caixa = 80
        margem = 20

        x = LARGURA - largura_caixa - margem
        y = margem

        # Fundo da caixa
        pygame.draw.rect(surf, (40, 40, 40), (x, y, largura_caixa, altura_caixa), border_radius=10)
        pygame.draw.rect(surf, (255, 215, 0), (x, y, largura_caixa, altura_caixa), 2, border_radius=10)

        # Título
        titulo = "Mochila cheia!"
        titulo_surf = self.font_titulo.render(titulo, True, (255, 215, 0))
        surf.blit(titulo_surf, (x + 15, y + 10))

        # Mensagem
        mensagem = "Vá ao centro de reciclagem."
        msg_surf = self.font_texto.render(mensagem, True, (230, 230, 230))
        surf.blit(msg_surf, (x + 15, y + 40))

        # Barra de progresso simples
        progresso = (pygame.time.get_ticks() - self.tempo_inicio) / self.duracao
        progresso = min(progresso, 1.0)

        barra_width = largura_caixa - 40
        barra_height = 8
        barra_x = x + 20
        barra_y = y + altura_caixa - 15

        pygame.draw.rect(surf, (80, 80, 80), (barra_x, barra_y, barra_width, barra_height), border_radius=5)
        pygame.draw.rect(
            surf,
            (100, 220, 100),
            (barra_x, barra_y, int(barra_width * (1 - progresso)), barra_height),
            border_radius=5
        )

    def tempo_expirou(self) -> bool:
        """Verifica se o popup já expirou"""
        return (pygame.time.get_ticks() - self.tempo_inicio) >= self.duracao

    def fechar(self):
        """Fecha o popup manualmente"""
        self.mostrar = False
