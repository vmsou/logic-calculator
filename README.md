# Resolução de Problemas com Lógica Matemática - Lógica Proposicional
Trabalho Prático com o objetivo de desenvolver um gerador de Tabela Verdade de fórmulas proposicionais.

# Grupo
* Vinicius Marques da Silva Oliveira

## Sobre o Projeto
Desenvolvimento de uma ferramenta para resolver problemas de Lógica Proposicional.
Realiza operações de uma fórmula lógica, no formato de tabela-verdade.

Essa é uma lista dos recursos utilizados para realizar esse projeto

## Principais Funcionalidades
### Cálculo
- [X] VARIABLES
- [x] NOT
- [x] AND
- [x] OR
- [x] IMPLICATION
- [x] EQUIVALENCE
- [X] XOR
- [X] NOR
- [X] NAND

## Pastas

* ### logic - Compõe os recursos para fazer o parse dos simbolos proposicionais
    * #### calculator: Utilizado para fazer o parse e cálculo proposicionais
    * #### model: Representa modelos lógicos como Expressões, Operandos e Operadores.
    * #### stream: Utilizado para criar e separar tokens de um texto a partir de simbolos predeterminados
* ### wordtree - Usado pelo stream para fazer busca de palavras em arvore de prefixos

## 🛠 Pacotes
- [tabulate](https://pypi.org/project/tabulate/) 
```bash
pip install -r requirements.txt
```
## Como executa-lo
Se você ter acesso a um terminal
```bash
cd src
```
```bash
python main.py
```

## Status
<h4 align="center"> 
	✔️ 🚧️ Funcionando (Em desenvolvimento) 🚧️ ✔️
</h4>

## Para fazer:
- [ ] IMPLICATION CHAIN PRECEDENCE
- [x] EQUIVALENCE CHAIN PRECEDENCE
- [ ] EQUIVALENCES
- [ ] SIMPLIFICATION

