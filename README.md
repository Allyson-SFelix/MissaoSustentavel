# Missão Sustentável

Um jogo educativo interativo desenvolvido em Python com Pygame, focado em ensinar sobre Objetivos de Desenvolvimento Sustentável (ODS), especificamente a ODS 12: Consumo e Produção Responsável.[1]

## Sobre o Jogo

Missão Sustentável é um jogo casual onde o jogador assume o papel de um coletor de lixo responsável. O objetivo é coletar diferentes tipos de lixo espalhados pelo mapa e classificá-los corretamente em lixeiras específicas no Centro de Reciclagem.[1]

O jogo progressivamente aumenta a dificuldade, introduzindo novos tipos de lixo a cada fase e, na fase final, o jogador enfrenta um desafio contra o tempo enquanto evita um obstáculo móvel.[1]

## Características

- 4 Fases Progressivas - Dificuldade crescente com novos tipos de lixo
- Sistema de Classificação - Aprenda a separar lixo corretamente
- Desafio Contra o Tempo - A fase final testa suas habilidades com urgência
- Inimigo Inteligente - Na fase 4, um obstáculo persegue o jogador
- Interface Intuitiva - Menu principal e telas de instruções claras
- Sistema de Progresso - Complete fases para desbloquear conteúdo
- Feedback Visual - Popups informativos durante o gameplay[1]

## Fases do Jogo

| Fase | Objetivo | Tipos de Lixo | Meta | Dificuldade | Inimigo |
|------|----------|---------------|------|-------------|---------|
| 1 | Coleta básica | Genérico | 5 itens | Fácil | Não |
| 2 | Separação dupla | Orgânico, Plástico | 8 itens | Intermediário | Não |
| 3 | Separação múltipla | Papel, Vidro, Metal, Orgânico | 12 itens | Difícil | Não |
| 4 | Desafio final | Todos (6 tipos) | 12 itens | Muito Difícil | Sim [1] |

## Controles

### Movimentação

| Tecla | Ação |
|-------|------|
| W / Seta ↑ | Mover para cima |
| S / Seta ↓ | Mover para baixo |
| A / Seta ← | Mover para esquerda |
| D / Seta → | Mover para direita [1] |

### Ações

| Tecla | Ação |
|-------|------|
| ESPAÇO | Pegar item (quando sobre o item) |
| F | Entrar no Centro de Reciclagem |
| R | Reiniciar fase |
| ESC | Voltar ao menu principal [1] |

## Instalação

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)[1]

### Passo 1: Clonar o repositório
```bash
git clone https://github.com/lailsonzw/Test-privado.git
cd Test-privado
```

### Passo 2: Criar ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### Passo 3: Instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Executar o jogo
```bash
python main.py [memory:1]
```

## Dependências

As dependências principais são:
- pygame (2.6.1+) - Motor gráfico do jogo
- pygame-menu (4.5.2+) - Sistema de menu
- pyperclip (1.11.0+) - Manipulação de área de transferência

Todas as dependências estão listadas em dependencias.md e requirements.txt.[1]

## Estrutura do Projeto

```
Test-privado/
├── main.py                  # Ponto de entrada principal
├── Menu.py                  # Interface de menu
├── BancoManipulacao.py      # Gerenciamento de dados
├── PreCond.py               # Pré-condições
├── usernameTela.py          # Tela de nome de usuário
├── requirements.txt         # Dependências Python
├── dependencias.md          # Lista de dependências
│
├── MissaoSustentavel/
│   └── missao_sustentavel/
│       ├── __init__.py
│       ├── config.py        # Configurações (resolução, cores, etc)
│       ├── enums.py         # Enumerações (tipos de lixo)
│       ├── entities.py      # Classes de entidades (Jogador, Item, Lixeira)
│       ├── game.py          # Lógica principal do jogo
│       ├── level.py         # Gerenciamento de fases
│       ├── menu_instrucoes.py # Menu de instruções
│       ├── menu_fase_completa.py # Tela de fase concluída
│       ├── menu_erro_lixeira.py # Popup de erro de classificação
│       ├── menu_vitoria.py    # Tela de vitória final
│       ├── popup_saco_cheio.py  # Popup de mochila cheia
│       ├── centro_interface.py  # Interface do centro de reciclagem
│       └── README.md        # Documentação técnica
│
├── Model/
│   └── users.py             # Modelo de usuários
│
├── DataBase/
│   └── BD.json              # Banco de dados (JSON)
│
├── assets/
│   └── cenario.png          # Imagem de fundo do jogo
│
└── __pycache__/             # Cache Python [memory:1]
```

## Tipos de Lixo

O jogo trabalha com os seguintes tipos de lixo, cada um com uma cor específica de lixeira:
- Genérico - Lixo comum
- Orgânico - Resíduos naturais (cascas, folhas, etc)
- Plástico - Materiais plásticos
- Papel - Papéis e papelão
- Vidro - Garrafas e vidros
- Metal - Latas e metais
- Perigoso - Materiais perigosos (baterias, etc)[1]

## Desenvolvimento

### Arquitetura

O projeto utiliza uma arquitetura orientada a objetos com as seguintes camadas:
- Camada de Configuração (config.py) - Constantes globais
- Camada de Entidades (entities.py) - Objetos do jogo
- Camada de Lógica (game.py, level.py) - Lógica principal
- Camada de UI (menu_instrucoes.py, etc) - Interface com usuário
- Camada de Banco de Dados (Model/, DataBase/) - Persistência de dados[1]

## Estatísticas do Jogo

- Total de Fases: 4
- Tipos de Lixo: 7
- Controles: 9 principais
- Velocidade do Jogador: 3.5 tiles/frame
- Velocidade do Inimigo: 2.4 tiles/frame
- Resolução: 960x600 pixels
- FPS: 60[1]

## Conceitos ODS Abordados

### ODS 12 - Consumo e Produção Responsável
- Compreender a importância da reciclagem
- Aprender a separar resíduos corretamente
- Reconhecer diferentes tipos de materiais[1]

### ODS 13 - Ação Climática
- Entender o impacto ambiental do lixo
- Promover ações sustentáveis
- Conscientizar sobre mudanças climáticas[1]

## Licença

Este projeto é de código aberto e disponível sob a licença MIT.[1]

## Equipe

Desenvolvido por Allyson Felix, Carlos Abrantes, Francisco Lailson, Francisco Daniel[1]