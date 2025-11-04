#classe com is dados do usuário : username e fase atual
class User:
    def __init__(self,username,faseAtual):
        self.username=username
        self.faseAtual=faseAtual
    
    def mostrar(self):
        print("Username="+self.username+"\nFase atual"+self.faseAtual)
        