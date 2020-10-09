[![Build Status](https://travis-ci.org/taciogt/snacks-machine.svg?branch=main)](https://travis-ci.org/taciogt/snacks-machine)
[![codecov](https://codecov.io/gh/taciogt/snacks-machine/branch/main/graph/badge.svg)](https://codecov.io/gh/taciogt/snacks-machine)

# Snacks Machine

Máquina de Salgadinhos.

## Decisões de Arquitetura

Snacks dependem da moeda (`Currency`) e não o contrário, porque a moeda é uma entidade mais elementar e pode ser isoladamente para ser reutilizada em outras aplicações.

## Hipóteses Assumidas
* A máquina possui uma quantidade limitada de moedas e notas. 
  * Essa quantidade varia conforme os usuários interagem com a máquina.
  * Caso não seja possível fornecer o troco adequado para o usuário, todo dinheiro inserido pelo usuário deve ser devolvido. 