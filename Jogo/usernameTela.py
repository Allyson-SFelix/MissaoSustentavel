import pygame_menu
import pygame
import sys
#from game import Game

class UsernameTela:
    def __init__(self,tela):
        self.username=""
        self.tela=tela
        
        #config tela e criacao
        self.menu=pygame_menu.Menu("",1000,600, theme=pygame_menu.themes.THEME_DARK) 

        
    def salvarInf(self,username,label):
        return 
    
    def run(self):
        label=self.menu.add.label('Digite seu username',max_char=100)
        
        username=self.menu.add.text_input(maxchar=25,title=" ",width=300,background_color=(0,0,0))
        self.menu.add.button("Submit",lambda:self.salvarInf(username.get_value().strip(),label))
        
        self.menu.mainloop(self.tela)
        
        return self.username
        
        