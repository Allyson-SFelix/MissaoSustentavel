import random
import pygame
from typing import List, Optional, Tuple
from .enums import TipoLixo, TIPO_NOMES, TIPO_IMAGENS, CORES_LIXEIRA
from .config import LARGURA, ALTURA, NOME_FONTE, COR_FUNDO, TILE


class ItemDragavel:
    """Representa um item no inventário que pode ser arrastado"""
    
    def __init__(self, tipo: TipoLixo, posicao: Tuple[int, int], indice: int):
        self.tipo = tipo
        self.rect = pygame.Rect(posicao[0], posicao[1], 50, 50)
        self.indice = indice
        self.sendo_arrastado = False
        self.offset_x = 0
        self.offset_y = 0
    
    def iniciar_arrasto(self, mouse_pos: Tuple[int, int]):
        """Inicia o arrasto do item"""
        if self.rect.collidepoint(mouse_pos):
            self.sendo_arrastado = True
            self.offset_x = mouse_pos[0] - self.rect.x
            self.offset_y = mouse_pos[1] - self.rect.y
            return True
        return False
    
    def atualizar_posicao(self, mouse_pos: Tuple[int, int]):
        """Atualiza a posição durante o arrasto"""
        if self.sendo_arrastado:
            self.rect.x = mouse_pos[0] - self.offset_x
            self.rect.y = mouse_pos[1] - self.offset_y
    
    def parar_arrasto(self):
        """Para o arrasto do item"""
        self.sendo_arrastado = False
    
    def desenhar(self, superficie: pygame.Surface):
        """Desenha o item"""
        try:
            imagem = TIPO_IMAGENS[self.tipo]
            imagem_redimensionada = pygame.transform.scale(imagem, (self.rect.w, self.rect.h))
            superficie.blit(imagem_redimensionada, self.rect)
        except:
            # Fallback se a imagem não carregar
            pygame.draw.rect(superficie, (200, 200, 200), self.rect, border_radius=5)
        
        # Desenhar borda se sendo arrastado
        if self.sendo_arrastado:
            pygame.draw.rect(superficie, (255, 255, 0), self.rect, 3, border_radius=5)
        else:
            pygame.draw.rect(superficie, (100, 100, 100), self.rect, 2, border_radius=5)


class LixeiraUI:
    """Representa uma lixeira na interface do centro"""
    
    def __init__(self, tipo: TipoLixo, posicao: Tuple[int, int]):
        self.tipo = tipo
        self.rect = pygame.Rect(posicao[0], posicao[1], 80, 100)
        self.itens_depositados = 0
        self.cor = CORES_LIXEIRA.get(tipo, (100, 100, 100))
    
    def verificar_colisao(self, item_rect: pygame.Rect) -> bool:
        """Verifica se um item está sobre a lixeira"""
        return self.rect.colliderect(item_rect)
    
    def aceitar_item(self, tipo_item: TipoLixo) -> bool:
        """Verifica se pode aceitar um item"""
        # Lixeira genérica aceita tudo, senão deve ser do mesmo tipo
        return self.tipo == TipoLixo.GENERICO or self.tipo == tipo_item
    
    def depositar_item(self) -> bool:
        """Deposita um item na lixeira"""
        self.itens_depositados += 1
        return True
    
    def desenhar(self, superficie: pygame.Surface):
        """Desenha a lixeira"""
        # Corpo da lixeira
        pygame.draw.rect(superficie, self.cor, self.rect, border_radius=8)
        
        # Interior (mais claro)
        interior = self.rect.inflate(-10, -10)
        pygame.draw.rect(superficie, (240, 240, 240), interior, border_radius=6)
        
        # Label (tipo da lixeira)
        fonte = pygame.font.SysFont(NOME_FONTE, 14, bold=True)
        nome_tipo = TIPO_NOMES.get(self.tipo, "Desconhecido")
        texto = fonte.render(nome_tipo, True, (30, 30, 30))
        texto_rect = texto.get_rect(center=(self.rect.centerx, self.rect.y + 15))
        superficie.blit(texto, texto_rect)
        
        # Contador de itens depositados
        fonte_pequena = pygame.font.SysFont(NOME_FONTE, 12)
        contador = fonte_pequena.render(f"x{self.itens_depositados}", True, (50, 50, 50))
        superficie.blit(contador, (self.rect.x + 10, self.rect.bottom - 25))


