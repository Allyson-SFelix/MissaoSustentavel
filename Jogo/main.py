import pygame
#from login import Login
from Menu import MenuPrincipal

#constantes
TELA_TAMANHO_X=1000
TELA_TAMANHO_Y=600

pygame.init()
tela = pygame.display.set_mode((TELA_TAMANHO_X, TELA_TAMANHO_Y))
pygame.display.set_caption("Missão Sustentável")

# Etapa 1: login
#login = Login(tela)
#username = login.run()  # retorna o nome do jogador


# Etapa acesso menu
username="tatu Voador"
menu = MenuPrincipal(tela, username) #cria instancia de menu
menu.run() #cria tela e execução do jogo

