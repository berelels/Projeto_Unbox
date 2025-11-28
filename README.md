-----

# 📦 Unbox | Sistema de Inventário Escolar

Uma aplicação desktop robusta e intuitiva construída em **Python**, desenvolvida para facilitar a organização, controle e gestão de patrimônio e estoque escolar.

O projeto utiliza a arquitetura **MVC (Model-View-Controller)** para garantir um código limpo e escalável, e o framework **Flet** para uma interface gráfica moderna e responsiva baseada em Material Design.

## 🚨 Atenção

Este projeto foi desenvolvido como parte de um trabalho colaborativo e serve como portfólio acadêmico. O sistema utiliza um banco de dados local **SQLite**. Sinta-se à vontade para explorar o código, sugerir melhorias ou usar como base para estudos\!

## ✨ Funcionalidades

  * **Dashboard Interativo:** Visão geral do sistema (em desenvolvimento).
  * **Gestão de Categorias:** Cadastro e listagem de categorias de produtos (ex: Eletrônicos, Mobiliário) com validação de dados.
  * **Cadastro de Itens:** Registro detalhado de bens com número de série, localização e definição de estoque mínimo.
  * **Controle de Movimentações:** Sistema de entrada e saída (IN/OUT) vinculado a funcionários (Staff), com verificação automática de saldo em estoque.
  * **Navegação Fluida:** Menu lateral (Navigation Rail) para alternar facilmente entre as telas de Dashboard, Categorias, Itens e Movimentações.
  * **Banco de Dados Integrado:** Persistência de dados automática utilizando SQLite com integridade referencial (Foreign Keys).

## 💻 Tecnologias Utilizadas

O projeto é escrito 100% em **Python** e utiliza as seguintes tecnologias:

  * **[Flet](https://flet.dev):** Framework para construção de interfaces gráficas (GUI) modernas.
  * **SQLite3:** Banco de dados relacional leve e serverless, nativo do Python.
  * **Padrão MVC:** Organização estrutural para separar lógica de dados, interface e regras de negócio.

## 🚀 Estrutura do Projeto (Arquitetura MVC)

O código foi modularizado seguindo rigorosamente o padrão Model-View-Controller:

| Arquivo | Componente | Responsabilidade |
| :--- | :--- | :--- |
| **unbox\_model.py** | **Model** | Gerencia o banco de dados e a lógica de negócio. Cria tabelas (`inventory`, `staff`, `locations`, `movements`) e executa queries SQL. |
| **unbox\_view.py** | **View** | Responsável pela **UI**. Constrói o layout, tabelas, formulários e o menu lateral usando componentes do Flet. |
| **controller.py** | **Controller** | O "cérebro" da aplicação. Conecta a View ao Model, gerencia eventos (cliques, trocas de tela) e atualiza a interface dinamicamente. |

## 🔧 Instalação e Execução

Para rodar este projeto localmente em sua máquina:

### Pré-requisitos

  * Python 3.7 ou superior instalado.

### 1\. Clonar o Repositório

```bash
git clone https://github.com/berelels/Projeto-Unbox
```

### 2\. Instalar Dependências

O projeto requer a biblioteca Flet. Instale via pip:

```bash
pip install flet
```

### 3\. Executar a Aplicação

Certifique-se de ter um arquivo principal (ex: `main.py`) que inicializa o MVC. Execute o comando:

```bash
python main.py
# ou
flet run main.py
```

> **Nota:** Ao iniciar a aplicação pela primeira vez, o arquivo `inventory.db` será criado automaticamente na raiz do projeto.

## 👥 Autores

Este projeto foi desenvolvido em colaboração por:

  * **berelels**
  * **bielzkk123**
  * **gabrielbx7**

## 📜 Licença

Este projeto é de código aberto, por CC. Sinta-se livre para contribuir\!
