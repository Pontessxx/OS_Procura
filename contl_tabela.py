import customtkinter as ctk
import datetime
import pyodbc
from tkinter import ttk


import calendar

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
            'hover_treeview':'#cc092f',
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
            Aba_relatorio(self, self.frame_tela, self.my_dict, self.conn, self.meses_dict)
    

class Aba_Controle:
    def __init__(self, parent, master, my_dict, conn, meses_dict):
        self.parent = parent  # Referência para a instância da classe pai
        self.style_treeview = ttk.Style()
        self.filter_mode = False
        self.conn = conn  # Conexão com o banco de dados
        self.meses_dict = meses_dict  # Dicionário de meses
        self.frame = ctk.CTkFrame(master, fg_color=my_dict['preto'])
        self.frame.pack(fill='both', expand=True)
        
        label = ctk.CTkLabel(self.frame, text="CONTROLE DE FREQUENCIA", text_color=my_dict['font'])
        label.pack(pady=5, padx=5)
        
        self.frame_checkbox = ctk.CTkFrame(self.frame, fg_color=my_dict['preto'],height=50)
        self.frame_checkbox.pack(pady=10, padx=10, fill='x')

        # Adicionar checkboxes
        self.add_checkboxes()

        combobox_frame = ctk.CTkFrame(self.frame, fg_color=my_dict['preto'])
        combobox_frame.pack(pady=10, padx=10, fill='x')

        # tipo presenca
        tipo_presenca_label = ctk.CTkLabel(combobox_frame, text="Presença :", text_color=my_dict['font'])
        tipo_presenca_label.grid(row=0, column=1, padx=10, pady=5)
        self.tipo_presenca_combobox = ctk.CTkComboBox(combobox_frame, values=self.get_presenca(), state='readonly')
        self.tipo_presenca_combobox.grid(row=0, column=2, padx=10, pady=5)
       
        # Dia
        dias = [str(i) for i in range(1, 32)]

        dia_label = ctk.CTkLabel(combobox_frame, text="Dia :", text_color=my_dict['font'])
        dia_label.grid(row=0, column=3, padx=10, pady=5)
        self.dia_combobox = ctk.CTkComboBox(combobox_frame, values=dias, state='readonly')
        self.dia_combobox.grid(row=0, column=4, padx=10, pady=5)

        # Mês
        mes_label = ctk.CTkLabel(combobox_frame, text="Mês :", text_color=my_dict['font'])
        mes_label.grid(row=0, column=5, padx=10, pady=5)
        self.mes_combobox = ctk.CTkComboBox(combobox_frame, values=list(self.meses_dict.values()), state='readonly')
        self.mes_combobox.grid(row=0, column=6, padx=10, pady=5)
        mes_atual = datetime.datetime.now().month
        self.mes_combobox.set(self.meses_dict[mes_atual])

        # Ano
        ano_atual = datetime.datetime.now().year
        ano_inicial = 2024
        anos = [str(a) for a in range(ano_inicial, ano_atual + 100)]
        
        ano_label = ctk.CTkLabel(combobox_frame, text="Ano :", text_color=my_dict['font'])
        ano_label.grid(row=0, column=7, padx=10, pady=5)
        self.ano_combobox = ctk.CTkComboBox(combobox_frame, values=anos, state='readonly')
        self.ano_combobox.grid(row=0, column=8, padx=10, pady=5)
        self.ano_combobox.set(str(ano_atual))

        button = ctk.CTkButton(combobox_frame, text="Adicionar", width=75, height=30, command=self.adicionar_frequencia)
        button.grid(row=0, column=9, padx=10, pady=5)
        button = ctk.CTkButton(combobox_frame, text="Deletar", width=75, height=30, command=self.remover_frequencia)
        button.grid(row=0, column=10, padx=10, pady=5)
        self.filter_button = ctk.CTkButton(combobox_frame, text="Filtrar", width=50, height=30, command=self.toggle_filter)
        self.filter_button.grid(row=0, column=11, padx=5, pady=5)

        # Tabela (Treeview)
        tabela_frame = ctk.CTkFrame(self.frame, fg_color=my_dict['preto'])
        tabela_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.tabela = ttk.Treeview(tabela_frame, columns=("Data", "Nome", "Presença"), show='headings',)
        self.style_treeview.theme_use('clam')
        #configurando a cor da treeview para ajustar ao tema
        self.style_treeview.configure("Treeview.Heading", background=my_dict['preto'], foreground=my_dict['font'], borderwidth=1, relief='solid', font=('Arial', 10))
        self.style_treeview.map("Treeview.Heading", background=[('active', my_dict['hover_treeview'])])

        self.style_treeview.configure("Treeview", background=my_dict['preto'], foreground=my_dict['font'], fieldbackground=my_dict['preto'], rowheight=25, borderwidth=1, relief='solid')
        self.style_treeview.map("Treeview", background=[('selected', my_dict['hover_treeview'])], fieldbackground=[('!selected', my_dict['preto'])])
        
        self.tabela.heading("Data", text="Data", command=lambda: self.ordenar_dados("Data", False))
        self.tabela.heading("Nome", text="Nome", command=lambda: self.ordenar_dados("Nome", False))
        self.tabela.heading("Presença", text="Presença", command=lambda: self.ordenar_dados("Presença", False))
        self.tabela.pack(fill='both', expand=True)

        self.tabela.bind("<ButtonRelease-1>", self.linha_selecionada_treeview)

        self.carregar_dados()

    def add_checkboxes(self):
        nomes = self.get_nomes()
        self.checkbox_vars = {}  # Dicionário para armazenar as variáveis das checkboxes
        row, col = 0, 0
        max_columns = 11  # Defina o número máximo de colunas por linha

        for nome in nomes:
            var = ctk.StringVar(value='off')
            checkbox = ctk.CTkCheckBox(self.frame_checkbox, text=nome, variable=var, onvalue='on', offvalue='off', font=('Arial', 15))
            checkbox.grid(row=row, column=col, padx=5, pady=5)
            self.checkbox_vars[nome] = var  # Armazena a variável da checkbox
            col += 1

            if col >= max_columns:
                col = 0
                row += 1

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

    def carregar_dados(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM tblControle")
            self.tabela.delete(*self.tabela.get_children())  # Limpa a tabela antes de carregar novos dados
            for row in cursor.fetchall():
                id, data, status, nome = row
                data_formatada = data.strftime('%d/%m/%Y')
                self.tabela.insert("", "end", values=[data_formatada, nome, status])
        except pyodbc.Error as e:
            print(f'Error: {e}')

    def adicionar_frequencia(self):
        tipo_presenca = self.tipo_presenca_combobox.get()
        dia = self.dia_combobox.get()
        mes = list(self.meses_dict.keys())[list(self.meses_dict.values()).index(self.mes_combobox.get())]
        ano = self.ano_combobox.get()

        data = datetime.datetime(int(ano), int(mes), int(dia))

        if tipo_presenca and dia and mes and ano:
            try:
                cursor = self.conn.cursor()
                for nome, var in self.checkbox_vars.items():
                    if var.get() == 'on':
                        cursor.execute("SELECT ID FROM tblControle WHERE Nomes=? AND DATA=?", (nome, data))
                        result = cursor.fetchone()
                        
                        if result:  # Se o registro existir, atualize-o
                            cursor.execute("UPDATE tblControle SET PRESENCA=? WHERE ID=?", (tipo_presenca, result[0]))
                        else:  # Se o registro não existir, insira um novo
                            cursor.execute("SELECT MAX(ID) FROM tblControle")
                            last_id = cursor.fetchone()[0]
                            if last_id is None:
                                last_id = 0
                            new_id = last_id + 1

                            cursor.execute("INSERT INTO tblControle (ID, DATA, NOMES, PRESENCA) VALUES (?, ?, ?, ?)", (new_id, data, nome, tipo_presenca))

                self.conn.commit()
                self.carregar_dados()
            except pyodbc.Error as e:
                print(f'Error: {e}')

    def remover_frequencia(self):
            dia = self.dia_combobox.get()
            mes = list(self.meses_dict.keys())[list(self.meses_dict.values()).index(self.mes_combobox.get())]
            ano = self.ano_combobox.get()

            data = datetime.datetime(int(ano), int(mes), int(dia))

            if dia and mes and ano:
                try:
                    cursor = self.conn.cursor()
                    for nome, var in self.checkbox_vars.items():
                        if var.get() == 'on':
                            cursor.execute("DELETE FROM tblControle WHERE Nomes=? AND DATA=?", (nome, data))
                    
                    self.dia_combobox.set('')
                    self.tipo_presenca_combobox.set('')
                    self.conn.commit()
                    self.carregar_dados()
                except pyodbc.Error as e:
                    print(f'Error: {e}')

    def toggle_filter(self):
        if self.filter_mode:
            self.limpar_filtro()
        else:
            self.filtrar_dados()

    def linha_selecionada_treeview(self, event):
        for selected_item in self.tabela.selection():
            item = self.tabela.item(selected_item)
            record = item['values']
            # print(f"Item selecionado: {record}")
            
            data_formatada, nome, tipo_presenca = record
            dia, mes, ano = data_formatada.split('/')
            # Remover zero à esquerda do dia
            if dia.startswith('0'):
                dia = dia[1:]
            self.dia_combobox.set(dia)
            # self.mes_combobox.set(self.meses_dict[int(mes)])
            # self.ano_combobox.set(ano)
            # self.tipo_presenca_combobox.set(tipo_presenca)
            
            # Atualizar checkboxes
            """ for nome_chk, var in self.checkbox_vars.items():
                if nome_chk == nome:
                    var.set('on')
                else:
                    var.set('off') """

    def filtrar_dados(self):
        dia = self.dia_combobox.get()
        mes = self.mes_combobox.get()
        ano = self.ano_combobox.get()
        tipo_presenca = self.tipo_presenca_combobox.get()
        nomes_selecionados = [nome for nome, var in self.checkbox_vars.items() if var.get() == 'on']

        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM tblControle WHERE 1=1"
            params = []

            if dia:
                query += " AND DAY(DATA)=?"
                params.append(dia)
            if mes:
                query += " AND MONTH(DATA)=?"
                params.append(list(self.meses_dict.keys())[list(self.meses_dict.values()).index(mes)])
            if ano:
                query += " AND YEAR(DATA)=?"
                params.append(ano)
            if tipo_presenca:
                query += " AND PRESENCA=?"
                params.append(tipo_presenca)
            if nomes_selecionados:
                query += " AND NOMES IN ({})".format(','.join(['?']*len(nomes_selecionados)))
                params.extend(nomes_selecionados)

            cursor.execute(query, params)
            
            self.tabela.delete(*self.tabela.get_children())  # Limpa a tabela antes de carregar novos dados
            for row in cursor.fetchall():
                id, data, status, nome = row
                data_formatada = data.strftime('%d/%m/%Y')
                self.tabela.insert("", "end", values=[data_formatada, nome, status])

            self.filter_button.configure(text="Limpar Filtro")
            self.filter_mode = True
        except pyodbc.Error as e:
            print(f'Error: {e}')

    def limpar_filtro(self):
        self.carregar_dados()
        self.dia_combobox.set('')
        self.tipo_presenca_combobox.set('')
        self.filter_button.configure(text="Filtrar")
        self.filter_mode = False
        # Limpar as checkboxes
        for nome, var in self.checkbox_vars.items():
            var.set('off')

    def ordenar_dados(self, coluna, reverse):
        try:
            dados = [(self.tabela.set(k, coluna), k) for k in self.tabela.get_children('')]
            dados.sort(reverse=reverse)

            for index, (val, k) in enumerate(dados):
                self.tabela.move(k, '', index)
            self.tabela.heading(coluna, command=lambda: self.ordenar_dados(coluna, not reverse))
        except Exception as e:
            print(f"Error: {e}")

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
                self.nome_combobox.set('')
            except pyodbc.Error as e:
                print(f'Error: {e}')


class Aba_relatorio:
    def __init__(self, parent, master, my_dict, conn,meses_dict):
        self.parent = parent  # Referência para a instância da classe pai
        self.conn = conn  # Conexão com o banco de dados
        self.frame = ctk.CTkFrame(master, fg_color=my_dict['preto'])
        self.frame.pack(fill='both', expand=True)

        self.meses_dict = meses_dict  # Dicionário de meses
        label = ctk.CTkLabel(self.frame, text="ABA DE RELATORIO", text_color=my_dict['font'])
        label.pack(pady=20, padx=20)

        filtro_frame = ctk.CTkFrame(self.frame, width=160, fg_color=my_dict['menu-inf'], bg_color=my_dict['preto'])
        filtro_frame.pack(padx=20,pady=20,side='left', fill='y')
        self.frame_checkbox = ctk.CTkFrame(self.frame, fg_color=my_dict['preto'],height=50)
        self.frame_checkbox.pack(pady=10, padx=10, fill='x')
         # Adicionar checkboxes

        # Mês
        mes_label = ctk.CTkLabel(filtro_frame, text="Mês :", text_color=my_dict['font'])
        mes_label.grid(row=0, column=5, padx=10, pady=5)
        self.mes_combobox = ctk.CTkComboBox(filtro_frame, values=list(self.meses_dict.values()), state='readonly')
        self.mes_combobox.grid(row=0, column=6, padx=10, pady=5)
        mes_atual = datetime.datetime.now().month
        self.mes_combobox.set(self.meses_dict[mes_atual])
        self.add_checkboxes()

    def add_checkboxes(self):
        nomes = self.get_nomes()
        self.checkbox_vars = {}  # Dicionário para armazenar as variáveis das checkboxes
        row, col = 0, 0
        max_columns = 11  # Defina o número máximo de colunas por linha

        for nome in nomes:
            var = ctk.StringVar(value='off')
            checkbox = ctk.CTkCheckBox(self.frame_checkbox, text=nome, variable=var, onvalue='on', offvalue='off', font=('Arial', 11))
            checkbox.grid(row=row, column=col, padx=5, pady=5)
            self.checkbox_vars[nome] = var  # Armazena a variável da checkbox
            col += 1

            if col >= max_columns:
                col = 0
                row += 1

    def get_nomes(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT Nomes FROM tblNomes")
            nomes = [row[0] for row in cursor.fetchall()]
            return nomes
        except pyodbc.Error as e:
            print(f'Error: {e}')
            return []
       

if __name__ == '__main__':
    root = ctk.CTk()
    app = ControleApp(root)
    root.mainloop()