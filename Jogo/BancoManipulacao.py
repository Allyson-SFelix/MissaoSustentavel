import json
import os
#from Model.users import User

# pega o diretório onde o arquivo BancoManipulacao.py está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# caminho completo para o JSON dentro da pasta DataBase
ARQUIVO_JSON = os.path.join(BASE_DIR, "DataBase", "BD.json")

class BancoManip:
    def __init__(self):
        self.dados={}
        
    def ler(self):
        with open(ARQUIVO_JSON,"r") as arquivo:
            self.dados=json.load(arquivo) #pega lista de dicionarios
            
    def escrever(self):
        with open(ARQUIVO_JSON,"w") as arquivo:
            json.dump(self.dados, arquivo, indent=2)
        
    def atualizarFaseAtual(self,user):
        self.dados[user.username]["FaseAtual"]=user.faseAtual
        self.escrever()
        return True
        
    def buscaDados(self,username):
        if username in self.dados:
            userCadastrado = self.dados[username]
            return User(username,userCadastrado.get("FaseAtual",0)) 
        else:
            self.criarDict(username)
            self.escrever()
            return User(username,0)

    def criarArquivo(self):
        with open(ARQUIVO_JSON,"w") as arquivo:
            json.dump({}, arquivo, indent=2)
            
    
    def criarDict(self,username):
        self.dados[username]={"FaseAtual":0}
        
    
    def inicializarAcessoBanco(self,username):
    #verifico se existe ou nao, depois direciono para as outras funções   
        if not os.path.exists(ARQUIVO_JSON): #crio arquivo
            self.criarArquivo()
            self.criarDict(username)
            self.escrever()
            return "USER NOVO, SALVO"
        else: #leio arquivo
            self.ler()
            return self.buscaDados(username)




banco = BancoManip()

resposta=banco.inicializarAcessoBanco("tatu")
print(resposta)
booResposta=banco.atualizarFaseAtual(User("tatu",2))
print(booResposta)