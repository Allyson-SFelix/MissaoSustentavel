import pygame_menu
import pygame
import sys
from MissaoSustentavel.game import Jogo

class MenuPrincipal:
    def __init__(self, tela, usuario):
        self.tela = tela
        self.usuario = usuario

        self.menu = pygame_menu.Menu(
            f'Bem-vindo, {self.usuario.username}!',
            1000,
            600,
            theme=pygame_menu.themes.THEME_DARK
        )

        imagem_original = pygame.image.load("assets/logo.png").convert_alpha()
        logo_redimensionado = pygame.transform.scale(imagem_original, (652 , 276))
        self.menu.add.surface(
            logo_redimensionado,
            margin=(0, 5)
        )

    def start_game(self):
        self.menu.disable()
        jogo = Jogo(self.usuario)
        jogo.executar()

    def carregar_game(self):
        pass
    
    def fechar_jogo(self):
        pygame.quit()
        sys.exit()
    
    def run(self):
        self.menu.add.button('Iniciar Jogo', self.start_game)
        self.menu.add.button('Carregar Jogo', self.carregar_game)
        self.menu.add.button('Sair Jogo', self.fechar_jogo) 
        self.menu.mainloop(self.tela)