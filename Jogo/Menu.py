import pygame_menu
import pygame
import sys
#from game import Game

class MenuPrincipal:
    def __init__(self, tela, username):
        self.tela =tela
        self.username = username
        
        #config tela e criacao
        self.menu=pygame_menu.Menu(f'Bem-vindo, {self.username}!',1000,600, theme=pygame_menu.themes.THEME_DARK) 

    
    def start_game(self):
            #game = Game(self.username)
            #game.run()
            self.menu.add.button('rodando')

    def carregar_game(self):
        return
    
    def fechar_jogo():
        pygame.quit()  # fecha a interface
        sys.exit()     # para de rodar
    
    def run(self):
        self.menu.add.button('Iniciar Jogo', self.start_game)
        self.menu.add.button('Carregar Jogo', self.carregar_game)
        self.menu.add.button('Sair Jogo', self.fechar_jogo) 
        self.menu.mainloop(self.tela)
