# Plano de Especificação Formal

## 1. Introdução  
O plano de especificação formal refere-se ao software de jogo interativo baseado em fases, com temática de reciclagem de itens em coletas adequadas.  
Dessa forma, é possível aplicar a notação formal (Z) para representar de forma rigorosa os requisitos funcionais e os requisitos não-funcionais levantados, de modo a garantir clareza, consistência e verificabilidade.  

## 2. Objetivos da Especificação  
Com o desenvolvimento da especificação em notação Z, será possível:  
- Garantir que os requisitos funcionais (**RF01 – RF09**) e os requisitos não-funcionais (**RNF01 – RNF03**) estejam representados formalmente.  
- Evitar ambiguidades na definição de regras de negócio.  
- Permitir a verificação da consistência do sistema por meio da notação Z.  
- Apoiar o processo de testes de software, fornecendo uma base formal para criação de casos de teste.  

## 3. Escopo  
O sistema a ser especificado é um **jogo baseado em fases**, que consiste na coleta de lixo necessária para a transição entre fases progressivas, cada uma com metas definidas.  

- Na **fase 4**, há um *boss* e ocorre reinício da fase em caso de falha.  
- Registro de progresso do usuário (última fase alcançada), permitindo retorno ao pressionar **“Carregar jogo”** no menu.  
- A especificação formal será restrita às operações principais relacionadas ao **controle de fases e metas**.  
