import pygame
from typing import List
from .config import LARGURA, ALTURA, FPS, COR_FUNDO, COR_GRADE, NOME_FONTE, TILE
from .enums import TipoLixo
from .entities import Jogador
from .level import Nivel
from .centro_interface import CentroInterfaceUI
from .menu_fase_completa import MenuFaseCompleta
from .menu_erro_lixeira import MenuErroLixeira
class Jogo:
    def __init__(self,usuario):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Missão Sustentável")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(NOME_FONTE, 18)

        self.limites = pygame.Rect(0,0,LARGURA,ALTURA)
        self.jogador = Jogador(pygame.Rect(60,60,28,28))

        self.niveis: List[Nivel] = [
            Nivel(1, [TipoLixo.GENERICO], meta_itens=5, inimigo=False),
            Nivel(2, [TipoLixo.ORGANICO, TipoLixo.PLASTICO], meta_itens=8, inimigo=False),
            Nivel(3, [TipoLixo.PAPEL, TipoLixo.VIDRO, TipoLixo.METAL], meta_itens=10, inimigo=False),
            Nivel(4, [TipoLixo.ORGANICO, TipoLixo.PLASTICO, TipoLixo.PAPEL, TipoLixo.VIDRO], meta_itens=12, inimigo=True),
        ]
        self.usuario=usuario
        self.atual = 0
        self.estado = "jogando"
        self._carregar_nivel()

    def _carregar_nivel(self):
        lvl = self.niveis[self.atual]
        lvl.spawn()

        lvl.coletados = 0

        start_col = 1
        start_row = lvl.map_rows // 2
        found = lvl.encontrar_celula_caminho_proxima(start_col, start_row)
        if found:
            bx, by = found

            px = bx * TILE + TILE // 2
            py = by * TILE + TILE // 2
            player_rect = self.jogador.rect.copy()
            player_rect.center = (px, py)
            if hasattr(lvl, 'centros'):
                blocked = any(c.rect.colliderect(player_rect) for c in lvl.centros)
            else:
                blocked = False
            if not blocked:
                self.jogador.rect.center = (px, py)
            else:

                safe_found = None
                for r in range(1, 6):
                    for dy in range(-r, r + 1):
                        for dx in range(-r, r + 1):
                            nx = bx + dx
                            ny = by + dy
                            if 0 <= nx < lvl.map_cols and 0 <= ny < lvl.map_rows and lvl.bg_map[ny][nx] != 2:
                                candx = nx * TILE + TILE // 2
                                candy = ny * TILE + TILE // 2
                                crect = self.jogador.rect.copy()
                                crect.center = (candx, candy)
                                if hasattr(lvl, 'centros') and any(c.rect.colliderect(crect) for c in lvl.centros):
                                    continue
                                safe_found = (candx, candy)
                                break
                        if safe_found:
                            break
                    if safe_found:
                        break
                if safe_found:
                    self.jogador.rect.center = safe_found
                else:

                    self.jogador.rect.topleft = (60, 60)
        else:
            self.jogador.rect.topleft = (60, 60)
        self.jogador.mochila.clear()
        self.estado = "jogando"

    def desenhar_grade(self):
        for x in range(0, self.screen.get_width(), 40):
            pygame.draw.line(self.screen, COR_GRADE, (x,0), (x,self.screen.get_height()))
            
        for y in range(0, self.screen.get_height(), 40):
            pygame.draw.line(self.screen, COR_GRADE, (0,y), (self.screen.get_width(),y))

    def desenhar_hud(self):
        lvl = self.niveis[self.atual]
        text1 = f"Fase {lvl.numero} | Meta: {lvl.meta_itens} | Coletados: {lvl.coletados} | Mochila: {len(self.jogador.mochila)}/{self.jogador.capacidade}"
        text2 = "Controles: [E] Pegar  [Q] Descartar  [R] Reiniciar  [Esc] Sair"

        text1_surface = self.font.render(text1, True, (0, 0, 0))
        text2_surface = self.font.render(text2, True, (0, 0, 0))

        margin = 10
        bottom_y = ALTURA - margin

        self.screen.blit(text2_surface, (margin, bottom_y - text2_surface.get_height()))

        self.screen.blit(text1_surface, (margin, bottom_y - text2_surface.get_height() - text1_surface.get_height() - 4))

    def _desenhar_texto(self, s, pos):
        surf = self.font.render(s, True, (235, 235, 235))
        self.screen.blit(surf, pos)

    def processar_eventos(self):
        """Processa eventos do teclado e mouse"""
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            
            # Eventos do menu de erro de lixeira
            if self.estado == "erro_lixeira" and self.menu_erro_lixeira:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self._confirmar_erro_lixeira()
            
            # Eventos do menu de conclusão de fase
            if self.estado == "fase_completa" and self.menu_fase_completa:
                if e.type == pygame.MOUSEMOTION:
                    self.menu_fase_completa.atualizar_mouse_hover(e.pos)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    resultado = self.menu_fase_completa.processar_clique_mouse(e.pos)
                    if resultado == "continuar":
                        self._avancar_fase()
                    elif resultado == "sair":
                        return False
            
            # Eventos do mouse para o centro de reciclagem
            if self.estado == "centro_aberto" and self.interface_centro:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.interface_centro.processar_mouse_pressionado(e.pos)
                elif e.type == pygame.MOUSEMOTION:
                    self.interface_centro.processar_mouse_movimento(e.pos)
                elif e.type == pygame.MOUSEBUTTONUP:
                    resultado = self.interface_centro.processar_mouse_solto(e.pos)
                    foi_depositado, indice, houve_erro, tipo_lixo, tipo_lixeira_correta = resultado
                    
                    if houve_erro:
                        # Erro! Mostrar menu de erro
                        self.estado = "erro_lixeira"
                        self.menu_erro_lixeira = MenuErroLixeira(tipo_lixo, tipo_lixeira_correta)
                    elif foi_depositado:
                        # Sucesso! Remove o item da mochila do jogador
                        if 0 <= indice < len(self.jogador.mochila):
                            del self.jogador.mochila[indice]
                        # Atualiza interface
                        self.interface_centro.atualizar_inventario(self.jogador.mochila)
            
            if e.type == pygame.KEYDOWN:
                # Menu de erro de lixeira
                if self.estado == "erro_lixeira" and self.menu_erro_lixeira:
                    if self.menu_erro_lixeira.processar_entrada(e.key):
                        self._confirmar_erro_lixeira()
                    continue
                
                # Menu de conclusão de fase
                if self.estado == "fase_completa" and self.menu_fase_completa:
                    resultado = self.menu_fase_completa.processar_entrada_teclado(e.key)
                    if resultado == "continuar":
                        self._avancar_fase()
                    elif resultado == "sair":
                        return False
                    continue
                
                # Sair do jogo ou do centro
                if e.key == pygame.K_ESCAPE:
                    if self.estado == "centro_aberto":
                        # Sair do centro
                        self._sair_centro()
                    else:
                        return False
                
                # Entrar no centro (somente modo jogando)
                if e.key == pygame.K_f and self.estado == "jogando":
                    self._tentar_entrar_centro()
                
                # Reiniciar fase
                if e.key == pygame.K_r:
                    if self.atual >= len(self.niveis):
                        self.atual = 0
                    self._carregar_nivel()
                    continue
                
                # Controles de coleta (somente quando jogando)
                if self.estado == "jogando" and self.atual < len(self.niveis):
                    if e.key == pygame.K_e:
                        # Coletar item
                        lvl = self.niveis[self.atual]
                        item_coletado = self.jogador.tentar_coletar(lvl.itens)
                        if item_coletado:
                            lvl.itens.remove(item_coletado)
                    
                    if e.key == pygame.K_q:
                        # Descartar na lixeira (modo antigo, mantido para compatibilidade)
                        lvl = self.niveis[self.atual]
                        depositado = self.jogador.tentar_depositar(lvl.lixeiras)
                        if depositado:
                            lvl.coletados += depositado
                
                # Confirmar saída do centro com ENTER
                if e.key == pygame.K_RETURN and self.estado == "centro_aberto":
                    self._sair_centro()
        
        return True
    
    def _tentar_entrar_centro(self):
        """Tenta entrar no centro de reciclagem"""
        # Validar se tem itens na mochila
        if len(self.jogador.mochila) == 0:
            # Não tem itens, não pode entrar
            return
        
        lvl = self.niveis[self.atual]
        
        if not hasattr(lvl, 'centros') or not lvl.centros:
            return
        
        # Procura o centro mais próximo
        centro_encontrado = None
        for centro in lvl.centros:
            if self.jogador.rect.colliderect(centro.rect.inflate(24, 16)):
                centro_encontrado = centro
                break
        
        if not centro_encontrado:
            return
        
        # Entra no centro
        self.estado = "centro_aberto"
        self.jogador.dentro_centro = centro_encontrado
        self.jogador.posicao_antes_centro = self.jogador.rect.copy()
        
        # Afastar o inimigo (na fase 4) para longe do centro
        if lvl.inimigo:
            self._afastar_inimigo_do_centro(centro_encontrado, lvl)
        
        # Cria a interface do centro
        tipos_lixeiras = centro_encontrado.lixeiras
        self.interface_centro = CentroInterfaceUI([l.tipo for l in tipos_lixeiras])
        self.interface_centro.atualizar_inventario(self.jogador.mochila)
    
    def _sair_centro(self):
        """Sai do centro de reciclagem e volta ao mapa"""
        if not self.interface_centro:
            return
        
        lvl = self.niveis[self.atual]
        
        # Conta os itens depositados
        total_depositado = self.interface_centro.obter_total_depositado()
        if total_depositado > 0:
            lvl.coletados += total_depositado
        
        # Retorna o jogador à posição anterior
        if self.jogador.posicao_antes_centro:
            self.jogador.rect = self.jogador.posicao_antes_centro.copy()
        
        # Limpa o estado
        self.estado = "jogando"
        self.jogador.dentro_centro = None
        self.interface_centro.limpar()
        self.interface_centro = None
    
    def _avancar_fase(self):
        """Avança para a próxima fase"""
        self.atual += 1
        
        # Fechar menu de conclusão
        self.menu_fase_completa = None
        
        if self.atual >= len(self.niveis):
            # Todas as fases concluídas
            self.estado = "vitoria"
        else:
            # Carregar próxima fase
            self._carregar_nivel()

    def _confirmar_erro_lixeira(self):
        """Confirma o erro e reinicia a fase"""
        # Fechar menu de erro
        self.menu_erro_lixeira = None
        
        # Sair do centro
        self.estado = "centro_aberto"
        self.interface_centro = None
        self.jogador.dentro_centro = None
        
        # Reiniciar a fase completamente
        self._carregar_nivel()
    
    def _afastar_inimigo_do_centro(self, centro, nivel):
        """Afasta o inimigo para longe do centro quando jogador entra"""
        if not nivel.inimigo:
            return
        
        import math
        
        # Definir distância mínima desejada
        distancia_minima = 300
        
        # Calcular direção oposta do centro
        dx = nivel.inimigo.rect.centerx - centro.rect.centerx
        dy = nivel.inimigo.rect.centery - centro.rect.centery
        
        # Se o inimigo já está longe, não faz nada
        distancia = math.hypot(dx, dy)
        if distancia >= distancia_minima:
            return
        
        # Normalizar a direção
        if distancia > 0:
            dx = dx / distancia
            dy = dy / distancia
        else:
            # Se está no mesmo lugar, afastar para canto aleatório
            dx = 1
            dy = 0
        
        # Mover inimigo para distância mínima
        novo_x = centro.rect.centerx + dx * distancia_minima
        novo_y = centro.rect.centery + dy * distancia_minima
        
        # Clampar dentro dos limites do mapa
        novo_x = max(50, min(novo_x, LARGURA - 50))
        novo_y = max(50, min(novo_y, ALTURA - 50))
        
        # Atualizar posição do inimigo
        nivel.inimigo.rect.center = (novo_x, novo_y)

    def atualizar(self):
        """Atualiza a lógica do jogo"""
        # No modo centro aberto ou em erro, não atualizar o mapa
        if self.estado == "centro_aberto" or self.estado == "erro_lixeira":
            return
        
        # No menu de conclusão de fase, não atualizar
        if self.estado == "fase_completa":
            return
        
        # Atualizar modo jogando normal
        if self.estado != "jogando":
            return
        
        keys = pygame.key.get_pressed()
        lvl = self.niveis[self.atual]
        self.jogador.mover(keys, self.limites, lvl)

        if lvl.atualizar_inimigo(self.jogador.rect, self.limites):
            self.estado = "game_over"

        # Verificar se completou a fase
        if lvl.coletados >= lvl.meta_itens:
            self.estado = "fase_completa"
            # Criar menu de conclusão
            self.menu_fase_completa = MenuFaseCompleta(lvl.numero)

    def desenhar(self):
        """Renderiza os gráficos do jogo"""
        self.screen.fill(COR_FUNDO)
        
        if self.estado == "jogando":
            # Desenhar o nivel normal
            self.desenhar_grade()
            lvl = self.niveis[self.atual]
            lvl.desenhar(self.screen)
            self.jogador.desenhar(self.screen)

            self.desenhar_hud()

            # Dicas quando próximo ao centro
            hint_y_offset = ALTURA - 80
            if hasattr(lvl, 'centros'):
                for c in lvl.centros:
                    if self.jogador.rect.colliderect(c.rect.inflate(16, 16)):
                        # Verificar se tem itens na mochila
                        if len(self.jogador.mochila) > 0:
                            hint_surface = self.font.render(
                                "Pressione [F] para entrar no Centro Reciclável",
                                True,
                                (0, 0, 0)
                            )
                        else:
                            hint_surface = self.font.render(
                                "Você precisa de itens na mochila para entrar!",
                                True,
                                (255, 100, 100)
                            )
                        self.screen.blit(hint_surface, (10, hint_y_offset))
                        break

        elif self.estado == "centro_aberto":
            # Desenhar a interface do centro
            if self.interface_centro:
                self.interface_centro.desenhar(self.screen)
        
        elif self.estado == "erro_lixeira":
            # Desenhar a interface do centro de fundo + menu de erro
            if self.interface_centro:
                self.interface_centro.desenhar(self.screen)
            
            if self.menu_erro_lixeira:
                self.menu_erro_lixeira.desenhar(self.screen)
        
        elif self.estado == "fase_completa":
            # Desenhar o mapa de fundo + menu de conclusão
            self.desenhar_grade()
            lvl = self.niveis[self.atual]
            lvl.desenhar(self.screen)
            self.jogador.desenhar(self.screen)
            
            # Desenhar o menu sobre o mapa
            if self.menu_fase_completa:
                self.menu_fase_completa.desenhar(self.screen)

        elif self.estado == "game_over":
            self._desenhar_texto("Você foi pego! Pressione R para tentar novamente ou ESC para sair.", (140, ALTURA//2))
        
        elif self.estado == "vitoria":
            self._desenhar_texto("Parabéns! Você concluiu a Missão Sustentável! (ESC para sair)", (200, ALTURA//2))

        pygame.display.flip()

    def executar(self):
        rodando = True
        while rodando:
            self.clock.tick(FPS)
            if not self.processar_eventos():
                break
            if self.estado == "jogando":
                self.atualizar()
            self.desenhar()

def executar_jogo():
    Jogo(None).executar()