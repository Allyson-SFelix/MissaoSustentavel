import pygame_menu
import pygame
import sys

# Importa o caminho da fonte do config.py
from MissaoSustentavel.missao_sustentavel.config import CAMINHO_FONTE

class UsernameTela:
    def __init__(self, tela):
        self.username = ""
        self.tela = tela

        # Criação de um tema personalizado com sua fonte
        tema_personalizado = pygame_menu.themes.THEME_DARK.copy()
        tema_personalizado.title_font = CAMINHO_FONTE
        tema_personalizado.widget_font = CAMINHO_FONTE
        tema_personalizado.title_font_size = 50
        tema_personalizado.widget_font_size = 40
        tema_personalizado.title_background_color = (20, 20, 20)
        tema_personalizado.widget_alignment = pygame_menu.locals.ALIGN_CENTER

        # Criação do menu com a fonte personalizada
        self.menu = pygame_menu.Menu(
            "Bem-vindo!",
            1000,
            600,
            theme=tema_personalizado
        )

    def salvarInf(self, username, label):
        if len(username) <= 25 and len(username) > 0:
            self.username = username
            label.set_title('LEGAL')
            self.menu.disable()
        else:
            label.set_title('Campo vazio')

    def run(self):
        label = self.menu.add.label("Digite seu nome de usuário", max_char=100)

        username = self.menu.add.text_input(
            title=" ",
            maxchar=25,
            width=300,
            background_color=(0, 0, 0)
        )

        self.menu.add.button("Continuar", lambda: self.salvarInf(username.get_value().strip(), label))

        self.menu.mainloop(self.tela)

        return self.username
