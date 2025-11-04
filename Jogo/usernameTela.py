import pygame_menu
import pygame
import sys
import os

# Configura o diretório de assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets")
FONTE_PERSONALIZADA = os.path.join(IMG_DIR, "BoldPixels.ttf")

class UsernameTela:
    def __init__(self, tela):
        self.username = ""
        self.tela = tela

        # Criação de um tema personalizado com a fonte personalizada
        tema_personalizado = pygame_menu.themes.THEME_DARK.copy()
        tema_personalizado.title_font = FONTE_PERSONALIZADA
        tema_personalizado.widget_font = FONTE_PERSONALIZADA
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
            label.set_title('✨ Nome registrado com sucesso!')
            # Pequeno delay para mostrar a mensagem de sucesso
            pygame.time.wait(800)
            self.menu.disable()
        else:
            label.set_title('❌ Por favor, digite um nome válido')

    def run(self):
        # Adiciona espaço vertical antes do conteúdo
        self.menu.add.vertical_margin(30)

        # Adiciona o label com o texto de instruções
        label = self.menu.add.label("Digite seu nome de usuário", max_char=100)
        
        # Adiciona espaço entre o label e o input
        self.menu.add.vertical_margin(20)

        # Campo de entrada de texto personalizado
        username = self.menu.add.text_input(
            title=" ",
            maxchar=25,
            width=300,
            background_color=(20, 26, 30),  # Cor mais escura para o fundo
            selection_color=(100, 200, 100),  # Cor de seleção verde
            border_width=2  # Borda mais fina
        )

        # Adiciona espaço entre o input e o botão
        self.menu.add.vertical_margin(30)

        # Botão de continuar personalizado
        self.menu.add.button(
            "Continuar",
            lambda: self.salvarInf(username.get_value().strip(), label),
            background_color=(40, 120, 40)  # Cor verde escuro para o botão
        )

        self.menu.mainloop(self.tela)

        return self.username