import customtkinter as ctk
import pyodbc
from tkinter import ttk

class ControleApp:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('C:\\Users\\Henrique\\OneDrive\\Anexos\\FIAP_2024\\OS_Procura\\Busca_os\\img\\bradimg.ico')
        ctk.set_appearance_mode('dark')
        root.geometry('1130x600')
        root.title('Controle de Frequência')
        root.minsize(1130, 600)
        self.center_window(1100, 600)

        self.my_dict = {
            'font': '#c2c2c2',
            'Heading_color': '#434343',
            'preto': '#111',
            'frames_ajuste': '#666',
            'frames_ajuste2': '#777',
            'hover': '#111',
            'selecionado': '#111',
            'menu-sup': '#333',
            'menu-inf': '#222',
            'borda': '#a3a3a3',
            'adicionar_btn': 'green',
            'remover_btn': 'red',
            'hover_treeview': '#cc092f',
        }

        self.buttons = {}
        self.conn = self.connect_to_db()
        self.selected_site = None
        self.selected_empresa = None
        self.setup_auto()

    def connect_to_db(self):
        try:
            con_string =r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Henrique\Downloads\Controle.accdb'
            conn = pyodbc.connect(con_string)
            return conn
        except pyodbc.Error as e:
            print(f'Error: {e}')
            return None

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_auto(self):
        janela = self.root

        # Frame lateral com botões
        frame_menu_lateral = ctk.CTkFrame(janela, width=150, fg_color=self.my_dict['menu-inf'], bg_color=self.my_dict['preto'])
        frame_menu_lateral.pack(side='left', fill='y')

        # Frame principal que mudará de acordo com os botões
        self.frame_tela = ctk.CTkFrame(janela, fg_color=self.my_dict['preto'], bg_color=self.my_dict['preto'])
        self.frame_tela.pack(side='left', fill='both', expand=True)

        # Adicionar ComboBoxes ao frame lateral
        self.add_comboboxes(frame_menu_lateral)
        
        # Adicionar botões ao frame lateral
        self.add_buttons_menu(frame_menu_lateral)
        
        # Mostrar a mensagem inicial solicitando a seleção de um site e empresa
        self.show_initial_message()

    def add_comboboxes(self, frame):
        # ComboBox para os sites
        sites = self.get_sites()
        self.combo_sites = ttk.Combobox(frame, values=sites)
        self.combo_sites.pack(pady=10, padx=10, fill='x')
        self.combo_sites.bind("<<ComboboxSelected>>", self.on_site_selected)

        # ComboBox para as empresas (inicia vazia)
        self.combo_empresas = ttk.Combobox(frame, values=[])
        self.combo_empresas.pack(pady=10, padx=10, fill='x')
        self.combo_empresas.bind("<<ComboboxSelected>>", self.on_empresa_selected)

    def get_sites(self):
        if self.conn is None:
            return []

        cursor = self.conn.cursor()
        cursor.execute("SELECT Sites FROM SITE")
        sites = [row[0] for row in cursor.fetchall()]
        return sites

    def get_empresas(self, site):
        if self.conn is None or not site:
            return []

        cursor = self.conn.cursor()
        query = """
            SELECT EMPRESA.Empresas 
            FROM SITE_EMPRESA 
            INNER JOIN SITE ON SITE_EMPRESA.ID_Sites = SITE.ID_Site 
            INNER JOIN EMPRESA ON SITE_EMPRESA.ID_Empresas = EMPRESA.ID_Empresa
            WHERE SITE.Sites = ?
        """
        cursor.execute(query, (site,))
        empresas = [row[0] for row in cursor.fetchall()]
        return empresas


    def on_site_selected(self, event):
        self.selected_site = self.combo_sites.get()
        print(f'Site selecionado: {self.selected_site}')

        # Atualiza a ComboBox de empresas com base no site selecionado
        empresas = self.get_empresas(self.selected_site)
        self.combo_empresas['values'] = empresas
        self.combo_empresas.set('')  # Reseta a seleção de empresas
        self.selected_empresa = None

    def on_empresa_selected(self, event):
        self.selected_empresa = self.combo_empresas.get()
        print(f'Empresa selecionada: {self.selected_empresa}')

        # Agora você pode carregar a aba de controle após a seleção da empresa
        if self.selected_empresa:
            self.show_frame("Controle de Frequencia")

    def add_buttons_menu(self, frame):
        button_texts = ["Controle de Frequencia", "Inserir Nomes", "Relatorio Mensal"]

        for text in button_texts:
            button = ctk.CTkButton(frame, text=text, command=lambda t=text: self.show_frame(t), hover_color=self.my_dict['hover'], border_width=2, border_color=self.my_dict['borda'])
            button.pack(pady=10, padx=10, fill='x')
            self.buttons[text] = button  # Armazena o botão no dicionário

    def show_initial_message(self):
        # Exibe uma mensagem inicial solicitando que o usuário selecione um site e uma empresa
        label = ctk.CTkLabel(self.frame_tela, text="Por favor, selecione um site e uma empresa no menu à esquerda.", text_color=self.my_dict['font'])
        label.pack(pady=20)

    def show_frame(self, frame_name):
        # Limpa o frame atual
        for widget in self.frame_tela.winfo_children():
            widget.destroy()
        
        # Atualiza a cor dos botões
        for name, button in self.buttons.items():
            if name == frame_name:
                button.configure(fg_color=self.my_dict['selecionado'], border_color=self.my_dict['selecionado'])
            else:
                button.configure(fg_color='transparent', border_color=self.my_dict['borda'])

        # Adiciona novo conteúdo baseado no botão pressionado
        if frame_name == "Controle de Frequencia":
            if self.selected_site and self.selected_empresa:
                Aba_Controle(self, self.frame_tela, self.my_dict, self.conn, self.selected_site, self.selected_empresa)
            else:
                self.show_initial_message()  # Volta a mostrar a mensagem caso nenhum site ou empresa esteja selecionado
        elif frame_name == "Inserir Nomes":
            if self.selected_site and self.selected_empresa:
                Aba_adiciona_remove_nomes(self, self.frame_tela, self.my_dict, self.conn, self.selected_site, self.selected_empresa)
            else:
                self.show_initial_message()
        elif frame_name == "Relatorio Mensal":
            if self.selected_site and self.selected_empresa:
                Aba_relatorio_mes(self, self.frame_tela, self.my_dict, self.conn, self.selected_site, self.selected_empresa)
            else:
                self.show_initial_message()

