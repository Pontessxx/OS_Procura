import customtkinter as ctk
import datetime
import pyodbc
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from tkinter import messagebox
import calendar
import os
import subprocess
class ControleApp:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('C:\\Users\\Henrique\\OneDrive\\Anexos\\FIAP_2024\\OS_Procura\\Busca_os\\img\\bradimg.ico')
        ctk.set_appearance_mode('dark')
        root.geometry('1130x600')
        # root.eval('tk::PlaceWindow . center')
        root.title('Busca de arquivos')
        root.minsize(1130, 600)
        # root.state('zoomed')
        self.center_window(1100, 600)  # Centraliza a janela

        self.my_dict = {
            'font': '#c2c2c2',
            'Heading_color':'#434343' ,
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
        frame_menu_lateral = ctk.CTkFrame(janela, width=150, fg_color=self.my_dict['menu-inf'], bg_color=self.my_dict['preto'])
        frame_menu_lateral.pack(side='left', fill='y')

        # Frame principal que mudará de acordo com os botões
        self.frame_tela = ctk.CTkFrame(janela, fg_color=self.my_dict['preto'], bg_color=self.my_dict['preto'])
        self.frame_tela.pack(side='left', fill='both', expand=True)

        # Adicionar botões ao frame lateral
        self.add_buttons_menu(frame_menu_lateral)
        
        # Abrir Controle de Frequencia por padrão
        self.show_frame("Controle de Frequencia")

    def add_buttons_menu(self, frame):
        button_texts = ["Controle de Frequencia", "Inserir Nomes", "Relatorio Mensal"]

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
        elif frame_name == "Relatorio Mensal":
            Aba_relatorio_mes(self, self.frame_tela, self.my_dict, self.conn, self.meses_dict)
    

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

        combobox_frame = ctk.CTkFrame(self.frame, fg_color=my_dict['preto'],)
        combobox_frame.pack(pady=10, padx=10, fill='x')

        # tipo presenca
        tipo_presenca_label = ctk.CTkLabel(combobox_frame, text="Presença :", text_color=my_dict['font'])
        tipo_presenca_label.grid(row=0, column=1, padx=5, pady=5)
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
        

        # spacer = ctk.CTkLabel(combobox_frame, text='')
        # spacer.grid(padx=20,row=0, column=9)

        button = ctk.CTkButton(combobox_frame, text="Adicionar", width=55, height=30, command=self.adicionar_frequencia)
        button.grid(row=0, column=10, padx=10, pady=5)
        button = ctk.CTkButton(combobox_frame, text="Deletar", width=55, height=30, command=self.remover_frequencia)
        button.grid(row=0, column=11, padx=10, pady=5)
        spacer = ctk.CTkLabel(combobox_frame, text='')
        spacer.grid(padx=0,row=0, column=12)
        self.filter_button = ctk.CTkButton(combobox_frame, text="Filtrar", width=55, height=30, command=self.toggle_filter)
        self.filter_button.grid(row=0, column=13, padx=5, pady=5)

        # Tabela (Treeview)
        tabela_frame = ctk.CTkFrame(self.frame, fg_color=my_dict['preto'])
        tabela_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.tabela = ttk.Treeview(tabela_frame, columns=("Data", "Nome", "Presença"), show='headings',)
        self.style_treeview.theme_use('alt')

        # scrollbar
        self.treeScrollbar = ctk.CTkScrollbar(tabela_frame,command=self.tabela.yview,)
        self.tabela.configure(yscrollcommand=self.treeScrollbar.set, )
        self.treeScrollbar.pack(side='right', fill='y',)

        #configurando a cor da treeview para ajustar ao tema
        self.style_treeview.configure("Treeview.Heading", background=my_dict['Heading_color'], foreground=my_dict['font'], borderwidth=1, relief='solid', font=('Arial', 12),bordercolor=my_dict['Heading_color'])
        self.style_treeview.map("Treeview.Heading", background=[('active', my_dict['hover_treeview'])])

        self.style_treeview.configure("Treeview", background=my_dict['preto'], foreground=my_dict['font'], fieldbackground=my_dict['preto'], rowheight=25, borderwidth=1, relief='solid',bordercolor=my_dict['preto'])
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
        max_columns = 9  # Defina o número máximo de colunas por linha

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

        # Verifica se a data cai em um sábado ou domingo
        dia_da_semana = calendar.weekday(int(ano), int(mes), int(dia))
        if dia_da_semana == 5 or dia_da_semana == 6:
            messagebox.showerror("Erro", "A data selecionada cai em um sábado ou domingo. Por favor, selecione um dia útil.")
            return

        if tipo_presenca and dia and mes and ano:
            try:
                cursor = self.conn.cursor()
                for nome, var in self.checkbox_vars.items():
                    if var.get() == 'on':
                        cursor.execute("SELECT ID FROM tblControle WHERE NOMES=? AND DATA=?", (nome, data))
                        result = cursor.fetchone()
                        
                        if result:  # Se o registro existir, pergunte se deseja atualizar
                            resposta = messagebox.askquestion(title="Dados já existentes", message=f"nome: {nome}\n data: {data.strftime('%d/%m/%Y')}")
                            if resposta == 'yes':
                                cursor.execute("UPDATE tblControle SET PRESENCA=? WHERE ID=?", (tipo_presenca, result[0]))
                                self.conn.commit()  # Comita a atualização
                        else:  # Se o registro não existir, insira um novo
                            cursor.execute("SELECT MAX(ID) FROM tblControle")
                            last_id = cursor.fetchone()[0]
                            if last_id is None:
                                last_id = 0
                            new_id = last_id + 1
                            cursor.execute("INSERT INTO tblControle (ID, DATA, NOMES, PRESENCA) VALUES (?, ?, ?, ?)", (new_id, data, nome, tipo_presenca))
                            self.conn.commit()  # Comita a inserção
                        
                        # Resetar a checkbox após processar o nome
                        var.set('off')

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
                # Verifica se pelo menos uma checkbox está selecionada
                if any(var.get() == 'on' for var in self.checkbox_vars.values()):
                    resposta = messagebox.askquestion(title="Deletar Controle", message=f"deletar presença: {data.strftime('%d/%m/%Y')}")
                    if resposta=='yes':
                        for nome, var in self.checkbox_vars.items():
                            if var.get() == 'on':
                                cursor.execute("DELETE FROM tblControle WHERE Nomes=? AND DATA=?", (nome, data))
                        self.dia_combobox.set('')
                        self.tipo_presenca_combobox.set('')
                        self.conn.commit()
                        self.carregar_dados()
                else:
                    messagebox.showerror(title="Erro", message="Nenhum nome selecionado.")
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
            
            data_formatada, nome, tipo_presenca = record
            dia, mes, ano = data_formatada.split('/')
            # Remover zero à esquerda do dia
            dia = dia.lstrip('0')
            mes = mes.lstrip('0')
            self.dia_combobox.set(dia)
            
            # Converter a string do mês para um número inteiro
            mes_numero = int(mes)
            
            # Definir o combobox do mês com o valor correspondente ao mês
            if mes_numero in self.meses_dict:
                self.mes_combobox.set(self.meses_dict[mes_numero])
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
        self.parent = parent # Referência para a instância da classe pai
        self.conn = conn # Conexão com o banco de dados
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
        resposta = messagebox.askquestion(title="Aviso", message=f'Gostaria de apagar o {nome}, e seus dados ')
        if resposta == 'yes':
            if nome:
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("DELETE FROM tblNomes WHERE Nomes = ?", (nome,))
                    cursor.execute("DELETE FROM tblControle WHERE Nomes = ?", (nome,)) # Remover linhas da tblControle
                    self.conn.commit()
                    self.nome_combobox.configure(values=self.get_nomes())
                    self.nome_combobox.set('')
                except pyodbc.Error as e:
                    print(f'Error: {e}')
        


class Aba_relatorio_mes: 
    def __init__(self, parent, master, my_dict, conn, meses_dict):
        self.parent = parent # Referência para a instância da classe pai
        self.conn = conn # Conexão com o banco de dados
        self.style_treeview = ttk.Style()
        self.filter_mode = False

        self.frame_superior = ctk.CTkFrame(master, fg_color=my_dict['preto'])
        self.frame_superior.pack(fill='both', expand=True)


        filtro_frame = ctk.CTkFrame(self.frame_superior, width=160, fg_color=my_dict['menu-inf'], bg_color=my_dict['preto'])
        filtro_frame.pack(padx=20, pady=20, side='left', fill='y')

        filtro_frame_1 = ctk.CTkFrame(filtro_frame, width=100, fg_color=my_dict['menu-inf'])
        filtro_frame_1.pack(side='top', fill='y', expand=True)

        self.filtro_frame_2 = ctk.CTkFrame(filtro_frame, width=100, fg_color=my_dict['menu-inf'])
        self.filtro_frame_2.pack(side='bottom', fill='y', expand=True)

        self.meses_dict = meses_dict # Dicionário de meses

        self.frame_checkbox = ctk.CTkFrame(self.frame_superior, fg_color=my_dict['preto'], height=50)
        self.frame_checkbox.pack(pady=10, padx=10, fill='x')

        # Mês
        mes_label = ctk.CTkLabel(filtro_frame_1, text="Mês :", text_color=my_dict['font'])
        mes_label.grid(row=0, column=0, padx=10, pady=5)
        self.mes_combobox = ctk.CTkComboBox(filtro_frame_1, values=list(self.meses_dict.values()), state='readonly')
        self.mes_combobox.grid(row=0, column=1, padx=10, pady=5)
        mes_atual = datetime.datetime.now().month
        self.mes_combobox.set(self.meses_dict[mes_atual])

        # Ano
        ano_atual = datetime.datetime.now().year
        ano_inicial = 2024
        anos = [str(a) for a in range(ano_inicial, ano_atual + 100)]
        
        ano_label = ctk.CTkLabel(filtro_frame_1, text="Ano :", text_color=my_dict['font'])
        ano_label.grid(row=1, column=0, padx=10, pady=5)
        self.ano_combobox = ctk.CTkComboBox(filtro_frame_1, values=anos, state='readonly')
        self.ano_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.ano_combobox.set(str(ano_atual))

        # linha em branco
        spacer = ctk.CTkLabel(filtro_frame_1, text='')
        spacer.grid(row=3, column=0)

        self.button = ctk.CTkButton(filtro_frame_1, text="Filtrar", width=160, height=30, command=self.Filtrar_dados)
        self.button.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

        self.btn_gerar_graficos = ctk.CTkButton(filtro_frame_1, text="Mostrar Gráficos", width=160, height=30,command=self.abrir_janela_graficos)
        self.btn_gerar_graficos.grid(row=6, column=0, padx=10, pady=10, columnspan=2)
        label = ctk.CTkLabel(self.filtro_frame_2, text='TIPO DE PRESENÇA', text_color='#c2c2c2')
        label.grid(row=0, column=0, padx=10, pady=5, columnspan=4)

        self.add_checkboxes()

        tabela_frame = ctk.CTkFrame(self.frame_superior, fg_color=my_dict['preto'])
        tabela_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.tabela = ttk.Treeview(tabela_frame, columns=("Data", "Nome", "Presença"), show='headings')
        self.style_treeview.theme_use('alt')
        self.treeScrollbar = ctk.CTkScrollbar(tabela_frame,command=self.tabela.yview,)
        self.treeScrollbar.pack(side='right', fill='y',)
        self.tabela.configure(yscrollcommand=self.treeScrollbar.set, )

        self.style_treeview.configure("Treeview.Heading", background=my_dict['Heading_color'], foreground=my_dict['font'], borderwidth=1, relief='solid', font=('Arial', 12),bordercolor=my_dict['Heading_color'])
        self.style_treeview.map("Treeview.Heading", background=[('active', my_dict['hover_treeview'])])

        self.style_treeview.configure("Treeview",bordercolor=my_dict['preto'], background=my_dict['preto'], foreground=my_dict['font'], fieldbackground=my_dict['preto'], rowheight=25, borderwidth=1, relief='solid',)
        self.style_treeview.map("Treeview", background=[('selected', my_dict['hover_treeview'])], fieldbackground=[('!selected', my_dict['preto'])])
        
        self.tabela.heading("Data", text="Data")
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("Presença", text="Presença")
        self.tabela.pack(fill='both', expand=True)
        

    def add_checkboxes(self):
        nomes = self.get_nomes()
        self.checkbox_vars = {} # Dicionário para armazenar as variáveis das checkboxes
        row, col = 0, 0
        max_columns = 11 # Defina o número máximo de colunas por linha

        for nome in nomes:
            var = ctk.StringVar(value='off')
            checkbox = ctk.CTkCheckBox(self.frame_checkbox, text=nome, variable=var, onvalue='on', offvalue='off', font=('Arial', 11))
            checkbox.grid(row=row, column=col, padx=5, pady=5)
            self.checkbox_vars[nome] = var # Armazena a variável da checkbox
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

    
    def limpar_filtro(self):
        self.filter_mode = False
        self.button.configure(text='Filtrar')
        for widget in self.filtro_frame_2.winfo_children():
            widget.destroy()

    def Filtrar_dados(self):
        mes = list(self.meses_dict.keys())[list(self.meses_dict.values()).index(self.mes_combobox.get())]
        ano = self.ano_combobox.get()
        
        # Obter os nomes selecionados nas checkboxes
        nomes_selecionados = [nome for nome, var in self.checkbox_vars.items() if var.get() == 'on']
        
        try:
            cursor = self.conn.cursor()
            
            if nomes_selecionados:
                # Filtrar por mês, ano e nomes selecionados
                query = "SELECT DATA, NOMES, PRESENCA FROM tblControle WHERE MONTH(DATA)=? AND YEAR(DATA)=? AND NOMES IN ({})".format(','.join(['?']*len(nomes_selecionados)))
                params = [mes, ano] + nomes_selecionados
            else:
                # Filtrar apenas por mês e ano
                query = "SELECT DATA, NOMES, PRESENCA FROM tblControle WHERE MONTH(DATA)=? AND YEAR(DATA)=?"
                params = [mes, ano]
            
            cursor.execute(query, params)
            resultados = cursor.fetchall()

            # Atualiza a Treeview com os dados filtrados
            self.tabela.delete(*self.tabela.get_children())  # Limpa a tabela antes de carregar novos dados
            for row in resultados:
                data, nome, presenca = row
                data_formatada = data.strftime('%d/%m/%Y')
                self.tabela.insert("", "end", values=[data_formatada, nome, presenca])

            contagem = {}
            for resultado in resultados:
                presenca = resultado[2]
                if presenca in contagem:
                    contagem[presenca] += 1
                else:
                    contagem[presenca] = 1

            # Apagar as labels anteriores
            for widget in self.filtro_frame_2.winfo_children():
                widget.destroy()

            label = ctk.CTkLabel(self.filtro_frame_2, text='TIPO DE PRESENÇA', text_color='#c2c2c2')
            label.grid(row=0, column=0, padx=10, pady=5, columnspan=4)
            row = 1

            for tipo_presenca, quantidade in contagem.items():
                presenca_label = ctk.CTkLabel(self.filtro_frame_2, text=tipo_presenca, text_color='#c2c2c2')
                presenca_label.grid(row=row, column=0, padx=10, pady=5)
                quantidade_label = ctk.CTkLabel(self.filtro_frame_2, text=str(quantidade), text_color='#c2c2c2')
                quantidade_label.grid(row=row, column=2, padx=10, pady=5)
                row += 1


        except pyodbc.Error as e:
            print(f'Error: {e}')


    def abrir_janela_graficos(self):
        self.figura = plt.Figure(figsize=(15, 8))

        # Minimiza a janela principal
        self.parent.root.iconify()
        # Cria uma nova janela
        self.new_window = ctk.CTkToplevel(self.parent.root)
        
        # frame graficos
        self.frame_teste = ctk.CTkFrame(self.new_window, fg_color='#FFF')
        self.frame_teste.pack(pady=10, padx=10, fill='both', expand=True,side='left')
        self.frame_2 = ctk.CTkFrame(self.new_window, fg_color=self.parent.my_dict['frames_ajuste'])
        self.frame_2.pack(pady=10, padx=10, fill='both', expand=True,side='left')

        self.new_window.title(f"Gráficos - {self.mes_combobox.get()}")
        self.new_window.geometry("800x600")
        self.new_window.minsize(1120, 600)
        # expande a nova janela
        self.new_window.state('zoomed')
        
        # Adiciona um botão para fechar a nova janela e maximizar a janela principal
        btn_fechar = ctk.CTkButton(self.frame_2, text="Fechar", command=self.fechar_janela_graficos)
        btn_fechar.pack(pady=20)

        # Adiciona um botão para salvar os gráficos em PDF
        btn_salvar_pdf = ctk.CTkButton(self.frame_2, text="Salvar PDF", command=self.salvar_pdf)
        btn_salvar_pdf.pack(pady=20)
        
        
        self.gerar_graficos()
    
    def gerar_graficos(self):
        mes = self.mes_combobox.get()
        ano = self.ano_combobox.get()

        try:
            cursor = self.conn.cursor()
            query = """
                SELECT PRESENCA, COUNT(*)
                FROM tblControle
                WHERE MONTH(DATA)=? AND YEAR(DATA)=?
                GROUP BY PRESENCA
            """
            cursor.execute(query, (list(self.meses_dict.keys())[list(self.meses_dict.values()).index(mes)], ano))
            dados = cursor.fetchall()

            if not dados:
                print("Nenhum dado encontrado para o mês e ano selecionados.")
                return

            tipos_presenca = [row[0] for row in dados]
            quantidades = [row[1] for row in dados]

            # Define as cores e marcadores para cada tipo de presença
            color_map = {
                'OK': ('#cfcfcf', 'o'),
                'FALTA': ('#C3514E', 'x'),
                'ATESTADO': ('#F79747', 'd'),
                'FÉRIAS': ('#F7DC6F', 's'),
                'ALPHAVILLE': ('#5DADE2', 'p'),
                'CURSO': ('#A569BD', '*'),
            }
            colors = [color_map.get(tipo, ('grey', 'o'))[0] for tipo in tipos_presenca]  # Define 'grey' como padrão para tipos desconhecidos

            # Cria subplots com GridSpec
            gs = GridSpec(2, 2, figure=self.figura,)

            self.figura.patch.set_facecolor('none')
            
            # Gráfico de Pizza
            ax1 = self.figura.add_subplot(gs[0, 0])
            wedges, texts, autotexts = ax1.pie(quantidades, labels=tipos_presenca, autopct=lambda p: f'{int(p * sum(quantidades) / 100)}', startangle=0,
                                                pctdistance=0.8, wedgeprops=dict(width=0.4), colors=colors,
                                                )

            # Ajusta as cores dos textos para corresponder às fatias
            for autotext in autotexts:
                autotext.set_color('white')  # Define a cor do texto em branco

            ax1.set_title('Tipo de Presença',)

            # Gráfico de Barras Empilhadas - Contagem de Tipos de Presença por Nome
            query = """
                SELECT NOMES, PRESENCA, COUNT(*)
                FROM tblControle
                WHERE MONTH(DATA)=? AND YEAR(DATA)=?
                GROUP BY NOMES, PRESENCA
                ORDER BY NOMES
            """
            cursor.execute(query, (list(self.meses_dict.keys())[list(self.meses_dict.values()).index(mes)], ano))
            dados_barras = cursor.fetchall()

            if not dados_barras:
                print("Nenhum dado encontrado para o mês e ano selecionados.")
                return

            # Excluir os tipos "OK" e "ALPHAVILLE"
            dados_barras_filtrados = [row for row in dados_barras if row[1] not in ["OK", "ALPHAVILLE"]]

            nomes = list(set([row[0] for row in dados_barras_filtrados]))
            nomes.sort()
            presencas = list(set([row[1] for row in dados_barras_filtrados]))
            contagens = {nome: {presenca: 0 for presenca in presencas} for nome in nomes}

            for row in dados_barras_filtrados:
                nome, presenca, contagem = row
                contagens[nome][presenca] = contagem

            bar_width = 0.5  # Aumentar a espessura das barras
            bar_positions = list(range(len(nomes)))

            ax2 = self.figura.add_subplot(gs[0, 1])
            ax2.set_facecolor('none')  # Fundo transparente para o subplot
            bottom_values = [0] * len(nomes)

            for presenca in presencas:
                counts = [contagens[nome][presenca] for nome in nomes]
                bars = ax2.barh(bar_positions, counts, height=bar_width, label=presenca, color=color_map.get(presenca, ('grey', 'o'))[0], left=bottom_values)
                for bar, count in zip(bars, counts):
                    if count > 0:
                        ax2.text(bar.get_width() + bar.get_x() - bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, str(count), ha='center', va='center', color='white', fontsize=10)
                bottom_values = [i + j for i, j in zip(bottom_values, counts)]

            ax2.set_yticks(bar_positions)
            ax2.set_yticklabels(nomes)
            ax2.tick_params(axis='both', which='both', length=0)
            ax2.set_frame_on(False)
            ax2.set_xlabel('')
            ax2.set_xticklabels([])
            ax2.set_title('Contagem de Tipos de Presença por Nome',)
            # Remove o fundo branco
            ax2.set_facecolor('none')

            # Gráfico de Dispersão
            query = """
                SELECT DATA, NOMES, PRESENCA
                FROM tblControle
                WHERE MONTH(DATA)=? AND YEAR(DATA)=?
            """
            cursor.execute(query, (list(self.meses_dict.keys())[list(self.meses_dict.values()).index(mes)], ano))
            dados_dispersao = cursor.fetchall()

            if not dados_dispersao:
                print("Nenhum dado encontrado para o mês e ano selecionados.")
                return

            # Ordenar os nomes conforme a tabela tblNomes
            query_nomes = "SELECT DISTINCT Nomes FROM tblNomes"
            cursor.execute(query_nomes)
            nomes_ordenados = [row[0] for row in cursor.fetchall()]

            datas = [row[0] for row in dados_dispersao]
            nomes_dispersao = [row[1] for row in dados_dispersao]
            presencas_dispersao = [row[2] for row in dados_dispersao]

            # Filtrar nomes que possuem dados no mês selecionado
            nomes_com_dados = list(set(nomes_dispersao))
            self.nomes = ctk.CTkComboBox(self.frame_2, values=nomes_com_dados)
            self.nomes.pack()
            self.nomes.set('')
            # Mapear nomes para índices com base em nomes_ordenados, filtrando apenas aqueles com dados
            nome_to_index = {nome: i for i, nome in enumerate(nomes_ordenados) if nome in nomes_com_dados}

            # Convertendo nomes_dispersao para seus respectivos índices
            nomes_indices = [nome_to_index[nome] for nome in nomes_dispersao]

            dias = [data.day for data in datas]

            # Aplicar cores e marcadores ao gráfico de dispersão
            scatter_colors = [color_map.get(presenca, ('grey', 'o'))[0] for presenca in presencas_dispersao]
            scatter_markers = [color_map.get(presenca, ('grey', 'o'))[1] for presenca in presencas_dispersao]

            ax3 = self.figura.add_subplot(gs[1, :])
            ax3.set_facecolor('none')  # Fundo transparente para o subplot
            for i, (x, y, color, marker) in enumerate(zip(dias, nomes_indices, scatter_colors, scatter_markers)):
                ax3.scatter(x, y, c=color, marker=marker, label=presencas_dispersao[i] if i == 0 or presencas_dispersao[i] != presencas_dispersao[i-1] else "",)
            ax3.set_title(f'Presença ao Longo dos Dias - {mes}')
            ax3.set_xticks(sorted(list(set(dias))))
            ax3.set_yticks(range(len(nome_to_index)))
            ax3.set_yticklabels([nome for nome in nomes_ordenados if nome in nomes_com_dados])

            # Adicionar legenda fora do gráfico
            handles, labels = ax3.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            ax3.legend(by_label.values(), by_label.keys(), title="Tipo de Presença", bbox_to_anchor=(1, 1), loc='upper left')

            # Adicionar o gráfico ao Tkinter
            chart = FigureCanvasTkAgg(self.figura, self.frame_teste)
            chart.get_tk_widget().pack()

        except pyodbc.Error as e:
            print(f'Error: {e}')



    def salvar_pdf(self):
        # Obter o caminho para a pasta de Downloads
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Nome do arquivo PDF
        pdf_filename = f"graficos_{self.mes_combobox.get()}_{self.ano_combobox.get()}.pdf"
        pdf_filepath = os.path.join(downloads_path, pdf_filename)
        
        # Salvar o PDF
        with PdfPages(pdf_filepath) as pdf:
            pdf.savefig(self.figura)
        
        # Exibir mensagem informando que o PDF foi salvo
        messagebox.showinfo("PDF Salvo", f"PDF salvo com sucesso em: {pdf_filepath}")

        # Abrir a pasta Downloads
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(f'explorer "{downloads_path}"')
            elif os.name == 'posix':  # macOS, Linux
                subprocess.Popen(['xdg-open', downloads_path])
        except Exception as e:
            print(f"Erro ao abrir a pasta Downloads: {e}")


    def fechar_janela_graficos(self):
        # Fecha a nova janela
        self.new_window.destroy()
        # Maximiza a janela principal
        self.parent.root.state('zoomed')
        
if __name__ == '__main__':
    root = ctk.CTk()
    app = ControleApp(root)
    root.mainloop()