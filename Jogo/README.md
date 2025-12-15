# 🌍 Missão Sustentável

Um jogo educativo interativo desenvolvido em Python com Pygame, focado em ensinar sobre **Objetivos de Desenvolvimento Sustentável (ODS)**, especificamente a **ODS 12: Consumo e Produção Responsável** e **ODS 13: Ação Climática**.

## 🎮 Sobre o Jogo

**Missão Sustentável** é um jogo casual onde o jogador assume o papel de um coletor de lixo responsável. O objetivo é coletar diferentes tipos de lixo espalhados pelo mapa e classificá-los corretamente em lixeiras específicas no Centro de Reciclagem.

O jogo progressivamente aumenta a dificuldade, introduzindo novos tipos de lixo a cada fase e, na fase final, o jogador enfrenta um desafio contra o tempo enquanto evita um obstáculo móvel.

### 🎯 Objetivos Educacionais

- Conscientizar sobre a importância da reciclagem
- Ensinar a classificação correta de resíduos
- Promover a responsabilidade ambiental
- Reforçar conceitos dos Objetivos de Desenvolvimento Sustentável

## 🌟 Características

✅ **4 Fases Progressivas** - Dificuldade crescente com novos tipos de lixo  
✅ **Sistema de Classificação** - Aprenda a separar lixo corretamente  
✅ **Desafio Contra o Tempo** - A fase final testa suas habilidades com urgência  
✅ **Inimigo Inteligente** - Na fase 4, um obstáculo persegue o jogador  
✅ **Interface Intuitiva** - Menu principal e telas de instruções claras  
✅ **Sistema de Progresso** - Complete fases para desbloquear conteúdo  
✅ **Feedback Visual** - Popups informativos durante o gameplay  

## 📋 Fases do Jogo

| Fase | Objetivo | Tipos de Lixo | Meta | Dificuldade | Inimigo |
|------|----------|---------------|------|-------------|---------|
| 1 | Coleta básica | Genérico | 5 itens | ⭐ Fácil | ❌ |
| 2 | Separação dupla | Orgânico, Plástico | 8 itens | ⭐⭐ Intermediário | ❌ |
| 3 | Separação múltipla | Papel, Vidro, Metal, Orgânico | 12 itens | ⭐⭐⭐ Difícil | ❌ |
| 4 | Desafio final | Todos (6 tipos) | 12 itens | ⭐⭐⭐⭐ Muito Difícil | ✅ |

## 🎮 Controles

### Movimentação
| Tecla | Ação |
|-------|------|
| **W** / **Seta ↑** | Mover para cima |
| **S** / **Seta ↓** | Mover para baixo |
| **A** / **Seta ←** | Mover para esquerda |
| **D** / **Seta →** | Mover para direita |

### Ações
| Tecla | Ação |
|-------|------|
| **ESPAÇO** | Pegar item (quando sobre o item) |
| **F** | Entrar no Centro de Reciclagem |
| **R** | Reiniciar fase |
| **ESC** | Voltar ao menu principal |

