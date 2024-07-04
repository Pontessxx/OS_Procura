import customtkinter as ctk
import datetime
import pyodbc

class ControleApp:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode('dark')
        root.geometry('1100x600')
        root.title('Busca de arquivos')
        root.minsize(1100, 600)

        self.center_window(1100, 600)  # Centraliza a janela

        self.my_dict = {
            'font': '#c2c2c2',
            'preto': '#111',
            'frames_ajuste': '#666',
            'hover': '#111',
            'selecionado': '#111',  
            'menu-sup': '#333',
            'menu-inf': '#222',
            'borda': '#a3a3a3',
            'adicionar_btn': 'green',
            'remover_btn': 'red',
        }

        self.meses_dict = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }

        self.buttons = {}  # Dicionário para armazenar os botões
        self.conn = self.connect_to_db()  # Conectar ao banco de dados
        self.setup_auto()

    def connect_to_db(self):
        try: 
            con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Henrique\OneDrive\Anexos\FIAP_2024\OS_Procura\ControleDataBase.accdb'
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
        frame_menu_inferior = ctk.CTkFrame(janela, width=150, fg_color=self.my_dict['menu-inf'], bg_color=self.my_dict['preto'])
        frame_menu_inferior.pack(side='left', fill='y')

        # Frame principal que mudará de acordo com os botões
        self.frame_tela = ctk.CTkFrame(janela, fg_color=self.my_dict['preto'], bg_color=self.my_dict['preto'])
        self.frame_tela.pack(side='left', fill='both', expand=True)

        # Adicionar botões ao frame lateral
        self.add_buttons_menu(frame_menu_inferior)

        # Abrir Controle de Frequencia por padrão
        self.show_frame("Controle de Frequencia")

    def add_buttons_menu(self, frame):
        button_texts = ["Controle de Frequencia", "Inserir Nomes", "Relatorio"]

        for text in button_texts:
            button = ctk.CTkButton(frame, text=text, command=lambda t=text: self.show_frame(t), hover_color=self.my_dict['hover'], border_width=2, border_color=self.my_dict['borda'])
            button.pack(pady=10, padx=10, fill='x')
            self.buttons[text] = button  # Armazena o botão no dicionário

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
            Aba_Controle(self, self.frame_tela, self.my_dict, self.conn, self.meses_dict)
        elif frame_name == "Inserir Nomes":
            Aba_adiciona_remove_nomes(self, self.frame_tela, self.my_dict, self.conn)
        elif frame_name == "Relatorio":
            Aba_relatorio(self, self.frame_tela, self.my_dict, self.conn)
    

