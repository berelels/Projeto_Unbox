# 📦 Unbox | Sistema de Inventário Escolar (v1.0)

Uma aplicação desktop completa, desenvolvida em **Python**, para modernizar o controle de patrimônio e estoque escolar.

O **Unbox** vai além de um simples CRUD: ele oferece controle de acesso, geração de documentos automáticos e relatórios gerenciais. O projeto utiliza a arquitetura **MVC (Model-View-Controller)** para garantir escalabilidade e o framework **Flet** para uma interface gráfica moderna baseada em Material Design.

## 🚨 Sobre o Projeto

Este software foi desenvolvido como parte de um portfólio acadêmico e trabalho colaborativo. O sistema utiliza banco de dados **SQLite** local e manipulação de arquivos para logs e configurações.

## ✨ Funcionalidades Principais

### 📊 Gestão e Dashboard
* **Dashboard Analítico:** Painel com indicadores em tempo real de itens totais, itens emprestados e **alertas de estoque baixo**.
* **Relatórios em Excel:** Exportação completa do inventário para `.xlsx` com um clique.
* **Log de Auditoria:** Registro interno de criação e exclusão de usuários para segurança.

### 🔐 Segurança e Controle de Acesso
* **Sistema de Login:** Autenticação segura com criptografia de senhas (SHA-256).
* **Permissões (RBAC):** Diferenciação de interface e permissões entre **ADMIN** (acesso total) e usuários comuns (Professores, Coordenadores).
    * *Apenas Admins podem gerenciar outros usuários.*

### 📦 Controle de Estoque
* **Cadastro Completo:** Registro de itens com Nº de Patrimônio, Categoria, Localização e Estoque Mínimo.
* **Status Visual:** Indicadores coloridos na listagem (🟢 Disponível, 🟠 Baixo Estoque, 🔴 Sem Estoque).

### 📄 Movimentações Inteligentes
* **Fluxo de Empréstimo:** Saída de itens vinculada a um responsável.
* **Validação de Devolução:** O sistema garante que apenas quem retirou o item pode devolvê-lo.
* **Comprovantes Automáticos:** Geração de **Recibos em PDF** no ato do empréstimo, contendo data, hora e código de verificação.

## 💻 Tecnologias Utilizadas

O projeto foi construído utilizando as seguintes bibliotecas:

* **[Flet](https://flet.dev):** Construção da interface gráfica (GUI).
* **SQLite3:** Banco de dados relacional (nativo).
* **Pandas:** Manipulação de dados e exportação para Excel.
* **FPDF:** Geração dinâmica de recibos em PDF.
* **Pytz:** Gerenciamento de fusos horários (Timezone BR).
* **Hashlib:** Segurança e criptografia de senhas.

## 🚀 Estrutura do Projeto (MVC)

O código segue rigorosamente a separação de responsabilidades:

| Arquivo | Componente | Responsabilidade |
| :--- | :--- | :--- |
| **unbox_model.py** | **Model** | Regras de negócio, acesso ao SQLite, hashing de senhas e validação de dados. |
| **unbox_view.py** | **View** | Camada visual. Contém os layouts, formulários, tabelas e lógica de exibição condicional (Admin vs User). |
| **controller.py** | **Controller** | Orquestrador. Conecta a View ao Model, gerencia eventos, gera PDFs e controla a navegação. |
| **login.py** | **View (Login)** | Tela inicial de autenticação e feedback de acesso. |

## 🔧 Instalação e Execução

Para rodar este projeto localmente:

### 1. Clonar o Repositório
```bash
git clone [https://github.com/berelels/Projeto-Unbox](https://github.com/berelels/Projeto-Unbox)
cd Projeto-Unbox
````

### 2\. Instalar Dependências

O projeto agora requer bibliotecas adicionais. Execute:

```bash
pip install flet pandas openpyxl fpdf pytz
```

### 3\. Executar a Aplicação

Inicie o sistema pelo arquivo principal (certifique-se de que ele chama a tela de login):

```bash
flet run main.py
```

> **Nota:** Ao iniciar pela primeira vez, o sistema criará automaticamente o banco de dados `inventory.db` e um usuário **Admin** padrão (`user: admin` | `pass: admin123`).

## 👥 Autores

  * **berelels**
  * **bielzkk123**
  * **gabrielbx7**

## 📜 Licença

Este projeto é de código aberto. Sinta-se livre para contribuir\!