## 🚀 Instalação

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

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
python main.py
```

## 📦 Dependências

As dependências principais são:

- **pygame** (2.6.1+) - Motor gráfico do jogo
- **pygame-menu** (4.5.2+) - Sistema de menu
- **pyperclip** (1.11.0+) - Manipulação de área de transferência

Todas as dependências estão listadas em `dependencias.md` e `requirements.txt`.

## 📁 Estrutura do Projeto

```
Test-privado/
├── main.py                          # Ponto de entrada principal
├── Menu.py                          # Interface de menu
├── BancoManipulacao.py              # Gerenciamento de dados
├── PreCond.py                       # Pré-condições
├── usernameTela.py                  # Tela de nome de usuário
├── requirements.txt                 # Dependências Python
├── dependencias.md                  # Lista de dependências
│
├── MissaoSustentavel/
│   └── missao_sustentavel/
│       ├── __init__.py
│       ├── config.py                # Configurações (resolução, cores, etc)
│       ├── enums.py                 # Enumerações (tipos de lixo)
│       ├── entities.py              # Classes de entidades (Jogador, Item, Lixeira)
│       ├── game.py                  # Lógica principal do jogo
│       ├── level.py                 # Gerenciamento de fases
│       ├── menu_instrucoes.py       # Menu de instruções
│       ├── menu_fase_completa.py    # Tela de fase concluída
│       ├── menu_erro_lixeira.py     # Popup de erro de classificação
│       ├── popup_saco_cheio.py      # Popup de mochila cheia
│       ├── centro_interface.py      # Interface do centro de reciclagem
│       └── README.md                # Documentação técnica
│
├── Model/
│   └── users.py                     # Modelo de usuários
│
├── DataBase/
│   └── BD.json                      # Banco de dados (JSON)
│
├── assets/
│   └── cenario.png                  # Imagem de fundo do jogo
│
└── __pycache__/                     # Cache Python
```

## 🎨 Tipos de Lixo

O jogo trabalha com os seguintes tipos de lixo, cada um com uma cor específica de lixeira:

- 🟢 **Genérico** - Lixo comum
- 🟤 **Orgânico** - Resíduos naturais (cascas, folhas, etc)
- 🔵 **Plástico** - Materiais plásticos
- 🟡 **Papel** - Papéis e papelão
- ⚪ **Vidro** - Garrafas e vidros
- ⚙️ **Metal** - Latas e metais
- 🔴 **Perigoso** - Materiais perigosos (baterias, etc)

## 🛠️ Desenvolvimento

### Arquitetura

O projeto utiliza uma arquitetura orientada a objetos com as seguintes camadas:

- **Camada de Configuração** (`config.py`) - Constantes globais
- **Camada de Entidades** (`entities.py`) - Objetos do jogo
- **Camada de Lógica** (`game.py`, `level.py`) - Lógica principal
- **Camada de UI** (`menu_instrucoes.py`, etc) - Interface com usuário
- **Camada de Banco de Dados** (`Model/`, `DataBase/`) - Persistência de dados

### Padrões Utilizados

- **Dataclasses** - Para definição de entidades
- **Type Hints** - Para melhor legibilidade do código
- **Enums** - Para tipos de lixo
- **Singleton** - Configurações globais

## 📊 Estatísticas do Jogo

- **Total de Fases**: 4
- **Tipos de Lixo**: 7
- **Controles**: 9 principais
- **Velocidade do Jogador**: 3.5 tiles/frame
- **Velocidade do Inimigo**: 2.4 tiles/frame
- **Resolução**: 960x600 pixels
- **FPS**: 60

## 🎓 Conceitos ODS Abordados

### ODS 12 - Consumo e Produção Responsável
- Compreender a importância da reciclagem
- Aprender a separar resíduos corretamente
- Reconhecer diferentes tipos de materiais

### ODS 13 - Ação Climática
- Entender o impacto ambiental do lixo
- Promover ações sustentáveis
- Conscientizar sobre mudanças climáticas

## 🐛 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'pygame'"
**Solução**: Instale pygame com `pip install pygame`

### Problema: A imagem de fundo não aparece
**Solução**: Verifique se `assets/cenario.png` existe no diretório correto

### Problema: Jogo roda lentamente
**Solução**: Verifique suas especificações de hardware. O jogo requer Python 3.10+ e Pygame 2.6.1+

### Problema: Erro ao salvar dados
**Solução**: Verifique permissões de escrita na pasta `DataBase/`

## 👨‍💻 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é de código aberto e disponível sob a licença MIT.

## Equipe

Desenvolvido por Allyson Felix, Carlos Henrrique, Francisco Lailson, Francisco Danicel

## 🙏 Agradecimentos

Agradecimentos especiais a:
- Pygame Foundation pela excelente biblioteca gráfica
- Comunidade Python por ferramentas e suporte
- Todos os educadores e ativistas ambientais

