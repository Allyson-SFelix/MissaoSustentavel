import pygame_menu
import pygame
import sys
#from .game import Game

class MenuPrincipal:
    def __init__(self, tela, usuario):
        self.tela =tela
        self.usuario = usuario
        
        #config tela e criacao
        self.menu=pygame_menu.Menu(f'Bem-vindo, {self.usuario.username}!',1000,600, theme=pygame_menu.themes.THEME_DARK) 

    
    def start_game(self):
            game = Game(self.usuario) # passa o objeto como parametro
            game.run()

    def carregar_game(self):
        return
    
    def fechar_jogo(event):
        pygame.quit()  # fecha a interface
        sys.exit()     # para de rodar
    
    def run(self):
        self.menu.add.button('Iniciar Jogo', self.start_game)
        self.menu.add.button('Carregar Jogo', self.carregar_game)
        self.menu.add.button('Sair Jogo', self.fechar_jogo) 
        self.menu.mainloop(self.tela)
