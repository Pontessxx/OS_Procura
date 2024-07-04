import os
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess  # Para abrir o diretório no explorador de arquivos

class ProcurarOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador de Arquivos")
        self.os_var = tk.StringVar()
        self.ritm_var = tk.StringVar()
        self.chg_var = tk.StringVar()
        self.inc_var = tk.StringVar()
        self.customize_root()
        self.setup_gui()

    def customize_root(self):
        # Personalizando a janela principal
        self.root.geometry('500x300')  # Ajuste o tamanho para acomodar os novos campos
        self.root.configure(bg='black')  # Define a cor de fundo
        self.root.resizable(False, False)  # Impede o redimensionamento da janela
        self.center_window(500, 300)

    def center_window(self, width, height):
        # Calcula a posição central para a janela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_gui(self):
        # Configurando os widgets utilizando place
        ttk.Label(self.root, text="Digite o código OS:", background='black', foreground='white').place(relx=0.05, rely=0.05, relwidth=0.4, relheight=0.1)
        ttk.Entry(self.root, textvariable=self.os_var).place(relx=0.5, rely=0.05, relwidth=0.45, relheight=0.1)

        ttk.Label(self.root, text="Digite o código RITM:", background='black', foreground='white').place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.1)
        ttk.Entry(self.root, textvariable=self.ritm_var).place(relx=0.5, rely=0.2, relwidth=0.45, relheight=0.1)

        ttk.Label(self.root, text="Digite o código CHG:", background='black', foreground='white').place(relx=0.05, rely=0.35, relwidth=0.4, relheight=0.1)
        ttk.Entry(self.root, textvariable=self.chg_var).place(relx=0.5, rely=0.35, relwidth=0.45, relheight=0.1)

        ttk.Label(self.root, text="Digite o código INC:", background='black', foreground='white').place(relx=0.05, rely=0.5, relwidth=0.4, relheight=0.1)
        ttk.Entry(self.root, textvariable=self.inc_var).place(relx=0.5, rely=0.5, relwidth=0.45, relheight=0.1)

        ttk.Button(self.root, text="Buscar e abrir pasta", command=self.buscar_arquivo).place(relx=0.3, rely=0.7, relwidth=0.4, relheight=0.15)

    def buscar_arquivo(self):
        os_code = self.os_var.get().strip()
        ritm_code = self.ritm_var.get().strip()
        chg_code = self.chg_var.get().strip()
        inc_code = self.inc_var.get().strip()

        # Validating input
        if not any([os_code, ritm_code, chg_code, inc_code]):
            messagebox.showinfo("Erro", "Por favor, insira ao menos um código (OS, RITM, CHG, ou INC).")
            return

        # Prepending codes if necessary
        if os_code and not os_code.startswith("EEc"):
            os_code = "EEc" + os_code
        if ritm_code and not ritm_code.startswith("RITM"):
            ritm_code = "RITM" + ritm_code
        if chg_code and not chg_code.startswith("CHG"):
            chg_code = "CHG" + chg_code
        if inc_code and not inc_code.startswith("INC"):
            inc_code = "INC" + inc_code

        # Search process
        found = False
        for year in range(2009, 2025):  # Assuming the range from 2009 to 2024
            base_path = f"\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\20{str(year)[-2:]}\\01 - CTI\\CABEAMENTO\\OPEN"
            if os.path.exists(base_path):
                for folder in os.listdir(base_path):
                    if (os_code in folder if os_code else True) and (ritm_code in folder if ritm_code else True) and (chg_code in folder if chg_code else True) and (inc_code in folder if inc_code else True):
                        full_path = os.path.join(base_path, folder)
                        subprocess.run(['explorer', full_path], shell=True)
                        messagebox.showinfo("Resultado", f"Pasta aberta: {full_path}")
                        found = True
                        break
                if found:
                    break
        if not found:
            messagebox.showinfo("Resultado", "Pasta com os códigos especificados não encontrada.")

# Criando a janela principal
root = tk.Tk()
app = ProcurarOS(root)
root.mainloop()
