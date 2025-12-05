# Sistema de Gestão de Inventário (Desktop - Tkinter/TtkBootstrap)
Sistema simples e eficiente para controle de estoque e inventário, desenvolvido em Python utilizando o Tkinter (com o tema moderno TtkBootstrap) para a interface gráfica e persistência de dados em arquivos JSON.

# Recursos Principais
Interface Amigável: Design moderno e responsivo com TtkBootstrap.

Controle CRUD: Adição, visualização, edição e exclusão de itens.

Persistência de Dados: Todos os dados (inventário e usuários) são salvos em arquivos JSON.

Gestão de Usuários: Funcionalidades de Login, Criação de Usuário e Recuperação de Senha.

Validação: Validação de tipos de dados (ID, quantidade, preço).

# Como Rodar o Projeto Localmente
Siga estas etapas para configurar e executar o projeto em sua máquina.

Pré-requisitos

Você precisa ter o Python 3 instalado.

Instalação das Dependências
Este projeto requer apenas uma biblioteca externa: ttkbootstrap.

# Certifique-se de estar usando um ambiente virtual (venv)
pip install ttkbootstrap

Execução
Após instalar as dependências, execute o arquivo principal:

python main.py

# Acesso Padrão
Na primeira execução, o sistema cria um usuário administrador padrão:

Campo

Valor

Usuário

admin

Senha

123456

Se desejar, você pode criar novos usuários usando o botão "Criar Usuário" na tela de login.

# Estrutura do Projeto
O projeto é organizado nos seguintes módulos:

Arquivo

Descrição

main.py

Ponto de entrada da aplicação. Inicializa o CRUD e a janela principal.

crud.py

Lógica de acesso a dados (CRUD) e persistência de itens e usuários nos arquivos JSON.

app_screens.py

Define as classes de telas (Login e Inventário) e orquestra a navegação.

ui_components.py

Define componentes reutilizáveis da interface (Popups de Item, Cadastro de Usuário, Tabela).

inventario.json

Gerado automaticamente. Armazena os dados do inventário. (Ignorado pelo Git)

usuarios.json

Gerado automaticamente. Armazena os usuários e senhas. (Ignorado pelo Git)

Desenvolvido com Python & TtkBootstrap
