[![Build Status](https://travis-ci.org/taciogt/snacks-machine.svg?branch=main)](https://travis-ci.org/taciogt/snacks-machine)
[![codecov](https://codecov.io/gh/taciogt/snacks-machine/branch/main/graph/badge.svg)](https://codecov.io/gh/taciogt/snacks-machine)
[![Maintainability](https://api.codeclimate.com/v1/badges/72a9470509c5d6873750/maintainability)](https://codeclimate.com/github/taciogt/snacks-machine/maintainability)

# Snacks Machine

Máquina de Salgadinhos.

## Decisões de Arquitetura

### Desenho geral

O sistema é dividido em dois grandes módulos: `core` e `backend`.

`core` é o módulo base do sistema, responsável por todas as regras de negócio e completamente desacoplado de tecnologias ou interfaces específicas. Esse módulo não conhece nada a respeito de protocolos HTTP ou sobre como interagir com banco de dados ou outras soluções de persistência de dados.

`backend` é o módulo do sistema responsável por toda a interface web e por implementar soluções de persistência dos dados (se necessário).

Essa separação de responsabilidades é construída aplicando os princípios SOLID, principalmente o Princípio de Substituição de Liskov e o Princípio de Inversão de Dependências.
A relação entre todos os módulos do sistema pode ser entendida através de 3 formato de relações que representam o padrão da arquitetura definida:
* Relação entre os componentes de um módulo do `core`. Por exemplo, os elementos dentro de `core.snacks`.
* Relação entre os diferentes módulos dentro do módulo `core`. Como os módulos `core.snacks` e `core.currency` se relacionam.
* Relação entre um módulo do `backend` com o módulo correspondente em `core`. Por exemplo, como `backend.snacks` e `core.snacks` interagem.

#### Componentes dentro de um módulo do pacote core

* `entities.py`
  * Entidades responsáveis por representar os dados fundamentais que modelam as regras de negócio.
  * O tráfego dos dados entre os módulo é feito através dessas entidades.
* `repositories.py`:
  * Define a interface através da qual o sistema realiza a persistência das Entidades.
  * Para fins de teste, o  módulo core pode definir Repositories simples que fazem armazenamento dos dados em memória.
* `services.py`
  * Define e implementa todas as regras de negócio (use cases) esperados para o sistema.
  * Depende apenas de Entidades e Repositories abstratos (interfaces).


#### Relação entre os módulos core

* `currency.py`
  * Responsável por todos os dados e operações referentes a moeda
  * Não conhece nada sobre snacks.
* `snacks.py`
  * Responsável por todos os dados e operações referentes a snacks
  * Para qualquer operação relacionada a dinheiro, utiliza o módulo `currency`

Snacks dependem da moeda (`Currency`) e não o contrário, porque a moeda é uma entidade mais elementar e pode ser isolada para ser uso em outras aplicações.


### Relação entre backend e core

* `backend.<x>.repositories`
  * Define uma ou mais implementações concreta para a interface definida em `core.<x>.repositories`
  * A implementação definitiva do Repository pode evoluir conforme as necessidades reais do sistema. Por exemplo:
     * Armazenamento em memória
     * Armazenamento em arquivo de texto
     * Armazenamento em banco de dados local
     * Armazenamento em banco de dados remoto.
     
* `backend.<x>.services`
  * Define uma implementação de Repository como padrão
  * Atua fazendo algo próximo a um [currying](https://en.wikipedia.org/wiki/Currying) das funções em `core.<x>.services`. Se necessário, pode mudar um pouco a assinatura da função apenas para se aplicar melhor ao contexto do backend (por exemplo, um argumento `snack: Snack` pode virar `snack_name: str`).    

* `backend.<x>.views`
  * Camada responsável por implementar os endpoints, tratando o request HTTP e retornando a resposta adequada.
  * Única camada ciente do contexto web do backend
  * Para tratar casos de exceção, utiliza as exceções definidas em `core.<x>.exceptions` para fazer o controle de fluxo e retornar o status code adequado para cda situação. 
    
 
  
 
![Diagrama de Arquitetura](diagrams.png)



## Hipóteses Assumidas
* A máquina possui uma quantidade limitada de moedas e notas. 
  * Essa quantidade varia conforme os usuários interagem com a máquina.
  * Caso não seja possível fornecer o troco adequado para o usuário, todo dinheiro inserido pelo usuário deve ser devolvido.
* Para fins de prototipação, não é críticao considerar aspectos de segurança como autenticação de usuários ou proteção contra CSRF.

## Melhorias Possíveis

* Implementar o `CashRepository` utilizando um sistema de persistência que não seja em memória, e que permita escalabilidade da aplicação (como um banco de dados)

* O `CashAmount` não faz uso otimizado da memória pois armazena cada nota/moeda como um objeto diferente em uma lista. Essa otimização pode ser feita de duas formas (simultaneamente):  
  * Em vez de armazenar uma lista com todas as notas/moedas, armazenar apenas a quantidade de cada tipo e nota/moeda.
  * Além disso, tranformar cada objeto `Cash(2), Cash(.5), ...` em um Singleton correspondente a cada valor.
  
* O banco de dados utilizado pelo backend é um SQLite. Pode-se utilizar o MySQL caso seja necessário um banco de dados em produção. Utilizando docker compose é possível testar essa solução sem adicionar nenhuma dificuldade ao setup do ambiente de desenvolvimento.  
    