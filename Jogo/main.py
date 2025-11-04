import pygame
from usernameTela import UsernameTela
from Menu import MenuPrincipal
from BancoManipulacao import BancoManip

#constantes
TELA_TAMANHO_X=1000
TELA_TAMANHO_Y=600

pygame.init()
tela = pygame.display.set_mode((TELA_TAMANHO_X, TELA_TAMANHO_Y))
pygame.display.set_caption("Missão Sustentável")

# Etapa 1: login
user = UsernameTela(tela)
username=user.run()  # retorna o nome do jogador

# Etapa 2 : acessar json e captar
bancoJson = BancoManip()
usuario=bancoJson.inicializarAcessoBanco(username)

# Etapa 3: acesso menu
menu = MenuPrincipal(tela, usuario) #cria instancia de menu
menu.run() #cria tela e execução do jogo



