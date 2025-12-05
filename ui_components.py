import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox


class PopupItem(ttk.Toplevel):
    def __init__(self, master, callback, item=None):
        super().__init__(master)
        self.title("Cadastro de Item" if item is None else "Editar Item")
        self.master.update_idletasks()
        self.geometry("300x320")
        self.transient(master)
        self.grab_set()

        self.callback = callback
        self.item = item

        # Layout
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=BOTH, expand=True)

        # Campo ID
        ttk.Label(frame, text="ID do Item:", bootstyle=PRIMARY).pack(pady=(5, 0), anchor=W)
        self.id_entry = ttk.Entry(frame, width=10, bootstyle=PRIMARY)
        self.id_entry.pack(fill=X, padx=5)

        ttk.Label(frame, text="Nome:", bootstyle=PRIMARY).pack(pady=(5, 0), anchor=W)
        self.nome_entry = ttk.Entry(frame, bootstyle=PRIMARY)
        self.nome_entry.pack(fill=X, padx=5)

        ttk.Label(frame, text="Quantidade:", bootstyle=PRIMARY).pack(pady=(5, 0), anchor=W)
        self.quantidade_entry = ttk.Entry(frame, bootstyle=PRIMARY)
        self.quantidade_entry.pack(fill=X, padx=5)

        ttk.Label(frame, text="Preço (R$):", bootstyle=PRIMARY).pack(pady=(5, 0), anchor=W)
        self.preco_entry = ttk.Entry(frame, bootstyle=PRIMARY)
        self.preco_entry.pack(fill=X, padx=5)

        ttk.Button(frame, text="Salvar", bootstyle=SUCCESS, command=self.salvar).pack(pady=15, fill=X, padx=5)

        if item:
            # Na edição, o ID não pode ser alterado, apenas as outras propriedades
            self.id_entry.insert(0, str(item["id"]))
            self.id_entry.configure(state=DISABLED, bootstyle=LIGHT)
            self.nome_entry.insert(0, item["nome"])
            self.quantidade_entry.insert(0, str(item["quantidade"]))
            self.preco_entry.insert(0, f"{item['preco']:.2f}".replace('.', ','))

        self.nome_entry.focus_set()

    def salvar(self):
        nome = self.nome_entry.get().strip()
        quantidade_str = self.quantidade_entry.get().strip().replace(",", ".")
        preco_str = self.preco_entry.get().strip().replace(",", ".")

        if self.item is None:
            id_str = self.id_entry.get().strip()
            if not id_str:
                messagebox.showerror("Erro", "O ID do Item é obrigatório na criação.", parent=self)
                return
        else:
            item_id = self.item["id"]

        if not nome or not quantidade_str or not preco_str:
            messagebox.showerror("Erro", "Preencha todos os campos.", parent=self)
            return

        # Validação do ID na CRIAÇÃO
        if self.item is None:
            try:
                item_id = int(id_str)
                if item_id <= 0:
                    messagebox.showerror("Erro", "ID do Item deve ser um número inteiro positivo.", parent=self)
                    return
            except ValueError:
                messagebox.showerror("Erro", "ID do Item deve ser um número inteiro válido.", parent=self)
                return

        # Validação de Quantidade
        try:
            quantidade = int(quantidade_str)
            if quantidade < 0:
                messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo.", parent=self)
                return
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro válido.", parent=self)
            return

        # Validação de Preço
        try:
            preco = float(preco_str)
            if preco < 0:
                messagebox.showerror("Erro", "Preço deve ser um valor positivo.", parent=self)
                return
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número decimal válido.", parent=self)
            return

        self.callback(item_id, nome, quantidade, preco, self.item)
        self.destroy()