# Exemplo de como passar o selected_site e selected_empresa para as outras classes/abas
class Aba_Controle:
    def __init__(self, app, frame, my_dict, conn, selected_site, selected_empresa):
        self.app = app
        self.frame = frame
        self.my_dict = my_dict
        self.conn = conn
        self.selected_site = selected_site
        self.selected_empresa = selected_empresa
        self.setup()

    def setup(self):
        # Exemplo de uso do selected_site e selected_empresa
        label = ctk.CTkLabel(self.frame, text=f"Controle de Frequência para o site: {self.selected_site}, Empresa: {self.selected_empresa}", text_color=self.my_dict['font'])
        label.pack(pady=20)

# O mesmo pode ser feito para as outras classes de abas
class Aba_adiciona_remove_nomes:
    def __init__(self, app, frame, my_dict, conn, selected_site, selected_empresa):
        self.app = app
        self.frame = frame
        self.my_dict = my_dict
        self.conn = conn
        self.selected_site = selected_site
        self.selected_empresa = selected_empresa
        self.setup()

    def setup(self):
        label = ctk.CTkLabel(self.frame, text=f"Inserir Nomes para o site: {self.selected_site}, Empresa: {self.selected_empresa}", text_color=self.my_dict['font'])
        label.pack(pady=20)

class Aba_relatorio_mes:
    def __init__(self, app, frame, my_dict, conn, selected_site, selected_empresa):
        self.app = app
        self.frame = frame
        self.my_dict = my_dict
        self.conn = conn
        self.selected_site = selected_site
        self.selected_empresa = selected_empresa
        self.setup()

    def setup(self):
        label = ctk.CTkLabel(self.frame, text=f"Relatório Mensal para o site: {self.selected_site}, Empresa: {self.selected_empresa}", text_color=self.my_dict['font'])
        label.pack(pady=20)

# Para rodar o app:
if __name__ == "__main__":
    root = ctk.CTk()
    app = ControleApp(root)
    root.mainloop()
