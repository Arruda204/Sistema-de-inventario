import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app_screens import LoginFrame, InventoryFrame
from crud import InventarioCRUD
from tkinter import messagebox
import os


# Define a classe principal da aplicação
class InventarioApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")  # Tema dark-mode moderno
        self.title("Sistema de Gestão de Inventário")
        self.geometry("800x600")
        self.center_window()

        # 1. Inicializa a lógica de persistência (CRUD)
        try:
            self.crud = InventarioCRUD()
            print("InventarioCRUD e usuários carregados com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha ao inicializar o sistema de dados: {e}")
            self.destroy()  # Fecha a aplicação se não puder carregar o CRUD
            return

        self.current_frame = None
        self.show_login()

    def center_window(self):

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def switch_frame(self, new_frame_class, *args, **kwargs):

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill=BOTH, expand=True)

    def show_login(self):

        self.switch_frame(LoginFrame, on_success=self.show_inventory, crud=self.crud)

    def show_inventory(self):

        self.switch_frame(InventoryFrame, crud=self.crud, on_logout=self.show_login)



if __name__ == "__main__":
    app = InventarioApp()
    app.mainloop()