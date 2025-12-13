import pygame_menu
import pygame
import sys
import os
from MissaoSustentavel.game import Jogo

# Configura o diretório de assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets")
FONTE_PERSONALIZADA = os.path.join(IMG_DIR, "BoldPixels.ttf")


class MenuPrincipal:
    def __init__(self, tela, usuario):
        self.tela = tela
        self.usuario = usuario

        # Criação de um tema personalizado usando a fonte personalizada
        tema_personalizado = pygame_menu.themes.THEME_DARK.copy()
        tema_personalizado.title_font = FONTE_PERSONALIZADA
        tema_personalizado.widget_font = FONTE_PERSONALIZADA
        tema_personalizado.title_font_size = 50
        tema_personalizado.widget_font_size = 36
        tema_personalizado.title_background_color = (20, 20, 20)
        tema_personalizado.widget_alignment = pygame_menu.locals.ALIGN_CENTER

        # Criação do menu principal
        self.menu = pygame_menu.Menu(
            f'Bem-vindo, {self.usuario.username}!',
            1000,
            600,
            theme=tema_personalizado
        )

        # Logo redimensionado
        imagem_original = pygame.image.load(os.path.join(IMG_DIR, "logo.png")).convert_alpha()
        logo_redimensionado = pygame.transform.scale(imagem_original, (612, 273))
        self.menu.add.surface(
            logo_redimensionado,
            margin=(0, 5)
        )

    def start_game(self):
        self.menu.disable()
        jogo = Jogo(self.usuario)
        jogo.executar()

        # Quando o jogador sai do jogo (com ESC), volta ao menu principal
        self.menu.enable()
        while True:
            eventos = pygame.event.get()
            if self.menu.is_enabled():
                self.menu.update(eventos)
                self.menu.draw(self.tela)
            pygame.display.flip()

            for e in eventos:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def fechar_jogo(self):
        pygame.quit()
        sys.exit()

    def _mostrar_aviso_sem_progresso(self):
        """Mostra um aviso informando que não há progresso salvo"""
        tema_aviso = pygame_menu.themes.THEME_DARK.copy()
        tema_aviso.title_font_size = 35
        tema_aviso.widget_font_size = 28
        
        menu_aviso = pygame_menu.Menu(
            'Sem Progresso',
            800,
            250,
            theme=tema_aviso
        )
        
        menu_aviso.add.label('Nenhum progresso salvo!')
        menu_aviso.add.label('Comece um novo jogo.')
        menu_aviso.add.button('Voltar', menu_aviso.disable)
        
        menu_aviso.mainloop(self.tela)
    def run(self):
        # Adicionando botões com espaçamento para melhor visual
        self.menu.add.vertical_margin(20)  # Espaço após o logo
        self.menu.add.button('Iniciar Jogo', self.start_game)
        self.menu.add.vertical_margin(10)  # Espaço entre botões
        self.menu.add.button('Sair do Jogo', self.fechar_jogo)
        self.menu.mainloop(self.tela)