"""
Menu de Conclusão de Fase - Gerencia a tela quando jogador completa uma fase
"""

import pygame
from .config import LARGURA, ALTURA, NOME_FONTE


class MenuFaseCompleta:
    """Tela exibida quando o jogador completa uma fase (exceto a última)"""

    def __init__(self, numero_fase: int):
        self.numero_fase = numero_fase
        self.eh_ultima = self.numero_fase == 4  # a fase 4 é a última
        self.acao_selecionada = None  # "proxima" ou "menu_principal"

        # Fontes
        self.font_titulo = pygame.font.SysFont(NOME_FONTE, 72, bold=True)
        self.font_mensagem = pygame.font.SysFont(NOME_FONTE, 36)
        self.font_instrucao = pygame.font.SysFont(NOME_FONTE, 28, bold=True)

        # Timer
        self.tempo_inicio = pygame.time.get_ticks()

    def desenhar(self, surf: pygame.Surface):
        """Desenha a tela de fase completa (somente se não for a última)"""
        if self.eh_ultima:
            return  # não desenha nada na última fase

        # Fundo semi-transparente
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        surf.blit(overlay, (0, 0))

        # --- Título ---
        titulo = "FASE COMPLETA!"
        titulo_sombra = self.font_titulo.render(titulo, True, (0, 0, 0))
        titulo_surf = self.font_titulo.render(titulo, True, (255, 255, 100))
        titulo_rect = titulo_surf.get_rect(center=(LARGURA // 2, ALTURA // 2 - 120))
        surf.blit(titulo_sombra, (titulo_rect.x + 3, titulo_rect.y + 3))
        surf.blit(titulo_surf, titulo_rect)

        # --- Mensagem de conclusão ---
        mensagem = f"Fase {self.numero_fase} concluída com sucesso!"
        mensagem_surf = self.font_mensagem.render(mensagem, True, (255, 255, 255))
        mensagem_rect = mensagem_surf.get_rect(center=(LARGURA // 2, ALTURA // 2 - 40))
        surf.blit(mensagem_surf, mensagem_rect)

        # --- Instrução (com quebra de linha manual) ---
        instrucao = (
            "Aperte [ESPAÇO] para avançar para o próximo nível\n"
            "[ESC] para voltar ao menu"
        )
        linhas = instrucao.split("\n")

        # Posição vertical inicial (um pouco abaixo da mensagem)
        y_base = ALTURA // 2 + 60
        for i, linha in enumerate(linhas):
            instrucao_surf = self.font_instrucao.render(linha, True, (200, 200, 200))
            instrucao_rect = instrucao_surf.get_rect(center=(LARGURA // 2, y_base + i * 40))
            surf.blit(instrucao_surf, instrucao_rect)

    def processar_entrada_teclado(self, tecla):
        """Processa entrada de teclado (ESPAÇO para próxima, ESC para menu)"""
        if tecla == pygame.K_SPACE:
            self.acao_selecionada = "proxima"
            return "proxima"
        return None

    def obter_acao(self):
        """Retorna a ação selecionada pelo usuário"""
        return self.acao_selecionada

    def tempo_expirou(self) -> bool:
        """Retorna True se já se passaram 2 segundos"""
        return (pygame.time.get_ticks() - self.tempo_inicio) >= 2000
