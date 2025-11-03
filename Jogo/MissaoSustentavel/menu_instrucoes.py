"""
Menu de Instruções - Exibe instruções e contexto no início de cada fase
"""

import pygame
from .config import LARGURA, ALTURA, NOME_FONTE


class MenuInstrucoes:
    """Tela que exibe instruções e contexto da fase por 4 segundos antes de permitir continuar"""

    def __init__(self, numero_fase: int):
        self.numero_fase = numero_fase
        self.tempo_inicio = pygame.time.get_ticks()
        self.duracao = 4000  # 4 segundos em milissegundos
        self.trava_pular = 4000  # tempo mínimo antes de poder pular

        # Fontes
        self.font_titulo = pygame.font.SysFont(NOME_FONTE, 48, bold=True)
        self.font_grande = pygame.font.SysFont(NOME_FONTE, 36, bold=True)
        self.font_media = pygame.font.SysFont(NOME_FONTE, 28)
        self.font_pequena = pygame.font.SysFont(NOME_FONTE, 22)

        # Contextos das ODS por fase
        self.contextos = {
            1: "ODS 12: Consumo e Produção Responsável\nColeta lixo genérico para reciclagem!",
            2: "ODS 12: Consumo e Produção Responsável\nSepare orgânico de plástico corretamente!",
            3: "ODS 12: Consumo e Produção Responsável\nTrate papel, vidro e metal adequadamente!",
            4: "ODS 12 e ODS 13: Ação Climática\nDesafio final: complete a reciclagem com agilidade!",
        }

    def desenhar(self, surf: pygame.Surface):
        """Desenha a tela de instruções"""
        # Fundo semi-transparente
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(200)
        overlay.fill((20, 26, 30))
        surf.blit(overlay, (0, 0))

        # Título da fase
        titulo = f"FASE {self.numero_fase:02d}"
        titulo_surf = self.font_titulo.render(titulo, True, (255, 215, 0))
        titulo_rect = titulo_surf.get_rect(center=(LARGURA // 2, 60))
        surf.blit(titulo_surf, titulo_rect)

        # Linha separadora
        pygame.draw.line(surf, (100, 200, 100), (100, 120), (LARGURA - 100, 120), 3)

        # Objetivo do jogo
        y_offset = 140
        objetivo_titulo = self.font_grande.render("OBJETIVO:", True, (255, 100, 100))
        surf.blit(objetivo_titulo, (100, y_offset))
        y_offset += 50

        objetivo_texto = "Colete lixo espalhado pelo mapa e leve-o"
        objetivo_surf = self.font_media.render(objetivo_texto, True, (200, 200, 255))
        surf.blit(objetivo_surf, (110, y_offset))
        y_offset += 35

        objetivo_texto2 = "ao Centro de Reciclagem para classificá-lo na lixeira certa!"
        objetivo_surf2 = self.font_media.render(objetivo_texto2, True, (200, 200, 255))
        surf.blit(objetivo_surf2, (110, y_offset))
        y_offset += 40

        # Segunda linha separadora
        pygame.draw.line(surf, (100, 200, 100), (100, y_offset + 10), (LARGURA - 100, y_offset + 10), 3)

        # Instruções de movimentação
        y_offset += 30

        # Título das instruções
        instr_titulo = self.font_grande.render("MOVIMENTAÇÃO:", True, (100, 220, 100))
        surf.blit(instr_titulo, (100, y_offset))
        y_offset += 60

        # Instruções individuais
        instrucoes = [
            ("W", "Mover para CIMA"),
            ("S", "Mover para BAIXO"),
            ("D", "Mover para DIREITA"),
            ("A", "Mover para ESQUERDA"),
        ]

        # Salvar y_offset inicial para MOVIMENTAÇÃO
        y_mov_inicio = y_offset
        y_mov = y_mov_inicio
        for tecla, descricao in instrucoes:
            tecla_surf = self.font_media.render(tecla, True, (0, 0, 0))
            tecla_rect = tecla_surf.get_rect(topleft=(120, y_mov + 5))
            
            tecla_bg = pygame.Rect(110, y_mov, 40, 40)
            pygame.draw.rect(surf, (100, 220, 100), tecla_bg, border_radius=5)
            pygame.draw.rect(surf, (255, 255, 255), tecla_bg, 2, border_radius=5)
            surf.blit(tecla_surf, tecla_rect)

            desc_surf = self.font_pequena.render(descricao, True, (200, 255, 200))
            surf.blit(desc_surf, (170, y_mov + 8))

            y_mov += 50

        # Outros controles ao lado (começar na mesma altura da MOVIMENTAÇÃO)
        outros_titulo = self.font_grande.render("OUTROS CONTROLES:", True, (100, 200, 255))
        surf.blit(outros_titulo, (LARGURA // 2 + 50, y_mov_inicio - 60))

        # Outros controles
        outros_controles = [
            ("ESPAÇO", "Pegar item", 90),  # Botão maior para ESPAÇO
            ("F", "Entrar no Centro", 40),
            ("R", "Reiniciar fase", 40),
            ("ESC", "Ir para o menu", 40),
        ]

        y_outros = y_mov_inicio
        for tecla, descricao, btn_width in outros_controles:
            tecla_surf = self.font_media.render(tecla, True, (0, 0, 0))
            tecla_x = LARGURA // 2 + 60 + (btn_width - tecla_surf.get_width()) // 2
            tecla_rect = tecla_surf.get_rect(topleft=(tecla_x, y_outros + (40 - tecla_surf.get_height()) // 2))
            
            tecla_bg = pygame.Rect(LARGURA // 2 + 60, y_outros, btn_width, 40)
            pygame.draw.rect(surf, (100, 200, 255), tecla_bg, border_radius=5)
            pygame.draw.rect(surf, (255, 255, 255), tecla_bg, 2, border_radius=5)
            surf.blit(tecla_surf, tecla_rect)

            desc_x = LARGURA // 2 + 60 + btn_width + 15
            desc_surf = self.font_pequena.render(descricao, True, (200, 220, 255))
            surf.blit(desc_surf, (desc_x, y_outros + 8))

            y_outros += 50

        # Calcular o y_offset final (usar o maior dos dois)
        y_offset = max(y_mov, y_outros)

        # (Linha separadora removida daqui)

        # Contexto e ODS
        y_offset += 60
        contexto = self.contextos.get(self.numero_fase, "Ajude a salvar o planeta!")
        linhas = contexto.split("\n")
        
        for linha in linhas:
            if linha.startswith("ODS"):
                linha_surf = self.font_media.render(linha, True, (255, 215, 0))
            else:
                linha_surf = self.font_pequena.render(linha, True, (200, 255, 200))
            linha_rect = linha_surf.get_rect(center=(LARGURA // 2, y_offset))
            surf.blit(linha_surf, linha_rect)
            y_offset += 45

        # Instrução para continuar (só aparece após 4 segundos)
        tempo_decorrido = pygame.time.get_ticks() - self.tempo_inicio
        y_offset += 30
        if tempo_decorrido >= self.trava_pular:
            texto = "Pressione qualquer tecla para começar..."
            cor = (150, 150, 150)
        else:
            texto = f"Aguarde {int((self.trava_pular - tempo_decorrido) / 1000) + 1}s..."
            cor = (200, 100, 100)

        continua = self.font_pequena.render(texto, True, cor)
        continua_rect = continua.get_rect(center=(LARGURA // 2, y_offset))
        surf.blit(continua, continua_rect)

        # Barra de progresso
        progresso = (pygame.time.get_ticks() - self.tempo_inicio) / self.duracao
        progresso = min(progresso, 1.0)
        barra_y = ALTURA - 30
        barra_width = 300
        barra_x = (LARGURA - barra_width) // 2

        pygame.draw.rect(surf, (70, 70, 70), (barra_x, barra_y, barra_width, 20), border_radius=5)
        if progresso > 0:
            preenchimento_width = int(barra_width * progresso)
            pygame.draw.rect(surf, (100, 220, 100), (barra_x, barra_y, preenchimento_width, 20), border_radius=5)
        pygame.draw.rect(surf, (150, 150, 150), (barra_x, barra_y, barra_width, 20), 2, border_radius=5)

    def tempo_expirou(self) -> bool:
        """Verifica se já se passaram os 4 segundos"""
        return (pygame.time.get_ticks() - self.tempo_inicio) >= self.duracao

    def pode_pular(self) -> bool:
        """Retorna True se já se passaram os 4 segundos mínimos"""
        return (pygame.time.get_ticks() - self.tempo_inicio) >= self.trava_pular

    def obter_progresso(self) -> float:
        """Retorna o progresso (0 a 1) do tempo decorrido"""
        progresso = (pygame.time.get_ticks() - self.tempo_inicio) / self.duracao
        return min(progresso, 1.0)
