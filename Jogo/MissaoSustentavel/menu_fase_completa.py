"""
Menu de Conclusão de Fase - Gerencia a tela quando jogador completa uma fase
"""

import pygame
from .config import LARGURA, ALTURA, COR_FUNDO, NOME_FONTE


class BotaoMenu:
    """Representa um botão no menu"""
    
    def __init__(self, texto: str, posicao: tuple, tamanho: tuple):
        self.texto = texto
        self.rect = pygame.Rect(posicao[0], posicao[1], tamanho[0], tamanho[1])
        self.selecionado = False
        self.cor_normal = (50, 120, 180)
        self.cor_selecionada = (100, 200, 255)
    
    def verificar_colisao_mouse(self, mouse_pos):
        """Verifica se o mouse está sobre o botão"""
        self.selecionado = self.rect.collidepoint(mouse_pos)
    
    def desenhar(self, surf: pygame.Surface, font: pygame.font.Font):
        """Desenha o botão na tela"""
        cor = self.cor_selecionada if self.selecionado else self.cor_normal
        pygame.draw.rect(surf, cor, self.rect)
        pygame.draw.rect(surf, (255, 255, 255), self.rect, 2)
        
        text_surf = font.render(self.texto, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surf.blit(text_surf, text_rect)


class MenuFaseCompleta:
    """Menu que aparece quando o jogador completa uma fase"""
    
    def __init__(self, numero_fase: int):
        """Inicializa o menu de conclusão"""
        self.numero_fase = numero_fase
        self.font = pygame.font.SysFont(NOME_FONTE, 32)
        self.font_pequena = pygame.font.SysFont(NOME_FONTE, 24)
        
        # Criar botões
        botao_width = 150
        botao_height = 50
        espacamento_x = 50
        
        botao_continuar_x = (LARGURA // 2) - botao_width - (espacamento_x // 2)
        botao_sair_x = (LARGURA // 2) + (espacamento_x // 2)
        botao_y = (ALTURA // 2) + 80
        
        self.botao_continuar = BotaoMenu("CONTINUAR", (botao_continuar_x, botao_y), (botao_width, botao_height))
        self.botao_sair = BotaoMenu("SAIR", (botao_sair_x, botao_y), (botao_width, botao_height))
        
        self.botao_selecionado = 0  # 0 = continuar, 1 = sair
    
    def processar_entrada_teclado(self, key):
        """Processa entrada do teclado"""
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.botao_selecionado = 0
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.botao_selecionado = 1
        elif key == pygame.K_RETURN:
            if self.botao_selecionado == 0:
                return "continuar"
            else:
                return "sair"
        return None
    
    def processar_clique_mouse(self, mouse_pos):
        """Processa clique do mouse"""
        if self.botao_continuar.rect.collidepoint(mouse_pos):
            return "continuar"
        elif self.botao_sair.rect.collidepoint(mouse_pos):
            return "sair"
        return None
    
    def atualizar_mouse_hover(self, mouse_pos):
        """Atualiza o estado dos botões ao mover o mouse"""
        self.botao_continuar.verificar_colisao_mouse(mouse_pos)
        self.botao_sair.verificar_colisao_mouse(mouse_pos)
        
        if self.botao_continuar.selecionado:
            self.botao_selecionado = 0
        elif self.botao_sair.selecionado:
            self.botao_selecionado = 1
    
    def desenhar(self, surf: pygame.Surface):
        """Desenha o menu na tela"""
        # Desenhar overlay semi-transparente
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        surf.blit(overlay, (0, 0))
        
        # Desenhar título
        titulo = "🎉 FASE COMPLETA! 🎉"
        titulo_surf = self.font.render(titulo, True, (255, 255, 100))
        titulo_rect = titulo_surf.get_rect(center=(LARGURA // 2, ALTURA // 2 - 100))
        surf.blit(titulo_surf, titulo_rect)
        
        # Desenhar mensagem
        mensagem = f"Fase {self.numero_fase} concluída com sucesso!"
        mensagem_surf = self.font_pequena.render(mensagem, True, (255, 255, 255))
        mensagem_rect = mensagem_surf.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20))
        surf.blit(mensagem_surf, mensagem_rect)
        
        # Desenhar botões
        self.botao_continuar.desenhar(surf, self.font_pequena)
        self.botao_sair.desenhar(surf, self.font_pequena)
