# Projeto: Calculadora de Custos para Bolos de Pote

## Objetivo
Criar uma aplicação simples em Python que permita:

- Cadastrar receitas (com ingredientes e quantidades).
- Cadastrar/preencher preços de ingredientes separadamente.
- Calcular o custo total da receita com base nos preços mais recentes.
- Estimar custo unitário por bolo de pote.
- Incluir custos adicionais (embalagem, colher, etc).
- Definir encargos, custo de mão de obra e lucro desejado.
- Obter automaticamente preço de venda sugerido, margem de lucro e relatório geral.

---

## Estrutura Base dos Dados

### 1. Receitas
Cada receita contém:

- Nome da receita
- Por quantos bolos de pote ela rende
- Lista de ingredientes: nome, quantidade, unidade (ex: g, ml, lata, colher...)

#### Exemplo (JSON):
```json
{
  "nome": "Prestígio",
  "rendimento_bolos": 21,
  "ingredientes": [
    {"nome": "leite condensado", "quantidade": 2, "unidade": "lata"},
    {"nome": "coco ralado", "quantidade": 150, "unidade": "g"},
    {"nome": "chocolate meio amargo", "quantidade": 200, "unidade": "g"}
  ]
}
```

### 2. Tabela de Preços de Ingredientes
Arquivo separado com:

- Nome do ingrediente
- Preço total da embalagem
- Quantidade da embalagem
- Unidade da embalagem

#### Exemplo (JSON):
```json
{
  "leite condensado": {"preco": 5.99, "quantidade": 395, "unidade": "g"},
  "coco ralado": {"preco": 7.50, "quantidade": 100, "unidade": "g"},
  "chocolate meio amargo": {"preco": 12.00, "quantidade": 200, "unidade": "g"}
}
```

### 3. Custos Adicionais
Permitir adicionar:

- Preço total pago nas embalagens + quantidade de embalagens + tamanho
- Preço total pago nas colheres + quantidade + tamanho
- Outras despesas fixas ou variáveis (ex: gás, energia, delivery...)
- Custo estimado de mão de obra (fixo ou percentual sobre custo dos ingredientes)
- Lucro desejado (percentual sobre custo final)

---

## Cálculos Automáticos

Para cada receita:

- Comparar ingredientes da receita com a tabela de preços.
- Calcular custo proporcional de cada ingrediente.
- Somar custos adicionais.
- Adicionar mão de obra.
- Calcular valor de venda com base no lucro desejado.

Exibir:

- Custo total da receita
- Custo por bolo
- Preço sugerido de venda por bolo
- Lucro estimado por unidade


---

## Interface de Uso (Simples)

### Menu principal (exemplo):
```
=== CALCULADORA DE BOLINHOS ===

1. Cadastrar nova receita
2. Atualizar preços de ingredientes
3. Calcular custo de uma receita
4. Configurar custos adicionais e lucro
5. Gerar relatório
6. Sair
```

---

# Exemplos de Uso no Terminal

Este projeto utiliza uma interface de linha de comando (CLI) para gerenciar receitas de bolos de pote, calcular custos e gerar relatórios. Abaixo,
exemplos ilustrativos de como a aplicação se comporta em cada etapa:

## Cadastrar Nova Receita

O usuário informa os dados da nova receita:
```
Digite o nome da receita: Prestígio
Quantos bolos essa receita rende? 21
Quantos ingredientes tem essa receita? 3

Ingrediente 1:
Nome: leite condensado
Quantidade: 2
Unidade: lata

Ingrediente 2:
Nome: coco ralado
Quantidade: 150
Unidade: g

Ingrediente 3:
Nome: chocolate meio amargo
Quantidade: 200
Unidade: g

Receita cadastrada com sucesso!

╔════════════════╦══════════════════════╦════════════════════════════════════╗
║ Receita        ║ Rendimento (bolos)   ║ Ingredientes                       ║
╠════════════════╬══════════════════════╬════════════════════════════════════╣
║ Prestígio      ║ 21                   ║ leite condensado (2 lata)          ║
║                ║                      ║ coco ralado (150 g)                ║
║                ║                      ║ chocolate meio amargo (200 g)      ║
╚════════════════╩══════════════════════╩════════════════════════════════════╝

```
## Atualizar Preços de Ingredientes

O sistema carrega os ingredientes salvos e permite atualizar preço, unidade e quantidade:

```
╔════╦════════════════════════════╦══════════════════════════╦══════════════════════╦═════════╗
║ Nº ║ Ingrediente                ║ Preço embalagem (R$)     ║ Quantidade embalagem ║ Unidade ║
╠════╬════════════════════════════╬══════════════════════════╬══════════════════════╬═════════╣
║ 1  ║ leite condensado           ║ 5,99                     ║ 395                  ║ g       ║
║ 2  ║ coco ralado                ║ 7,50                     ║ 100                  ║ g       ║
║ 3  ║ chocolate meio amargo      ║ 12,00                    ║ 200                  ║ g       ║
╚════╩════════════════════════════╩══════════════════════════╩══════════════════════╩═════════╝


```
Ao atualizar:
```
Digite o número do ingrediente que deseja atualizar (ou 0 para sair): 1

Ingrediente: leite condensado
Preço atual: R$ 5,99
Novo preço (enter para manter): 6,20
Quantidade atual: 395
Nova quantidade (enter para manter):
Unidade atual: g
Nova unidade (enter para manter):

Ingrediente atualizado!

```

