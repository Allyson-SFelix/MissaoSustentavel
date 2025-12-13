import pygame
from typing import List
from .config import FPS, LARGURA, ALTURA, CAMINHO_FONTE, COR_FUNDO, TILE, COR_GRADE, NOME_FONTE, TAMANHO_FONTE_PADRAO, TAMANHO_FONTE_TITULO, TAMANHO_FONTE_PEQUENA
from .enums import TipoLixo
from .entities import Jogador
from .level import Nivel
from .centro_interface import CentroInterfaceUI
from .menu_fase_completa import MenuFaseCompleta
from .menu_erro_lixeira import MenuErroLixeira
from .menu_instrucoes import MenuInstrucoes
from .menu_vitoria import MenuVitoria
from .popup_saco_cheio import PopupSacoCheio

class Jogo:
    def __init__(self, usuario, fase_inicial=0):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Missão Sustentável")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(CAMINHO_FONTE, TAMANHO_FONTE_PADRAO)

        self.limites = pygame.Rect(0, 0, LARGURA, ALTURA)
        self.jogador = Jogador(pygame.Rect(60, 60, 28, 28))

        self.niveis: List[Nivel] = [
            # Fase 1: 1 lixeira geral, meta de 5 itens
            Nivel(1, [TipoLixo.GENERICO], meta_itens=5, inimigo=False),
            # Fase 2: 2 lixeiras (orgânicos e plásticos), meta de 4 itens de cada
            Nivel(2, [TipoLixo.ORGANICO, TipoLixo.PLASTICO], meta_itens=8, inimigo=False),
            # Fase 3: 4 lixeiras (plástico, vidro, orgânico, papel), meta de 3 itens de cada
            Nivel(3, [TipoLixo.PLASTICO, TipoLixo.VIDRO, TipoLixo.ORGANICO, TipoLixo.PAPEL], meta_itens=12, inimigo=False),
            # Fase 4: 6 lixeiras (plástico, vidro, orgânico, papel, metal, perigoso), meta de 2 itens de cada, com monstro
            Nivel(4, [TipoLixo.PLASTICO, TipoLixo.VIDRO, TipoLixo.ORGANICO, TipoLixo.PAPEL, TipoLixo.METAL, TipoLixo.PERIGOSO], meta_itens=12, inimigo=True),
        ]
        self.usuario = usuario
        self.atual = max(0, min(fase_inicial, len(self.niveis) - 1))
        self.estado = "jogando"
        self.interface_centro = None
        self.menu_fase_completa = None
        self.menu_erro_lixeira = None
        self.menu_instrucoes = None
        self.menu_vitoria = None
        self.popup_saco_cheio = None
        self.mostrar_icone_centro = False
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
        self.jogador.saco_lixo.clear()
        
        # Resetar variáveis de popup
        self.popup_saco_cheio = None
        self.mostrar_icone_centro = False
        
        # Criar menu de instruções apenas para a primeira fase
        if lvl.numero == 1:
            self.menu_instrucoes = MenuInstrucoes(lvl.numero)
            self.estado = "instrucoes"
        else:
            self.estado = "jogando"

    def desenhar_grade(self):
        for x in range(0, self.screen.get_width(), 40):
            pygame.draw.line(self.screen, COR_GRADE, (x,0), (x,self.screen.get_height()))
        for y in range(0, self.screen.get_height(), 40):
            pygame.draw.line(self.screen, COR_GRADE, (0,y), (self.screen.get_width(),y))

    def desenhar_hud(self):
        lvl = self.niveis[self.atual]
        text1 = f"Fase {lvl.numero} | Meta: {lvl.meta_itens} | Coletados: {lvl.coletados} | Saco de Lixo: {len(self.jogador.saco_lixo)}/{self.jogador.capacidade}"
        text2 = "Controles: [Espaço] Pegar  [R] Reiniciar  [Esc] Menu"

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

            # Eventos do popup de saco cheio
            if self.popup_saco_cheio:
                # O popup agora ignora qualquer entrada (não fecha com tecla)
                if self.popup_saco_cheio.tempo_expirou():
                    self.popup_saco_cheio = None

            # Eventos do menu de instruções
            if self.estado == "instrucoes" and self.menu_instrucoes:
                if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_instrucoes.pode_pular():
                        self.menu_instrucoes = None
                        self.estado = "jogando"

            # Eventos do menu de fase completa
            if self.estado == "fase_completa" and self.menu_fase_completa:
                if e.type == pygame.KEYDOWN:
                    acao = self.menu_fase_completa.processar_entrada_teclado(e.key)
                    if acao == "proxima":
                        self._avancar_fase()
                    elif acao == "menu_principal":
                        # Volta ao menu principal (NÃO fecha o jogo)
                        self.estado = "menu_principal"
                        self.menu_fase_completa = None
                    # Importante: NÃO dar return False aqui!

            # Eventos do menu de erro de lixeira
            if self.estado == "erro_lixeira" and self.menu_erro_lixeira:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self._confirmar_erro_lixeira()

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
                        self.estado = "erro_lixeira"
                        self.menu_erro_lixeira = MenuErroLixeira(tipo_lixo, tipo_lixeira_correta)
                    elif foi_depositado:
                        if 0 <= indice < len(self.jogador.saco_lixo):
                            del self.jogador.saco_lixo[indice]
                        self.interface_centro.atualizar_inventario(self.jogador.saco_lixo)

            if e.type == pygame.KEYDOWN:
                # Erro de lixeira
                if self.estado == "erro_lixeira" and self.menu_erro_lixeira:
                    if self.menu_erro_lixeira.processar_entrada(e.key):
                        self._confirmar_erro_lixeira()
                    continue

                if e.key == pygame.K_ESCAPE:

                    # Se estiver no menu principal, apenas ignore o ESC (não fecha o jogo)
                    if self.estado == "menu_principal":
                        continue

                    return False


                # Entrar ou sair do centro com F
                if e.key == pygame.K_f:
                    if self.estado == "jogando":
                        self._tentar_entrar_centro()
                    elif self.estado == "centro_aberto":
                        self._sair_centro()


                # Reiniciar fase
                if e.key == pygame.K_r:
                    if self.atual >= len(self.niveis):
                        self.atual = 0
                    self._carregar_nivel()
                    continue

                # Coletar item
                if self.estado == "jogando" and self.atual < len(self.niveis):
                    if e.key == pygame.K_SPACE:
                        lvl = self.niveis[self.atual]
                        item_coletado = self.jogador.tentar_coletar(lvl.itens)
                        if item_coletado:
                            lvl.itens.remove(item_coletado)

                # Confirmar saída do centro
                if e.key == pygame.K_RETURN and self.estado == "centro_aberto":
                    self._sair_centro()


        return True

    
    def _tentar_entrar_centro(self):
        """Tenta entrar no centro de reciclagem"""
        # Validar se tem itens no saco de lixo
        if len(self.jogador.saco_lixo) == 0:
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
        self.interface_centro.atualizar_inventario(self.jogador.saco_lixo)
    
    def _sair_centro(self):
        """Sai do centro de reciclagem e volta ao mapa"""
        if not self.interface_centro:
            return
        
        lvl = self.niveis[self.atual]
        
        # Conta os itens depositados
        total_depositado = self.interface_centro.obter_total_depositado()
        if total_depositado > 0:
            lvl.coletados += total_depositado
        
        # Verificar imediatamente se completou a fase ANTES de mudar estado
        if lvl.coletados >= lvl.meta_itens:
            # Se for a última fase, vai direto para vitória
            if self.atual == len(self.niveis) - 1:
                self.estado = "vitoria"
            else:
                self.estado = "fase_completa"
                self.menu_fase_completa = MenuFaseCompleta(lvl.numero)
        else:
            # Só volta ao estado "jogando" se NÃO completou a fase
            self.estado = "jogando"
        
        # Retorna o jogador à posição anterior
        if self.jogador.posicao_antes_centro:
            self.jogador.rect = self.jogador.posicao_antes_centro.copy()
        
        # Limpa a interface
        self.jogador.dentro_centro = None
        self.interface_centro.limpar()
        self.interface_centro = None
        
        # Afastar o inimigo novamente ao sair do centro (Fase 4)
        if lvl.inimigo and lvl.centros:
            self._afastar_inimigo_do_centro(lvl.centros[0], lvl)
    
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
        
        # Definir distância mínima desejada (aumentada)
        distancia_minima = 500
        
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
        # Se está exibindo instruções
        if self.estado == "instrucoes":
            if self.menu_instrucoes and self.menu_instrucoes.tempo_expirou():
                self.menu_instrucoes = None
                self.estado = "jogando"
            return
        
        # Fechar popup de saco cheio se expirou
        if self.popup_saco_cheio and self.popup_saco_cheio.tempo_expirou():
            self.popup_saco_cheio = None
        
        if self.estado == "centro_aberto" or self.estado == "erro_lixeira" or self.estado == "fase_completa":
            return

        if self.estado != "jogando":
            return

        keys = pygame.key.get_pressed()
        lvl = self.niveis[self.atual]
        self.jogador.mover(keys, self.limites, lvl)

        if lvl.atualizar_inimigo(self.jogador.rect, self.limites):
            self.estado = "game_over"

        # Verificar se o saco de lixo ficou cheio
        if len(self.jogador.saco_lixo) >= self.jogador.capacidade and not self.popup_saco_cheio:
            self.popup_saco_cheio = PopupSacoCheio()
            self.mostrar_icone_centro = True

        # Verificar se completou a fase
        if lvl.coletados >= lvl.meta_itens:
            self.estado = "fase_completa"
            self.menu_fase_completa = MenuFaseCompleta(lvl.numero)

    def desenhar(self):
        """Renderiza os gráficos do jogo"""
        self.screen.fill(COR_FUNDO)
        
        if self.estado == "instrucoes":
            # Desenhar o mapa de fundo + menu de instruções
            self.desenhar_grade()
            lvl = self.niveis[self.atual]
            lvl.desenhar(self.screen)
            self.jogador.desenhar(self.screen)
            
            # Desenhar o menu de instruções sobre o mapa
            if self.menu_instrucoes:
                self.menu_instrucoes.desenhar(self.screen)
        
        elif self.estado == "jogando":
            # Desenhar o nivel normal
            self.desenhar_grade()
            lvl = self.niveis[self.atual]
            lvl.desenhar(self.screen)
            self.jogador.desenhar(self.screen)

            self.desenhar_hud()
            
            # Desenhar ícone do centro se saco estiver cheio
            if self.mostrar_icone_centro and hasattr(lvl, 'centros') and lvl.centros:
                self._desenhar_icone_centro(lvl.centros[0])

            # Dicas quando próximo ao centro
            hint_y_offset = ALTURA - 80
            if hasattr(lvl, 'centros'):
                for c in lvl.centros:
                    if self.jogador.rect.colliderect(c.rect.inflate(16, 16)):
                        # Verificar se tem itens no saco de lixo
                        if len(self.jogador.saco_lixo) > 0:
                            hint_surface = self.font.render(
                                "Pressione [F] para entrar no Centro Reciclável",
                                True,
                                (0, 0, 0)
                            )
                        else:
                            hint_surface = self.font.render(
                                "Você precisa de itens no saco de lixo para entrar!",
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
            self._desenhar_texto("Você foi pego! Pressione R para tentar novamente ou ESC para ir pro menu.", (150, ALTURA//2))
        
        elif self.estado == "vitoria":
            # Criar menu de vitória na primeira vez
            if not self.menu_vitoria:
                self.menu_vitoria = MenuVitoria(self.usuario.username)
            
            # Desenhar a tela de vitória
            self.menu_vitoria.desenhar(self.screen)
        
        # Desenhar popup de saco cheio se houver
        if self.popup_saco_cheio:
            self.popup_saco_cheio.desenhar(self.screen)
        
        pygame.display.flip()
    
    def _desenhar_icone_centro(self, centro):
        """Desenha um ícone visual do centro de reciclagem no mapa"""
        # Animação pulsante do ícone
        tempo = pygame.time.get_ticks() / 500  # Pulsa a cada 500ms
        escala = 1.0 + 0.2 * abs(((tempo % 2) - 1))  # Varia entre 0.8 e 1.2
        
        # Calcular posição do ícone no topo do centro
        icon_x = centro.rect.centerx
        icon_y = centro.rect.top - 40
        
        # Desenhar círculo pulsante
        raio = int(15 * escala)
        pygame.draw.circle(self.screen, (100, 255, 100), (icon_x, icon_y), raio, 3)
        
        # Desenhar símbolo de reciclagem (triângulo)
        pontos = [
            (icon_x, icon_y - 8),
            (icon_x + 8, icon_y + 8),
            (icon_x - 8, icon_y + 8)
        ]
        pygame.draw.polygon(self.screen, (100, 255, 100), pontos, 2)
        
        # Desenhar texto "CENTRO"
        font_pequena = pygame.font.SysFont(NOME_FONTE, 16, bold=True)
        texto = font_pequena.render("CENTRO", True, (100, 255, 100))
        texto_rect = texto.get_rect(center=(icon_x, icon_y + 25))
        self.screen.blit(texto, texto_rect)

    def executar(self):
        rodando = True
        while rodando:
            self.clock.tick(FPS)
            if not self.processar_eventos():
                break

            # Atualiza sempre, pois o método já trata o estado internamente
            self.atualizar()

            self.desenhar()

def executar_jogo():
    Jogo(None).executar()
