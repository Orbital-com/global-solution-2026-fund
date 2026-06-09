# Análise de Rotas e Risco de Seca em Municípios (Global Solution 2026)

**Turma:** 2ESPG

**Integrantes:**
| Nome | RM |
|---|---|
João Pedro Marcilio | 561603 |
Lucas Zanella Clemente | 563880 |
Daniel Oliveira de Souza | 566284 |
Pedro Henrique Silva Gregolini | 563342 |
Mateus Amaral Franze | 562334 |

## 💼 Sobre o Projeto

Este projeto foi desenvolvido como parte da Global Solution 2026, com foco na análise e otimização de rotas logísticas entre municípios em diferentes cenários:

### Cenário A - Rede de resposta a enchentes no Rio Grande do Sul
Grafo baseado nos 478 municípios afetados pelas enchentes do RS em 2024. Vértices
= municípios; arestas = rodovias com tempo de deslocamento como peso. Objetivo:
encontrar a MST de cobertura mínima para posicionar equipes de resposta, e o caminho
mais curto de Porto Alegre a cada município afetado.

### Cenário B - Triagem de risco de seca no MATOPIBA
Grafo de municípios da região MATOPIBA (MA, TO, PI, BA) com índice de risco derivado
de NDVI e precipitação INMET. BST organiza os municípios por grau de criticidade.
Algoritmo Guloso determina a ordem ótima de atendimento dado um orçamento máximo
de deslocamento.

## 📁 Estrutura do Repositório
```
global-solution-2026-fund/
│
├── data/
│   ├── processed/         # Grafos e árvores serializados (arquivos JSON)
│   │   ├── ...
│   ├── raw/               # Dados brutos, como índices NDVI, pluviometria INMET e malha viária (em JSON)
│   │   ├── ...
│
├── notebooks/
│   ├── analise_resultados.ipynb   # Análise e resolução dos cenários, avaliação do gap de otimalidade e justificativa da escala de decisão
│
├── report/
│   ├── relatorio_final.pdf   # Relatório técnico final (4 páginas)
│
├── src/
│   ├── brute_force.py               # Lógica de roteamento baseada em enumeração completa (baseline de validação)
│   ├── data_structures.py           # Implementação das estruturas base (Lista, Tupla, Dict, Heap, Árvore Binária de Busca, Grafo)
│   ├── greedy.py                    # Lógica gulosa, contendo a solução eficiente escolhida para o cenário
│   ├── performance_monitor.py       # Encapsula a medição de tempo, memória e contagem de operações elementares
│   ├── visualizations.py            # Funções responsáveis pela plotagem geoespacial de grafos, representação da BST e gráficos comparativos de benchmark
│
├── tests/
│   ├── test_algorithms.py            # Testes unitários automatizados utilizando pytest
│
├── readme.md            # Descrição, instruções e identificação do grupo
├── requirements.txt     # Dependências Python necessárias para execução do projeto
```

## 🛠️ Como Executar

**Pré-requisitos**
É necessário possuir o Python 3.10 instalado.

**Instalação**
1. Abra seu terminal e acesse o diretório raiz do projeto.
2. (Recomendado) Crie e ative seu ambiente virtual: `python -m venv .venv` e `source .venv/bin/activate` (pode mudar conforme o sistema operacional ou shell)
3. Instale as dependências com o comando: `pip install -r requirements.txt`

**Análise**
A melhor forma de visualizar o comportamento dos algoritmos de perto é rodando as análises estruturadas interativas.
1. Navegue até o diretório `notebooks/` e abra o `analise_resultados.ipynb`.
2. Execute as células em sequência para acompanhar os outputs, o cruzamento das curvas de desempenho e a geração automática dos mapas logísticos.

**Executando os Testes**
Para garantir o funcionamento correto de todas as estruturas e buscas, execute os testes unitários a partir da raiz do projeto:
`pytest tests/test_algorithms.py`
