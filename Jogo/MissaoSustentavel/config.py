import os

LARGURA, ALTURA = 960, 600
FPS = 60
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # caminho da pasta onde este arquivo está
ASSETS_PATH = os.path.join(BASE_DIR, "..", "assets")   # sobe um nível e entra em 'assets'
CAMINHO_FONTE = os.path.join(ASSETS_PATH, "BoldPixels.ttf")
#CAMINHO_FONTE = os.path.join("assets", "BoldPixels.ttf")

TILE = 40
VELOCIDADE_JOGADOR = 3.5
VELOCIDADE_INIMIGO = 2.4

COR_FUNDO = (20, 26, 30)
COR_GRADE = (35, 45, 55)

NOME_FONTE = "BoldPixels"
TAMANHO_FONTE_PADRAO = 20
TAMANHO_FONTE_TITULO = 36
TAMANHO_FONTE_PEQUENA = 14

COR_ARVORE = (28, 100, 28)
COR_CHAO = (34, 139, 34)

COR_CAMINHO = COR_CHAO
COR_AGUA = (28, 120, 180)