import pygame
import math
from .config import CAMINHO_FONTE, TAMANHO_FONTE_TITULO, TAMANHO_FONTE_PADRAO, TAMANHO_FONTE_PEQUENA, LARGURA, ALTURA, COR_FUNDO
import os

class MenuVitoria:
    def __init__(self, usuario_username):
        self.username = usuario_username
        self.tempo_inicial = pygame.time.get_ticks()
        
        # Cores
        self.cor_texto_principal = (100, 255, 100)  # Verde
        self.cor_texto_secundario = (200, 200, 200)  # Cinza claro
        self.cor_fundo_painel = (20, 60, 20)  # Verde escuro
        
        # Fonte
        self.fonte_titulo = pygame.font.Font(CAMINHO_FONTE, TAMANHO_FONTE_TITULO)
        self.fonte_padrao = pygame.font.Font(CAMINHO_FONTE, TAMANHO_FONTE_PADRAO)
        self.fonte_pequena = pygame.font.Font(CAMINHO_FONTE, TAMANHO_FONTE_PEQUENA)
        
        # Mensagens sobre meio ambiente
        self.mensagens_ambiente = [
            "A reciclagem reduz a quantidade de lixo em aterros sanitários.",
            "Separar o lixo corretamente economiza recursos naturais e energia.",
            "Plástico leva mais de 400 anos para se decompor na natureza.",
            "O vidro pode ser reciclado infinitas vezes sem perder qualidade.",
            "Papel reciclado economiza 50% de água comparado ao papel novo.",
            "Metal reciclado reduz 95% da energia necessária para produzir novo.",
            "Este jogo te ensina sobre sustentabilidade de forma divertida!",
            "Cada pequeno ato de reciclagem faz diferença para o planeta."
        ]
        self.indice_mensagem = 0
        self.tempo_ultima_mudanca = pygame.time.get_ticks()
        
        # Carregar logo
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logo_path = os.path.join(base_dir, "assets", "logo.png")
        try:
            self.logo_original = pygame.image.load(logo_path).convert_alpha()
            # Redimensionar logo para caber na tela (reduzir para 25% do tamanho original)
            novo_tamanho = (int(self.logo_original.get_width() * 0.25), 
                           int(self.logo_original.get_height() * 0.25))
            self.logo = pygame.transform.scale(self.logo_original, novo_tamanho)
        except:
            self.logo = None
            print("Logo não encontrada")

    def desenhar(self, screen):
        """Desenha a tela de vitória com animações"""
        # Fundo
        screen.fill(COR_FUNDO)
        
        # Calcular tempo decorrido e animações
        tempo_decorrido = (pygame.time.get_ticks() - self.tempo_inicial) / 1000
        
        # Painel de fundo com semi-transparência
        painel = pygame.Surface((LARGURA - 60, 400))
        painel.fill(self.cor_fundo_painel)
        painel.set_alpha(200)
        screen.blit(painel, (30, ALTURA // 2 - 200))
        
        # Borda do painel
        pygame.draw.rect(screen, self.cor_texto_principal, (30, ALTURA // 2 - 200, LARGURA - 60, 400), 3)
        
        # Animação de estrelas piscantes no topo
        num_estrelas = 5
        for i in range(num_estrelas):
            angulo = (tempo_decorrido * 2 + i * (360 / num_estrelas)) * (math.pi / 180)
            raio = 80
            x = LARGURA // 2 + raio * math.cos(angulo)
            y = ALTURA // 2 - 180 + raio * math.sin(angulo)
            
            # Tamanho pulsante da estrela
            tamanho = 3 + 2 * math.sin(tempo_decorrido * 3 + i)
            pygame.draw.circle(screen, self.cor_texto_principal, (int(x), int(y)), max(1, int(tamanho)))
        
        # Logo com animação de escala
        if self.logo:
            escala_logo = 1.0 + 0.08 * math.sin(tempo_decorrido * 2)
            novo_tamanho = (int(self.logo.get_width() * escala_logo), 
                           int(self.logo.get_height() * escala_logo))
            logo_escalada = pygame.transform.scale(self.logo, novo_tamanho)
            
            logo_rect = logo_escalada.get_rect(center=(LARGURA // 2, ALTURA // 2 - 130))
            screen.blit(logo_escalada, logo_rect)
        
        # Mensagem principal
        mensagem = f"Parabéns, {self.username}!"
        mensagem_renderizada = self.fonte_padrao.render(mensagem, True, self.cor_texto_secundario)
        mensagem_rect = mensagem_renderizada.get_rect(center=(LARGURA // 2, ALTURA // 2 - 40))
        screen.blit(mensagem_renderizada, mensagem_rect)
        
        # Mensagem de conclusão
        conclusao = "Você salvou o planeta e concluiu a"
        conclusao_renderizada = self.fonte_padrao.render(conclusao, True, self.cor_texto_secundario)
        conclusao_rect = conclusao_renderizada.get_rect(center=(LARGURA // 2, ALTURA // 2 + 10))
        screen.blit(conclusao_renderizada, conclusao_rect)
        
        # Mensagem de conclusão linha 2
        conclusao2 = "Missão Sustentável!"
        conclusao2_renderizada = self.fonte_padrao.render(conclusao2, True, self.cor_texto_principal)
        conclusao2_rect = conclusao2_renderizada.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50))
        screen.blit(conclusao2_renderizada, conclusao2_rect)
        
        # Instrução com piscada
        if (int(tempo_decorrido * 2) % 2) == 0:  # Pisca a cada 0.5 segundos
            instrucao = "Pressione [ESC] para voltar ao menu"
            instrucao_renderizada = self.fonte_pequena.render(instrucao, True, self.cor_texto_principal)
            instrucao_rect = instrucao_renderizada.get_rect(center=(LARGURA // 2, ALTURA // 2 + 120))
            screen.blit(instrucao_renderizada, instrucao_rect)
        
        # Linha decorativa inferior
        pygame.draw.line(screen, self.cor_texto_principal, 
                        (50, ALTURA // 2 + 160), 
                        (LARGURA - 50, ALTURA // 2 + 160), 
                        2)
        
        # Atualizar mensagem a cada 4 segundos
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultima_mudanca > 4000:
            self.indice_mensagem = (self.indice_mensagem + 1) % len(self.mensagens_ambiente)
            self.tempo_ultima_mudanca = tempo_atual
        
        # Exibir mensagem sobre sustentabilidade
        mensagem_sustentavel = self.mensagens_ambiente[self.indice_mensagem]
        mensagem_sust_renderizada = self.fonte_pequena.render(mensagem_sustentavel, True, self.cor_texto_principal)
        mensagem_sust_rect = mensagem_sust_renderizada.get_rect(center=(LARGURA // 2, ALTURA - 40))
        screen.blit(mensagem_sust_renderizada, mensagem_sust_rect)
