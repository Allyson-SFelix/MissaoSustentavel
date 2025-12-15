# Missão Sustentável

Um jogo educativo interativo desenvolvido em Python com Pygame, focado em ensinar sobre Objetivos de Desenvolvimento Sustentável (ODS), especificamente a ODS 12: Consumo e Produção Responsável.

## Sobre o Jogo

Missão Sustentável é um jogo casual onde o jogador assume o papel de um coletor de lixo responsável. O objetivo é coletar diferentes tipos de lixo espalhados pelo mapa e classificá-los corretamente em lixeiras específicas no Centro de Reciclagem.

O jogo progressivamente aumenta a dificuldade, introduzindo novos tipos de lixo a cada fase e, na fase final, o jogador enfrenta um desafio contra o tempo enquanto evita um obstáculo móvel.

## Características

- 4 Fases Progressivas - Dificuldade crescente com novos tipos de lixo
- Sistema de Classificação - Aprenda a separar lixo corretamente
- Desafio Contra o Tempo - A fase final testa suas habilidades com urgência
- Inimigo Inteligente - Na fase 4, um obstáculo persegue o jogador
- Interface Intuitiva - Menu principal e telas de instruções claras
- Sistema de Progresso - Complete fases para desbloquear conteúdo
- Feedback Visual - Popups informativos durante o gameplay

## Controles

### Movimentação

| Tecla | Ação |
|-------|------|
| W / Seta ↑ | Mover para cima |
| S / Seta ↓ | Mover para baixo |
| A / Seta ← | Mover para esquerda |
| D / Seta → | Mover para direita |

### Ações

| Tecla | Ação |
|-------|------|
| ESPAÇO | Pegar item (quando sobre o item) |
| F | Entrar no Centro de Reciclagem |
| R | Reiniciar fase |
| ESC | Voltar ao menu principal |

## Instalação

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Clonar o repositório
```bash
git clone https://github.com/Allyson-SFelix/MissaoSustentavel
cd MissaoSustentavel
```
```

### Passo 2: Instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Executar o jogo
```bash
cd Jogo
python main.py
```

## Dependências

As dependências principais são:
- pygame (2.6.1+) - Motor gráfico do jogo
- pygame-menu (4.5.2+) - Sistema de menu
- pyperclip (1.11.0+) - Manipulação de área de transferência

Todas as dependências estão listadas em dependencias.md e requirements.txt.

## Tipos de Lixo

O jogo trabalha com os seguintes tipos de lixo, cada um com uma cor específica de lixeira:
- Genérico - Lixo comum
- Orgânico - Resíduos naturais (cascas, folhas, etc)
- Plástico - Materiais plásticos
- Papel - Papéis e papelão
- Vidro - Garrafas e vidros
- Metal - Latas e metais
- Perigoso - Materiais perigosos (baterias, etc)

## Desenvolvimento

### Arquitetura

O projeto utiliza uma arquitetura orientada a objetos com as seguintes camadas:
- Camada de Configuração (config.py) - Constantes globais
- Camada de Entidades (entities.py) - Objetos do jogo
- Camada de Lógica (game.py, level.py) - Lógica principal
- Camada de UI (menu_instrucoes.py, etc) - Interface com usuário
- Camada de Banco de Dados (Model/, DataBase/) - Persistência de dados

## Estatísticas do Jogo

- Total de Fases: 4
- Tipos de Lixo: 7
- Controles: 9 principais
- Velocidade do Jogador: 3.5 tiles/frame
- Velocidade do Inimigo: 2.4 tiles/frame
- Resolução: 960x600 pixels
- FPS: 60

## Conceitos ODS Abordados

### ODS 12 - Consumo e Produção Responsável
- Compreender a importância da reciclagem
- Aprender a separar resíduos corretamente
- Reconhecer diferentes tipos de materiais

### ODS 13 - Ação Climática
- Entender o impacto ambiental do lixo
- Promover ações sustentáveis
- Conscientizar sobre mudanças climáticas

## Licença

Este projeto é de código aberto e disponível sob a licença MIT.

## Equipe

Desenvolvido por Allyson Felix, Carlos Abrantes, Francisco Lailson, Francisco Daniel.