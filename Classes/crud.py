import json
import os


# --- Configurações de Persistência ---
ARQUIVO_DADOS = "inventario.json"
ARQUIVO_USUARIOS = "usuarios.json"


class InventarioCRUD:

    def __init__(self):
        self.itens = self._carregar_dados()
        self.id_atual = self._proximo_id()
        self.usuarios = self._carregar_usuarios()


        if not self.usuarios:
            self.usuarios = {"admin": "123456"}
            self._salvar_usuarios()

    # --- Métodos de Persistência de Dados (Itens) ---

    def _carregar_dados(self):

        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def _salvar_dados(self):
        try:
            with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
                json.dump(self.itens, f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar dados: {e}")

            # --- Métodos de Persistência de Usuários ---

    def _carregar_usuarios(self):
        if os.path.exists(ARQUIVO_USUARIOS):
            try:
                with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}

    def _salvar_usuarios(self):
        try:
            with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
                json.dump(self.usuarios, f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar usuários: {e}")

    # --- Métodos de CRUD de Usuários ---

    def autenticar_usuario(self, username, password):
        """Verifica se o nome de usuário e a senha correspondem."""
        return self.usuarios.get(username) == password

    def criar_usuario(self, username, password):
        """Adiciona um novo usuário ao sistema."""
        if username in self.usuarios:
            return False, "Nome de usuário já existe."
        if not username or not password:
            return False, "Usuário e senha não podem ser vazios."

        self.usuarios[username] = password
        self._salvar_usuarios()
        return True, "Usuário criado com sucesso."

    def redefinir_senha(self, username, new_password):
        """Redefine a senha de um usuário existente."""
        if username not in self.usuarios:
            return False, "Nome de usuário não encontrado."
        if not new_password:
            return False, "A nova senha não pode ser vazia."

        self.usuarios[username] = new_password
        self._salvar_usuarios()
        return True, "Senha redefinida com sucesso."

    # --- Métodos de CRUD de Itens ---

    def _proximo_id(self):
        if self.itens:
            return max(item["id"] for item in self.itens) + 1
        return 1

    def id_existe(self, item_id):
        return any(item["id"] == item_id for item in self.itens)

    def criar_item(self, item_id, nome, quantidade, preco):

        if self.id_existe(item_id):
            item_id = self._proximo_id()
            print(f"ID {item_id} já existia. Novo ID gerado: {item_id}")
            self.id_atual = item_id + 1
        else:
            if item_id >= self.id_atual:
                self.id_atual = item_id + 1

        novo = {
            "id": item_id,
            "nome": nome,
            "quantidade": quantidade,
            "preco": preco
        }
        self.itens.append(novo)
        self.itens.sort(key=lambda x: x["id"])
        self._salvar_dados()
        return novo

    def ler_itens(self):
        return self.itens

    def atualizar_item(self, item_id, nome, quantidade, preco):
        for item in self.itens:
            if item["id"] == item_id:
                item["nome"] = nome
                item["quantidade"] = quantidade
                item["preco"] = preco
                self._salvar_dados()
                return True
        return False

    def deletar_item(self, item_id):
        for item in self.itens:
            if item["id"] == item_id:
                self.itens.remove(item)
                self._salvar_dados()
                return True
        return False