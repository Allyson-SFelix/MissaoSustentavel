import pygame_menu
import pygame
import sys
from MissaoSustentavel.missao_sustentavel.game import Jogo
from MissaoSustentavel.missao_sustentavel.config import CAMINHO_FONTE  # importa o caminho da fonte


class MenuPrincipal:
    def __init__(self, tela, usuario):
        self.tela = tela
        self.usuario = usuario

        # Criação de um tema personalizado usando sua fonte
        tema_personalizado = pygame_menu.themes.THEME_DARK.copy()
        tema_personalizado.title_font = CAMINHO_FONTE
        tema_personalizado.widget_font = CAMINHO_FONTE
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
        imagem_original = pygame.image.load("assets/logo.png").convert_alpha()
        logo_redimensionado = pygame.transform.scale(imagem_original, (652, 276))
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

    def carregar_game(self):
        pass

    def fechar_jogo(self):
        pygame.quit()
        sys.exit()

    def run(self):
        self.menu.add.button('Iniciar Jogo', self.start_game)
        self.menu.add.button('Carregar Jogo', self.carregar_game)
        self.menu.add.button('Sair do Jogo', self.fechar_jogo)
        self.menu.mainloop(self.tela)