class Aba_Controle:
    def __init__(self, parent, master, my_dict, conn, meses_dict):
        self.parent = parent  # Referência para a instância da classe pai
        self.conn = conn  # Conexão com o banco de dados
        self.meses_dict = meses_dict  # Dicionário de meses
        self.frame = ctk.CTkFrame(master, fg_color=my_dict['preto'])
        self.frame.pack(fill='both', expand=True)
        
        label = ctk.CTkLabel(self.frame, text="CONTROLE DE FREQUENCIA", text_color=my_dict['font'])
        label.pack(pady=5, padx=5)
        
        combobox_frame = ctk.CTkFrame(self.frame, fg_color=my_dict['frames_ajuste'])
        combobox_frame.pack(pady=10, padx=10, fill='y',side='left')

        # Nome
        nome_label = ctk.CTkLabel(combobox_frame, text="Nome :", text_color=my_dict['font'])
        nome_label.grid(row=0, column=0, padx=5, pady=5)
        # for i in range(len(self.get_nomes())):
        #     nomes = self.get_nomes()
        #     nome_combobox = ctk.CTkCheckBox(combobox_frame, text=nomes[i])
        #     nome_combobox.grid(row=0, column=i, padx=5, pady=5)
        self.nome_combobox = ctk.CTkComboBox(combobox_frame, values=self.get_nomes(), state='readonly')
        self.nome_combobox.grid(row=1, column=0, padx=5, pady=5)

        # tipo presenca
        tipo_presenca_label = ctk.CTkLabel(combobox_frame, text="Presença :", text_color=my_dict['font'])
        tipo_presenca_label.grid(row=2, column=0, padx=5, pady=5)
        tipo_presenca_combobox = ctk.CTkComboBox(combobox_frame, values=self.get_presenca(), state='readonly')
        tipo_presenca_combobox.grid(row=3, column=0, padx=5, pady=5)
       
        # Dia
        dias = [str(i) for i in range(1, 32)]

        dia_label = ctk.CTkLabel(combobox_frame, text="Dia :", text_color=my_dict['font'])
        dia_label.grid(row=4, column=0, padx=5, pady=5)
        dia_combobox = ctk.CTkComboBox(combobox_frame, values=dias, state='readonly')
        dia_combobox.grid(row=5, column=0, padx=5, pady=5)

        # Mês
        mes_label = ctk.CTkLabel(combobox_frame, text="Mês :", text_color=my_dict['font'])
        mes_label.grid(row=6, column=0, padx=5, pady=5)
        mes_combobox = ctk.CTkComboBox(combobox_frame, values=list(self.meses_dict.values()), state='readonly')
        mes_combobox.grid(row=7, column=0, padx=5, pady=5)
        mes_atual = datetime.datetime.now().month
        mes_combobox.set(self.meses_dict[mes_atual])

        # Ano
        ano_atual = datetime.datetime.now().year
        anos = [str(a) for a in range(ano_atual, ano_atual + 100)]
        
        ano_label = ctk.CTkLabel(combobox_frame, text="Ano :", text_color=my_dict['font'])
        ano_label.grid(row=8, column=0, padx=5, pady=5)
        ano_combobox = ctk.CTkComboBox(combobox_frame, values=anos, state='readonly')
        ano_combobox.grid(row=9, column=0, padx=5, pady=5)
        ano_combobox.set(str(ano_atual))

        button = ctk.CTkButton(combobox_frame, text="Adicionar", width=200, height=60)
        button.grid(row=10, column=0, padx=5, pady=5, rowspan=2)

        # # Tabview
        # tabela_frame = ctk.CTkFrame(self.frame,fg_color=my_dict['preto'])
        # tabela_frame.pack(pady=10, padx=10, fill='both', expand=True)

    def get_nomes(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT Nomes FROM tblNomes")
            nomes = [row[0] for row in cursor.fetchall()]
            return nomes
        except pyodbc.Error as e:
            print(f'Error: {e}')
            return []
        
    def get_presenca(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT PRESENCA FROM tblTipoFrequencia")
            presenca = [row[0] for row in cursor.fetchall()]
            return presenca
        except pyodbc.Error as e:
            print(f'Error: {e}')
            return []


class Aba_adiciona_remove_nomes:
    def __init__(self, parent, master, my_dict, conn):
        self.parent = parent  # Referência para a instância da classe pai
        self.conn = conn  # Conexão com o banco de dados
        self.frame = ctk.CTkFrame(master, fg_color=my_dict['preto'])
        self.frame.pack(fill='both', expand=True)
    
        label = ctk.CTkLabel(self.frame, text="INSERIR OU REMOVER NOME", text_color=my_dict['font'])
        label.pack(pady=5, padx=5)
        
        frame_superior = ctk.CTkFrame(self.frame, fg_color=my_dict['preto'])
        frame_superior.pack(pady=10, padx=10, fill='x')

        nome_label = ctk.CTkLabel(frame_superior, text="Inserir Nome :", text_color=my_dict['font'])
        nome_label.grid(row=0, column=0, padx=5, pady=5)

        self.nome_entry = ctk.CTkEntry(frame_superior, fg_color=my_dict['font'])
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)
        
        button_add = ctk.CTkButton(frame_superior, text="Adicionar", fg_color=my_dict['adicionar_btn'], command=self.adicionar_nome)
        button_add.grid(row=0, column=2, padx=5, pady=5)
        
        nome_label2 = ctk.CTkLabel(frame_superior, text="Remover Nome :", text_color=my_dict['font'])
        nome_label2.grid(row=1, column=0, padx=5, pady=5)
        self.nome_combobox = ctk.CTkComboBox(frame_superior, values=self.get_nomes(), state='readonly')
        self.nome_combobox.grid(row=1, column=1, padx=5, pady=5)
        
        button_remove = ctk.CTkButton(frame_superior, text="Remover", fg_color=my_dict['remover_btn'], command=self.remover_nome)
        button_remove.grid(row=1, column=2, padx=5, pady=5)

    def get_nomes(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT Nomes FROM tblNomes")
            nomes = [row[0] for row in cursor.fetchall()]
            return nomes
        except pyodbc.Error as e:
            print(f'Error: {e}')
            return []

    def adicionar_nome(self):
        nome = self.nome_entry.get()
        if nome:
            try:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO tblNomes (Nomes) VALUES (?)", (nome,))
                self.conn.commit()
                self.nome_combobox.configure(values=self.get_nomes())
                self.nome_entry.delete(0, 'end')
            except pyodbc.Error as e:
                print(f'Error: {e}')

    def remover_nome(self):
        nome = self.nome_combobox.get()
        if nome:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM tblNomes WHERE Nomes = ?", (nome,))
                self.conn.commit()
                self.nome_combobox.configure(values=self.get_nomes())
            except pyodbc.Error as e:
                print(f'Error: {e}')


class Aba_relatorio:
    def __init__(self, parent, master, my_dict, conn):
        self.parent = parent  # Referência para a instância da classe pai
        self.conn = conn  # Conexão com o banco de dados
        self.frame = ctk.CTkFrame(master, fg_color=my_dict['preto'])
        self.frame.pack(fill='both', expand=True)
        label = ctk.CTkLabel(self.frame, text="ABA DE RELATORIO", text_color=my_dict['font'])
        label.pack(pady=20, padx=20)

       

if __name__ == '__main__':
    root = ctk.CTk()
    app = ControleApp(root)
    root.mainloop()