## Calcular Custo de uma Receita

Selecionada a receita, a aplicação gera um relatório detalhado:

```
Relatório de custo — Receita: Prestígio

╔════════════════════════════╦══════════╦════════╦══════════════════════╦══════════════════════╗
║ Ingrediente                ║ Quant.   ║ Und    ║ Preço unit. (R$/unid)║Custo proporcional(R$)║
╠════════════════════════════╬══════════╬════════╬══════════════════════╬══════════════════════╣
║ leite condensado           ║ 2        ║ lata   ║ 6,20                 ║ 12,40                ║
║ coco ralado                ║ 150      ║ g      ║ 0,075                ║ 11,25                ║
║ chocolate meio amargo      ║ 200      ║ g      ║ 0,060                ║ 12,00                ║
╚════════════════════════════╩══════════╩════════╩══════════════════════╩══════════════════════╝

Custos adicionais:
- Embalagem: R$ 1,50
- Colher: R$ 0,40
- Outras despesas: R$ 1,20
- Mão de obra (12%): R$ 5,46

Resumo final:
─────────────────────────────
Custo total da receita: R$ 43,81  
Rendimento: 21 bolos  
Custo por bolo: R$ 2,09  
Lucro desejado: 35%  
Preço sugerido por bolo: R$ 2,82  
Lucro estimado por bolo: R$ 0,73  
```

## Configurar Custos Adicionais e Lucro

O sistema exibe os valores atuais salvos no config.json e permite alteração:

```
Configurações Atuais

╔════════════════════╦════════════════════════════╗
║ Item               ║ Valor                      ║
╠════════════════════╬════════════════════════════╣
║ Embalagem          ║ R$ 1,50 (100 unidades)     ║
║ Colher             ║ R$ 0,40 (50 unidades)      ║
║ Outras despesas    ║ R$ 1,20                    ║
║ Mão de obra        ║ 12% (percentual)           ║
║ Lucro desejado     ║ 35%                        ║
╚════════════════════╩════════════════════════════╝
```
## Gerar Relatório Geral

O sistema lista todas as receitas com valores detalhados:

```
Relatório Geral

╔════════════╦════════════╦════════════════╦════════════════════╦════════════════════╦════════════════════╗
║ Receita    ║ Rendimento ║ Custo Total(R$)║ Custo por bolo(R$) ║ Preço sugerido(R$) ║ Lucro por bolo(R$) ║
╠════════════╬════════════╬════════════════╬════════════════════╬════════════════════╬════════════════════╣
║ Prestígio  ║ 21         ║ 43,81          ║ 2,09               ║ 2,82               ║ 0,73               ║
║ Nutella    ║ 16         ║ 38,00          ║ 2,38               ║ 3,22               ║ 0,84               ║
║ Mousse     ║ 20         ║ 40,50          ║ 2,03               ║ 2,74               ║ 0,71               ║
╚════════════╩════════════╩════════════════╩════════════════════╩════════════════════╩════════════════════╝

```
Relatório pode ser exportado para .txt, .json ou .csv.


---

## Relatórios Financeiros Integrados

### a) Relatório de Custos e Componentes por Produto

| Produto           | Rendimento | Preço de Custo | Outras Despesas | Mão de Obra | Lucro | Embalagem |
|-------------------|------------|----------------|------------------|-------------|--------|------------|
| Prestígio         | 21         | 58,16          | 58,16            | 69,80       | 69,80  | 14,91      |
| Sonho de Valsa    | 16         | 66,56          | 66,56            | 79,87       | 79,87  | 11,36      |
| Leite Ninho       | 7          | 31,06          | 31,06            | 37,27       | 37,27  | 4,97       |
| Mousse Chocolate  | 16         | 63,60          | 63,60            | 76,32       | 76,32  | 11,36      |
| Mousse Nutella    | 16         | 56,49          | 56,49            | 67,79       | 67,79  | 11,36      |

### b) Relatório Financeiro / Faturamento por Produto

| Produto           | Custo Total | Total | Custo Unitário | Verba/Unidade | Faturamento |
|-------------------|-------------|-------|----------------|----------------|--------------|
| Prestígio         | 58,16       | 224,30| 2,77           | 10,68          | 166,14       |
| Sonho de Valsa    | 66,56       | 250,97| 4,16           | 15,69          | 184,41       |
| Leite Ninho       | 31,06       | 116,78| 4,44           | 16,68          | 85,72        |
| Mousse Chocolate  | 63,60       | 240,32| 3,98           | 15,02          | 176,72       |
| Mousse Nutella    | 56,49       | 214,73| 3,53           | 13,42          | 158,24       |

---

## Organização de Arquivos

```
pinaki/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── calculator.py
│   ├── report.py
│   └── utils.py
├── data/
│   ├── recipes/
│   │   ├── prestigio.json
│   │   └── nutella.json
│   ├── ingredients.json
│   ├── config.json
│   └── finance.json
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Futuras Expansões

- Exportar planilhas (Excel, CSV)
- Interface gráfica (tkinter, PySimpleGUI ou web com Flask)
- Banco de dados (SQLite)
- Suporte a múltiplas moedas/fornecedores
- Histórico de preços e compras
- Aplicativo mobile (Kivy, BeeWare)
- Integração com sites de mercado (scraping ou API)