class CentroInterfaceUI:
    """Gerencia a tela do centro de reciclagem com drag & drop"""
    
    def __init__(self, tipos_lixeiras: List[TipoLixo]):
        self.tipos_lixeiras = tipos_lixeiras
        self.itens_inventario: List[ItemDragavel] = []
        self.lixeiras: List[LixeiraUI] = []
        self.item_sendo_arrastado: Optional[ItemDragavel] = None
        
        self._criar_layout()
    
    def _criar_layout(self):
        """Cria o layout visual do centro"""
        # Criando lixeiras (lado direito)
        inicio_lixeiras_x = LARGURA - 400
        inicio_lixeiras_y = 100
        
        espaco_entre = 120
        for i, tipo in enumerate(self.tipos_lixeiras):
            pos_x = inicio_lixeiras_x + (i % 2) * espaco_entre
            pos_y = inicio_lixeiras_y + (i // 2) * 140
            self.lixeiras.append(LixeiraUI(tipo, (pos_x, pos_y)))
    
    def atualizar_inventario(self, mochila: List[TipoLixo]):
        """Atualiza o inventário visual com base na mochila do jogador"""
        self.itens_inventario.clear()
        
        # Posicionamento do inventário (lado esquerdo)
        inicio_x = 50
        inicio_y = 100
        itens_por_linha = 4
        espaco = 70
        
        for i, tipo_lixo in enumerate(mochila):
            coluna = i % itens_por_linha
            linha = i // itens_por_linha
            
            pos_x = inicio_x + coluna * espaco
            pos_y = inicio_y + linha * espaco
            
            item = ItemDragavel(tipo_lixo, (pos_x, pos_y), i)
            self.itens_inventario.append(item)
    
    def processar_mouse_pressionado(self, mouse_pos: Tuple[int, int]):
        """Processa quando mouse é pressionado"""
        for item in self.itens_inventario:
            if item.iniciar_arrasto(mouse_pos):
                self.item_sendo_arrastado = item
                break
    
    def processar_mouse_movimento(self, mouse_pos: Tuple[int, int]):
        """Processa movimento do mouse"""
        if self.item_sendo_arrastado:
            self.item_sendo_arrastado.atualizar_posicao(mouse_pos)
    
    def processar_mouse_solto(self, mouse_pos: Tuple[int, int]):
        """
        Processa quando mouse é solto
        Retorna (foi_depositado, indice_item, houve_erro, tipo_lixo, tipo_lixeira_correta)
        """
        if not self.item_sendo_arrastado:
            return False, -1, False, None, None
        
        item_arrastado = self.item_sendo_arrastado
        foi_depositado = False
        houve_erro = False
        tipo_lixeira_correta = None
        
        # Verificar colisão com lixeiras
        for lixeira in self.lixeiras:
            if lixeira.verificar_colisao(item_arrastado.rect):
                # Verificar se a lixeira aceita este tipo de item
                if lixeira.aceitar_item(item_arrastado.tipo):
                    # Item correto!
                    lixeira.depositar_item()
                    foi_depositado = True
                    indice = item_arrastado.indice
                    self.item_sendo_arrastado.parar_arrasto()
                    self.item_sendo_arrastado = None
                    return foi_depositado, indice, False, None, None
                else:
                    # Item errado! Encontrar a lixeira correta
                    houve_erro = True
                    for lixeira_correta in self.lixeiras:
                        if lixeira_correta.aceitar_item(item_arrastado.tipo):
                            tipo_lixeira_correta = lixeira_correta.tipo
                            break
                    
                    # Se não encontrou, a resposta é genérica
                    if tipo_lixeira_correta is None:
                        tipo_lixeira_correta = lixeira.tipo
                    
                    indice = item_arrastado.indice
                    self.item_sendo_arrastado.parar_arrasto()
                    self.item_sendo_arrastado = None
                    return False, indice, houve_erro, item_arrastado.tipo, tipo_lixeira_correta
        
        # Se não foi depositado, parar arrasto e voltar posição
        self.item_sendo_arrastado.parar_arrasto()
        self.item_sendo_arrastado = None
        return False, -1, False, None, None
    
    def desenhar(self, superficie: pygame.Surface):
        """Desenha a interface do centro"""
        # Fundo
        superficie.fill(COR_FUNDO)
        
        # Títulos
        fonte_titulo = pygame.font.SysFont(NOME_FONTE, 24, bold=True)
        fonte_normal = pygame.font.SysFont(NOME_FONTE, 16)
        
        # Título inventário
        titulo_inv = fonte_titulo.render("📦 INVENTÁRIO", True, (100, 200, 100))
        superficie.blit(titulo_inv, (50, 20))
        
        # Título lixeiras
        titulo_lix = fonte_titulo.render("♻️ LIXEIRAS", True, (100, 200, 100))
        superficie.blit(titulo_lix, (LARGURA - 400, 20))
        
        # Instruções
        instrucoes = fonte_normal.render("Arraste os itens para as lixeiras corretas", True, (200, 200, 200))
        superficie.blit(instrucoes, (50, 70))
        
        # Desenhar lixeiras
        for lixeira in self.lixeiras:
            lixeira.desenhar(superficie)
        
        # Desenhar itens do inventário
        for item in self.itens_inventario:
            item.desenhar(superficie)
        
        # Informações na parte inferior
        info = fonte_normal.render("Pressione [ESC] para sair ou [ENTER] para confirmar", True, (150, 150, 150))
        superficie.blit(info, (50, ALTURA - 40))
        
        # Mostrar contagem total de itens depositados
        total_depositados = sum(l.itens_depositados for l in self.lixeiras)
        contador_total = fonte_normal.render(f"Total Depositado: {total_depositados}", True, (100, 200, 100))
        superficie.blit(contador_total, (LARGURA - 400, ALTURA - 40))
    
    def obter_total_depositado(self) -> int:
        """Retorna o total de itens depositados"""
        return sum(l.itens_depositados for l in self.lixeiras)
    
    def limpar(self):
        """Limpa a interface"""
        self.itens_inventario.clear()
        self.lixeiras.clear()
        self.item_sendo_arrastado = None
