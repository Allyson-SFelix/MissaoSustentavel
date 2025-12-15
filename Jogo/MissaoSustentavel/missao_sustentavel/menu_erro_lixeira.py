"""
Menu de Erro Lixeira - Exibe mensagem quando lixo é jogado na lixeira errada
"""

import pygame
from .config import LARGURA, ALTURA, COR_FUNDO, NOME_FONTE
from .enums import TIPO_NOMES, CORES_LIXEIRA


class MenuErroLixeira:
    """Menu que aparece quando o jogador joga lixo na lixeira errada"""
    
    def __init__(self, tipo_lixo, tipo_lixeira_correta):
        """
        Inicializa o menu de erro
        
        Args:
            tipo_lixo: TipoLixo - tipo de lixo que foi jogado errado
            tipo_lixeira_correta: TipoLixo - tipo correto da lixeira
        """
        self.tipo_lixo = tipo_lixo
        self.tipo_lixeira_correta = tipo_lixeira_correta
        self.font_grande = pygame.font.SysFont(NOME_FONTE, 40)
        self.font_media = pygame.font.SysFont(NOME_FONTE, 28)
        self.font_pequena = pygame.font.SysFont(NOME_FONTE, 20)
    
    def processar_entrada(self, key):
        """Processa qualquer entrada para fechar o menu"""
        # Qualquer tecla fecha o menu
        return True
    
    def desenhar(self, surf: pygame.Surface):
        """Desenha o menu na tela"""
        # Desenhar overlay semi-transparente com cor vermelha
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(150)
        overlay.fill((139, 0, 0))  # Vermelho escuro
        surf.blit(overlay, (0, 0))
        
        # Caixa de diálogo
        caixa_width = 500
        caixa_height = 300
        caixa_x = (LARGURA - caixa_width) // 2
        caixa_y = (ALTURA - caixa_height) // 2
        
        pygame.draw.rect(surf, (50, 50, 50), (caixa_x, caixa_y, caixa_width, caixa_height))
        pygame.draw.rect(surf, (255, 0, 0), (caixa_x, caixa_y, caixa_width, caixa_height), 3)
        
        # Título de erro
        titulo = "ERRO! LIXEIRA ERRADA"
        titulo_surf = self.font_grande.render(titulo, True, (255, 100, 100))
        titulo_rect = titulo_surf.get_rect(center=(LARGURA // 2, caixa_y + 40))
        surf.blit(titulo_surf, titulo_rect)
        
        # Mensagem de lixo jogado errado
        nome_lixo = TIPO_NOMES.get(self.tipo_lixo, "Desconhecido")
        mensagem1 = f"Você tentou jogar: {nome_lixo}"
        mensagem1_surf = self.font_media.render(mensagem1, True, (255, 200, 200))
        mensagem1_rect = mensagem1_surf.get_rect(center=(LARGURA // 2, caixa_y + 110))
        surf.blit(mensagem1_surf, mensagem1_rect)
        
        # Linha separadora
        pygame.draw.line(surf, (200, 200, 200), (caixa_x + 20, caixa_y + 160), (caixa_x + caixa_width - 20, caixa_y + 160), 2)
        
        # Mensagem de lixeira correta
        mensagem2 = "Lixeira correta:"
        mensagem2_surf = self.font_pequena.render(mensagem2, True, (200, 255, 200))
        mensagem2_rect = mensagem2_surf.get_rect(center=(LARGURA // 2, caixa_y + 190))
        surf.blit(mensagem2_surf, mensagem2_rect)
        
        # Bloco de cor da lixeira correta
        cor_lixeira = CORES_LIXEIRA.get(self.tipo_lixeira_correta, (100, 100, 100))
        nome_lixeira_correta = TIPO_NOMES.get(self.tipo_lixeira_correta, "Desconhecido")
        
        bloco_x = (LARGURA // 2) - 60
        bloco_y = caixa_y + 220
        bloco_size = 30
        
        pygame.draw.rect(surf, cor_lixeira, (bloco_x, bloco_y, bloco_size, bloco_size))
        pygame.draw.rect(surf, (255, 255, 255), (bloco_x, bloco_y, bloco_size, bloco_size), 2)
        
        # Nome da lixeira correta
        nome_correta_surf = self.font_media.render(nome_lixeira_correta, True, (200, 255, 200))
        nome_correta_rect = nome_correta_surf.get_rect(topleft=(bloco_x + bloco_size + 20, bloco_y + 2))
        surf.blit(nome_correta_surf, nome_correta_rect)
        
        # Instrução para fechar
        instrucao = "Pressione qualquer tecla para continuar"
        instrucao_surf = self.font_pequena.render(instrucao, True, (200, 200, 200))
        instrucao_rect = instrucao_surf.get_rect(center=(LARGURA // 2, caixa_y + caixa_height - 20))
        surf.blit(instrucao_surf, instrucao_rect)
