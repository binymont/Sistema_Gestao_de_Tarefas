#   Sistema de Gestão de Tarefas - Grupo 9

[![Status   do Projeto](https://img.shields.io/badge/status-em_desenvolvimento-yellow)](https://github.com/seu-usuario/seu-repositorio)
[![Licença](https://img.shields.io/badge/licença-MIT-green)](https://opensource.org/licenses/MIT)
[![Linguagens](https://img.shields.io/github/languages/count/seu-usuario/seu-repositorio)](https://github.com/seu-usuario/seu-repositorio)

Este é um sistema web para gerenciamento de tarefas, criado com o objetivo de organizar atividades de forma simples e eficiente.

##   Visão Geral

O Sistema de Gestão de Tarefas permite que usuários criem, organizem e acompanhem suas tarefas de forma intuitiva. Com funcionalidades como cadastro, edição, exclusão e filtragem por status, o sistema visa aumentar a produtividade e a organização pessoal ou em equipe. A interface web é responsiva, garantindo uma boa experiência em diferentes dispositivos.

##   Funcionalidades

* Cadastro de tarefas: Permite adicionar novas tarefas com um título descritivo e uma descrição detalhada.
* Marcar tarefas como concluídas: Os usuários podem marcar tarefas como finalizadas, facilitando o acompanhamento do progresso.
* Editar tarefas: É possível modificar o título e a descrição de tarefas existentes para mantê-las atualizadas.
* Excluir tarefas: Tarefas que não são mais relevantes podem ser removidas do sistema.
* Filtros por status: As tarefas podem ser filtradas por seu status (pendente, em andamento, concluída), permitindo uma visualização focada nas atividades desejadas.
* Interface intuitiva e responsiva: A interface web foi projetada para ser fácil de usar e se adaptar a diferentes tamanhos de tela (desktops, tablets e smartphones).
* Autenticação de usuários: Os usuários podem se registrar, fazer login e logout de suas contas.
* Recuperação de senha: Funcionalidade para recuperar senhas esquecidas via e-mail.
* Upload de foto de perfil: Os usuários podem personalizar suas contas com uma foto de perfil.

##   Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas em sua máquina:

* Python (versões 3.9, 3.10 ou 3.11)
* pip (gerenciador de pacotes do Python)

##   Instalação

1.  Clone o repositório (branch master):

    * Abra o Terminal (macOS ou Linux) ou Prompt de Comando (Windows).
    * Navegue até o diretório onde você deseja salvar o projeto.
    * Execute o seguinte comando:

        ```bash
        git clone -b master   [https://github.com/binymont/Sistema_Gestao_de_Tarefas.git](https://github.com/binymont/Sistema_Gestao_de_Tarefas.git)
        ```

2.  Acesse o diretório do projeto:

    * No Terminal ou Prompt de Comando, navegue até a pasta do projeto usando o comando `cd`. Por exemplo:

        ```bash
        cd Sistema_Gestao_de_Tarefas
        ```

3.  Instale as dependências do Python:

    * Certifique-se de que você está no diretório raiz do projeto.
    * Execute o seguinte comando:

        ```bash
        pip install -r requirements.txt
        ```

    * *(Certifique-se de que o arquivo `requirements.txt` esteja na raiz do seu projeto.)*

4.  Instale o `python-dotenv` (opcional, mas recomendado):

    * Para garantir que as variáveis de ambiente do arquivo `.env` sejam carregadas corretamente, é recomendável instalar a biblioteca `python-dotenv`.
    * Execute o seguinte comando:

        ```bash
        pip install python-dotenv
        ```

##   Execução da Aplicação

1.  Inicie a aplicação Flask:

    ```bash
    python app.py
    ```

    A aplicação estará disponível em `http://127.0.0.1:5000/` por padrão.

    * Para executar a aplicação em produção, você pode precisar usar um servidor WSGI como Gunicorn. Consulte a documentação do Flask para mais detalhes.
    * A aplicação também lê a porta a partir da variável de ambiente `PORT` (útil para deploy em plataformas como Heroku):

        ```bash
        PORT=8000 python app.py
        ```

##   Uso

1.  **Registro e Login:**

    * Acesse a página de registro (`/register`) para criar uma nova conta.
    * Acesse a página de login (`/login`) para fazer login com uma conta existente.

2.  **Gerenciamento de Tarefas:**

    * Na página principal (`/`), você pode ver a lista de tarefas, adicionar novas tarefas, editar tarefas existentes, marcar tarefas como concluídas e excluir tarefas.
    * Use os filtros para visualizar tarefas por status (pendente, em andamento, concluída).

3.  **Foto de Perfil:**

    * Você pode fazer upload de uma foto de perfil na página principal.

4.  **Recuperação de Senha:**

    * Na página de login, há um link para a página de recuperação de senha (`/forgot-password`).
    * Insira seu e-mail para receber um link para redefinir sua senha.

##   Testes

A aplicação inclui testes automatizados. Para executá-los:

```bash
python test_app.py