# NOVO COMPONENTE: Popup para criar um novo usuário
class PopupCriarUsuario(ttk.Toplevel):
    def __init__(self, master, crud):
        super().__init__(master)
        self.title("Criar Novo Usuário")
        self.master.update_idletasks()
        self.geometry("300x250")
        self.transient(master)
        self.grab_set()
        self.crud = crud

        frame = ttk.Frame(self, padding=15)
        frame.pack(fill=BOTH, expand=True)

        ttk.Label(frame, text="Nome de Usuário:", bootstyle=PRIMARY).pack(pady=(5, 0), anchor=W)
        self.user_entry = ttk.Entry(frame, width=30, bootstyle=PRIMARY)
        self.user_entry.pack(fill=X, padx=5)

        ttk.Label(frame, text="Senha:", bootstyle=PRIMARY).pack(pady=(5, 0), anchor=W)
        self.pass_entry = ttk.Entry(frame, width=30, show="*", bootstyle=PRIMARY)
        self.pass_entry.pack(fill=X, padx=5)

        ttk.Label(frame, text="Confirmar Senha:", bootstyle=PRIMARY).pack(pady=(5, 0), anchor=W)
        self.confirm_pass_entry = ttk.Entry(frame, width=30, show="*", bootstyle=PRIMARY)
        self.confirm_pass_entry.pack(fill=X, padx=5)

        ttk.Button(frame, text="Criar Conta", bootstyle=SUCCESS, command=self.criar).pack(pady=15, fill=X, padx=5)
        self.user_entry.focus_set()

    def criar(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        confirm_password = self.confirm_pass_entry.get().strip()

        if not username or not password or not confirm_password:
            messagebox.showerror("Erro", "Preencha todos os campos.", parent=self)
            return

        if password != confirm_password:
            messagebox.showerror("Erro", "As senhas não coincidem.", parent=self)
            return

        # Chama a função de criação do CRUD
        sucesso, mensagem = self.crud.criar_usuario(username, password)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", mensagem, parent=self)


# NOVO COMPONENTE: Popup para redefinir a senha
class PopupRedefinirSenha(ttk.Toplevel):

    def __init__(self, master, crud):
        super().__init__(master)
        self.title("Esqueci a Senha")
        self.master.update_idletasks()
        self.geometry("300x250")
        self.transient(master)
        self.grab_set()
        self.crud = crud

        frame = ttk.Frame(self, padding=15)
        frame.pack(fill=BOTH, expand=True)

        ttk.Label(frame, text="Nome de Usuário:", bootstyle=PRIMARY).pack(pady=(5, 0), anchor=W)
        self.user_entry = ttk.Entry(frame, width=30, bootstyle=PRIMARY)
        self.user_entry.pack(fill=X, padx=5)

        ttk.Label(frame, text="Nova Senha:", bootstyle=PRIMARY).pack(pady=(5, 0), anchor=W)
        self.new_pass_entry = ttk.Entry(frame, width=30, show="*", bootstyle=PRIMARY)
        self.new_pass_entry.pack(fill=X, padx=5)

        ttk.Label(frame, text="Confirmar Nova Senha:", bootstyle=PRIMARY).pack(pady=(5, 0), anchor=W)
        self.confirm_pass_entry = ttk.Entry(frame, width=30, show="*", bootstyle=PRIMARY)
        self.confirm_pass_entry.pack(fill=X, padx=5)

        ttk.Button(frame, text="Redefinir", bootstyle=WARNING, command=self.redefinir).pack(pady=15, fill=X, padx=5)
        self.user_entry.focus_set()

    def redefinir(self):
        username = self.user_entry.get().strip()
        new_password = self.new_pass_entry.get().strip()
        confirm_password = self.confirm_pass_entry.get().strip()

        if not username or not new_password or not confirm_password:
            messagebox.showerror("Erro", "Preencha todos os campos.", parent=self)
            return

        if new_password != confirm_password:
            messagebox.showerror("Erro", "As novas senhas não coincidem.", parent=self)
            return

        # Chama a função de redefinição do CRUD
        sucesso, mensagem = self.crud.redefinir_senha(username, new_password)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem + "\nUse a nova senha para fazer login.", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", mensagem, parent=self)


class TabelaInventario(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=10)

        colunas = ("ID", "Nome", "Quantidade", "Preço")

        self.tree = ttk.Treeview(
            self,
            columns=colunas,
            show="headings",
            bootstyle=INFO,
        )

        for col in colunas:
            self.tree.heading(col, text=col)
            if col == "Nome":
                self.tree.column(col, width=200, anchor=W)
            else:
                self.tree.column(col, width=120, anchor=CENTER)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(fill=BOTH, expand=True)

    def atualizar(self, itens):
        self.tree.delete(*self.tree.get_children())
        for item in itens:
            # Formata o preço para exibição com separador de milhar (ponto) e decimal (vírgula)
            preco_formatado = f"R$ {item['preco']:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
            self.tree.insert("", END, values=(item["id"], item["nome"], item["quantidade"], preco_formatado))

    def pegar_item_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            return None
        valores = self.tree.item(sel[0], "values")

        try:
            item_id = int(valores[0])
            nome = valores[1]
            quantidade = int(valores[2])
            preco_str = valores[3].replace("R$", "").strip().replace('.', '').replace(',', '.')
            preco = float(preco_str)

            return {
                "id": item_id,
                "nome": nome,
                "quantidade": quantidade,
                "preco": preco
            }
        except (ValueError, IndexError):
            # Erro na conversão de dados da tabela
            messagebox.showerror("Erro de Dados", "Não foi possível ler o item selecionado corretamente.")
            return None