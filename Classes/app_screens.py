import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
# Importa os novos popups de usuário
from ui_components import TabelaInventario, PopupItem, PopupCriarUsuario, PopupRedefinirSenha


class LoginFrame(ttk.Frame):
    # ALTERAÇÃO: Agora aceita uma instância do CRUD
    def __init__(self, master, on_success, crud):
        super().__init__(master, padding=20)
        self.on_success = on_success
        self.crud = crud  # Armazena a instância do CRUD
        self.pack(fill=BOTH, expand=True)

        # Centraliza o formulário
        form_frame = ttk.Frame(self, padding=20, relief=FLAT, borderwidth=1)
        form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        ttk.Label(form_frame, text="Acesso ao Sistema", font=("Helvetica", 16, "bold"), bootstyle=PRIMARY).pack(pady=15)

        # Usuário
        ttk.Label(form_frame, text="Usuário:").pack(pady=(10, 0), anchor=W)
        self.user_entry = ttk.Entry(form_frame, width=30, bootstyle=PRIMARY)
        self.user_entry.pack(pady=5, padx=10)

        # Senha
        ttk.Label(form_frame, text="Senha:").pack(pady=(10, 0), anchor=W)
        self.pass_entry = ttk.Entry(form_frame, width=30, show="*", bootstyle=PRIMARY)
        self.pass_entry.pack(pady=5, padx=10)

        self.user_entry.bind('<Return>', lambda event: self.pass_entry.focus_set())
        self.pass_entry.bind('<Return>', lambda event: self.autenticar())

        # Botão de Login
        ttk.Button(form_frame, text="Entrar", command=self.autenticar, bootstyle=SUCCESS).pack(pady=(20, 10), fill=X,
                                                                                               padx=10)

        # NOVO: Botões de Ação Secundária
        action_frame = ttk.Frame(form_frame)
        action_frame.pack(fill=X, padx=10, pady=(0, 10))

        ttk.Button(action_frame, text="Criar Usuário", command=self.abrir_criar_usuario, bootstyle=(INFO, OUTLINE),
                   width=15).pack(side=LEFT, expand=True, padx=(0, 5))
        ttk.Button(action_frame, text="Esqueci a Senha", command=self.abrir_redefinir_senha,
                   bootstyle=(SECONDARY, OUTLINE), width=15).pack(side=RIGHT, expand=True, padx=(5, 0))

        self.user_entry.focus_set()

    def autenticar(self):
        usuario = self.user_entry.get()
        senha = self.pass_entry.get()

        # ALTERAÇÃO: Usa o método CRUD para autenticação
        if self.crud.autenticar_usuario(usuario, senha):
            self.on_success()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos. Tente novamente.")
            self.pass_entry.delete(0, END)
            self.user_entry.focus_set()

    # NOVO: Abre o popup de criação de usuário
    def abrir_criar_usuario(self):
        PopupCriarUsuario(self.master, self.crud)

    # NOVO: Abre o popup de redefinição de senha
    def abrir_redefinir_senha(self):
        PopupRedefinirSenha(self.master, self.crud)


class InventoryFrame(ttk.Frame):
    def __init__(self, master, crud, on_logout):
        super().__init__(master, padding=10)
        self.crud = crud
        self.on_logout = on_logout
        self.pack(fill=BOTH, expand=True)

        # Cabeçalho com Logout
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=X, pady=(0, 10))
        ttk.Label(header_frame, text="Controle de Inventário", font=("Helvetica", 18, "bold"), bootstyle=PRIMARY).pack(
            side=LEFT)
        ttk.Button(header_frame, text="Sair", command=self.on_logout, bootstyle=(DANGER, OUTLINE)).pack(side=RIGHT)

        # Tabela
        self.tabela = TabelaInventario(self)
        self.tabela.pack(fill=BOTH, expand=True)

        # Botões
        frame_btn = ttk.Frame(self)
        frame_btn.pack(pady=10)

        ttk.Button(frame_btn, text="Adicionar Item", bootstyle=SUCCESS,
                   command=self.adicionar_item).pack(side=LEFT, padx=10)

        ttk.Button(frame_btn, text="Editar Item", bootstyle=WARNING,
                   command=self.editar_item).pack(side=LEFT, padx=10)

        ttk.Button(frame_btn, text="Excluir Item", bootstyle=DANGER,
                   command=self.deletar_item).pack(side=LEFT, padx=10)

        self.tabela.atualizar(self.crud.ler_itens())

    # -------- CRUD Actions --------
    def adicionar_item(self):
        PopupItem(self, self.callback_salvar_item)

    def editar_item(self):
        item = self.tabela.pegar_item_selecionado()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um item para editar")
            return
        PopupItem(self, self.callback_salvar_item, item=item)

    def deletar_item(self):
        item = self.tabela.pegar_item_selecionado()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um item para excluir")
            return

        if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o item ID {item['id']} ({item['nome']})?"):
            self.crud.deletar_item(item["id"])
            self.tabela.atualizar(self.crud.ler_itens())

    def callback_salvar_item(self, item_id, nome, quantidade, preco, item):
        if item is None:
            self.crud.criar_item(item_id, nome, quantidade, preco)
        else:
            self.crud.atualizar_item(item_id, nome, quantidade, preco)

        self.tabela.atualizar(self.crud.ler_itens())