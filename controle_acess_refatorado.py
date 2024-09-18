import customtkinter as ctk
import pyodbc
from tkinter import ttk
from tkinter import messagebox
import datetime
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import subprocess
from fpdf import FPDF, XPos, YPos
import pandas as pd


class ControleApp:
    def __init__(self, rot):
        self.root = rot
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
        self.meses_dict = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }

        self.buttons = {}
        self.conn = self.connect_to_db()
        self.selected_site_id = None  # Armazena o ID do site selecionado
        self.selected_empresa_id = None  # Armazena o ID da empresa selecionada
        self.selected_siteempresa_id = None  # Armazena o ID_SiteEmpresa correspondente
        self.setup_auto()

    @staticmethod
    def connect_to_db():
        try:
            con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Henrique\Downloads\Controle.accdb'
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
        frame_menu_lateral = ctk.CTkFrame(janela, width=150, fg_color=self.my_dict['menu-inf'],
                                          bg_color=self.my_dict['preto'])
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
        cursor.execute("SELECT id_Site, Sites FROM Site")
        sites = [row[1] for row in cursor.fetchall()]
        return sites

    def get_site_id(self, site_name):
        """Obtém o ID do site com base no nome do site."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_Site FROM Site WHERE Sites = ?", (site_name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_empresas(self, site_id):
        """Obtém as empresas associadas ao ID_Site, filtrando por empresas ativas."""
        if self.conn is None or not site_id:
            return []

        cursor = self.conn.cursor()
        query = """
            SELECT Empresa.id_Empresa, Empresa.Empresas
            FROM Site_Empresa
            INNER JOIN Empresa ON Site_Empresa.id_Empresas = Empresa.id_Empresa
            WHERE Site_Empresa.id_Sites = ? AND Site_Empresa.Ativo = True
        """
        cursor.execute(query, (site_id,))
        empresas = [(row[0], row[1]) for row in cursor.fetchall()]
        return empresas

    def get_siteempresa_id(self, site_id, empresa_id):
        """Obtém o ID_SiteEmpresas com base no site e empresa selecionados, considerando apenas empresas ativas."""
        cursor = self.conn.cursor()
        query = """SELECT id_SiteEmpresa FROM Site_Empresa WHERE id_Sites = ? AND id_Empresas = ? AND Ativo = True"""
        cursor.execute(query, (site_id, empresa_id))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_nomes(self, siteempresa_id, ativos=True):
        """Obtém os nomes associados ao ID_SiteEmpresas, filtrando por ativos se solicitado."""
        cursor = self.conn.cursor()
        query = "SELECT Nome.Nome FROM Nome WHERE id_SiteEmpresa = ?"

        if ativos:
            query += " AND Ativo = True"
        else:
            query += " AND Ativo = False"

        cursor.execute(query, (siteempresa_id,))
        nomes = [row[0] for row in cursor.fetchall()]
        return nomes

    def get_anos(self):
        """Retorna uma lista de anos presentes na coluna de Data da tabela Controle."""
        if self.conn is None:
            return []

        cursor = self.conn.cursor()
        query = """
            SELECT Ano
            FROM (
                SELECT DISTINCT YEAR(Data) AS Ano
                FROM Controle
            ) AS Subconsulta
            ORDER BY Ano DESC
        """
        cursor.execute(query)
        anos = [str(row[0]) for row in cursor.fetchall()]
        return anos

    def get_presenca(self):
        if self.conn is None:
            return []
        query = """ SELECT Presenca.Presenca FROM Presenca """
        cursor = self.conn.cursor()
        cursor.execute(query)
        presenca = [row[0] for row in cursor.fetchall()]
        return presenca

    def on_site_selected(self, event):
        site_name = self.combo_sites.get()
        # Obter o ID do site selecionado
        self.selected_site_id = self.get_site_id(site_name)

        # Atualiza a ComboBox de empresas com base no site selecionado
        empresas = self.get_empresas(self.selected_site_id)
        self.combo_empresas['values'] = [empresa[1] for empresa in empresas]
        self.combo_empresas.set('')  # Reseta a seleção de empresas
        self.selected_empresa_id = None
        self.selected_siteempresa_id = None

        # Desativa os botões até que a empresa seja selecionada
        self.toggle_buttons(state="disabled")

    def on_empresa_selected(self, event):
        empresa_name = self.combo_empresas.get()
        # Obter o ID da empresa selecionada
        empresas = self.get_empresas(self.selected_site_id)
        self.selected_empresa_id = next((emp[0] for emp in empresas if emp[1] == empresa_name), None)

        # Obter o ID_SiteEmpresas correspondente
        self.selected_siteempresa_id = self.get_siteempresa_id(self.selected_site_id, self.selected_empresa_id)

        # Ativa os botões apenas após a seleção do site e da empresa
        if self.selected_siteempresa_id:
            self.toggle_buttons(state="normal")
            self.show_frame('Controle de Frequencia')

    def toggle_buttons(self, state):
        """Ativa ou desativa os botões."""
        for button in self.buttons.values():
            button.configure(state=state)

    def add_buttons_menu(self, frame):
        button_texts = ["Controle de Frequencia", "Nomes", "Empresas", "Relatorio Mensal"]

        for text in button_texts:
            button = ctk.CTkButton(
                frame,
                text=text,
                command=lambda t=text: self.show_frame(t),
                hover_color=self.my_dict['hover'],
                border_width=2,
                border_color=self.my_dict['menu-sup'],
                state="disabled"
            )
            button.pack(pady=10, padx=10, fill='x')
            self.buttons[text] = button  # Armazena o botão no dicionário

    def show_initial_message(self):
        # Exibe uma mensagem inicial solicitando que o usuário selecione um site e uma empresa
        label = ctk.CTkLabel(self.frame_tela, text="Por favor, selecione um site e uma empresa no menu à esquerda.",
                             text_color=self.my_dict['font'])
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
                button.configure(fg_color='transparent', border_color=self.my_dict['menu-sup'])

        # Adiciona novo conteúdo baseado no botão pressionado
        if frame_name == "Controle de Frequencia":
            if self.selected_siteempresa_id:
                AbaControle(self, self.frame_tela, self.my_dict, self.conn, self.selected_siteempresa_id)
            else:
                self.show_initial_message()
        elif frame_name == "Relatorio Mensal":
            if self.selected_siteempresa_id:
                AbaRelatorioMes(self, self.frame_tela, self.my_dict, self.conn, self.selected_siteempresa_id)
            else:
                self.show_initial_message()
        elif frame_name == "Empresas":
            if self.selected_siteempresa_id:
                AbaEmpresas(self, self.frame_tela, self.my_dict, self.conn, self.selected_siteempresa_id)
            else:
                self.show_initial_message()
        elif frame_name == "Nomes":
            if self.selected_siteempresa_id:
                AbaNomes(self, self.frame_tela, self.my_dict, self.conn, self.selected_siteempresa_id)
            else:
                self.show_initial_message()


class AbaControle:
    def __init__(self, app_, frame, my_dict, conn, selected_siteempresa_id):
        self.app = app_
        self.frame = frame
        self.my_dict = my_dict
        self.conn = conn
        self.selected_siteempresa_id = selected_siteempresa_id
        self.filter_active = False  # Variável para controlar o estado do filtro

        self.setup()

    def setup(self):
        self.style = ttk.Style()
        # Configurando o estilo da Treeview
        self.style.theme_use('alt')  # Use 'clam' ou outro tema que suporte estilos personalizados

        # Obter os nomes relacionados ao ID_SiteEmpresas
        nomes = self.app.get_nomes(self.selected_siteempresa_id)

        # Exibir os nomes na aba de controle
        label = ctk.CTkLabel(self.frame, text=f"Nomes associados ao site e empresa selecionados:",
                             text_color=self.my_dict['font'])
        label.pack(pady=10)

        self.frame_checkbox = ctk.CTkFrame(self.frame, fg_color=self.my_dict['preto'], height=50)
        self.frame_checkbox.pack(pady=10, padx=10, fill='x')

        self.checkbox_vars = {}  # Dicionário para armazenar as variáveis das checkboxes
        row, col = 0, 0
        max_columns = 9  # Defina o número máximo de colunas por linha

        for nome in nomes:
            var = ctk.StringVar(value='off')
            checkbox = ctk.CTkCheckBox(self.frame_checkbox, text=nome, variable=var, onvalue='on', offvalue='off',
                                       font=('Arial', 15), hover_color=self.my_dict['Heading_color'])
            checkbox.grid(row=row, column=col, padx=5, pady=5)
            self.checkbox_vars[nome] = var  # Armazena a variável da checkbox
            col += 1

            if col >= max_columns:
                col = 0
                row += 1

        combobox_frame = ctk.CTkFrame(self.frame, fg_color=self.my_dict['preto'], )
        combobox_frame.pack(pady=10, padx=10, fill='x')

        # tipo presenca
        tipo_presenca_label = ctk.CTkLabel(combobox_frame, text="Presença :", text_color=self.my_dict['font'])
        tipo_presenca_label.grid(row=0, column=1, padx=5, pady=5)
        self.tipo_presenca_combobox = ctk.CTkComboBox(combobox_frame, values=self.app.get_presenca(), state='readonly')
        self.tipo_presenca_combobox.grid(row=0, column=2, padx=10, pady=5)

        # Dia
        dias = [str(i) for i in range(1, 32)]

        dia_label = ctk.CTkLabel(combobox_frame, text="Dia :", text_color=self.my_dict['font'])
        dia_label.grid(row=0, column=3, padx=10, pady=5)
        self.dia_combobox = ctk.CTkComboBox(combobox_frame, values=dias, state='readonly')
        self.dia_combobox.grid(row=0, column=4, padx=10, pady=5)

        # Mês
        mes_label = ctk.CTkLabel(combobox_frame, text="Mês :", text_color=self.my_dict['font'])
        mes_label.grid(row=0, column=5, padx=10, pady=5)
        self.mes_combobox = ctk.CTkComboBox(combobox_frame, values=list(self.app.meses_dict.values()), state='readonly')
        self.mes_combobox.grid(row=0, column=6, padx=10, pady=5)
        mes_atual = datetime.datetime.now().month
        self.mes_combobox.set(self.app.meses_dict[mes_atual])

        # Ano
        ano_atual = datetime.datetime.now().year
        ano_inicial = 2024
        anos = [str(a) for a in range(ano_inicial, ano_atual + 100)]
        ano_label = ctk.CTkLabel(combobox_frame, text="Ano :", text_color=self.my_dict['font'])
        ano_label.grid(row=0, column=7, padx=10, pady=5)
        self.ano_combobox = ctk.CTkComboBox(combobox_frame, values=anos, state='readonly')
        self.ano_combobox.grid(row=0, column=8, padx=10, pady=5)
        self.ano_combobox.set(str(datetime.datetime.now().year))

        # Botões
        button = ctk.CTkButton(combobox_frame, text="Adicionar", width=55, height=30, command=self.adicionar_frequencia)
        button.grid(row=0, column=10, padx=10, pady=5)
        button_delete = ctk.CTkButton(combobox_frame, text="Deletar", width=55, height=30,
                                      command=self.remover_frequencia)
        button_delete.grid(row=0, column=11, padx=10, pady=5)
        # spacer = ctk.CTkLabel(combobox_frame, text='')
        # spacer.grid(padx=0,row=0, column=12)
        self.filter_button = ctk.CTkButton(combobox_frame, text="Filtrar", width=55, height=30,
                                           command=self.toggle_filter)
        self.filter_button.grid(row=0, column=12, padx=5, pady=5)

        # Tabela (Treeview)
        tabela_frame = ctk.CTkFrame(self.frame, fg_color=self.my_dict['preto'])
        tabela_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.tabela = ttk.Treeview(tabela_frame, columns=("Nome", "Presença", "Data"), show='headings')
        self.treeScrollbar = ctk.CTkScrollbar(tabela_frame, command=self.tabela.yview)
        self.treeScrollbar.pack(side='right', fill='y')
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("Presença", text="Presença")
        self.tabela.heading("Data", text="Data")
        # Scrollbar
        self.tabela.configure(yscrollcommand=self.treeScrollbar.set)
        self.tabela.pack(fill='both', expand=True)

        # Configurando as cores da Treeview
        self.style.configure("Treeview.Heading", background=self.my_dict['Heading_color'],
                             foreground=self.my_dict['font'], borderwidth=1, relief='solid', font=('Arial', 12),
                             bordercolor=self.my_dict['Heading_color'])
        self.style.map("Treeview.Heading", background=[('active', self.my_dict['hover_treeview'])])
        self.style.configure("Treeview", background=self.my_dict['preto'], foreground=self.my_dict['font'],
                             fieldbackground=self.my_dict['preto'], rowheight=25)
        self.style.map("Treeview", background=[('selected', self.my_dict['hover_treeview'])])
        # Preencher a Treeview com dados
        self.preencher_tabela()

    def preencher_tabela(self):
        """Preenche a Treeview com os dados da consulta SQL."""
        query = """
            SELECT Nome.Nome, Presenca.Presenca, Controle.Data, Controle.id_SiteEmpresa
            FROM Presenca 
            INNER JOIN (Nome 
            INNER JOIN Controle ON Nome.id_Nomes = Controle.id_Nome) 
            ON Presenca.id_Presenca = Controle.id_Presenca
            WHERE Controle.id_SiteEmpresa = ?;
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (self.selected_siteempresa_id,))

        # Limpar a Treeview antes de adicionar novos dados
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        # Adicionar os dados à Treeview
        for row in cursor.fetchall():
            nome = row[0]  # Nome do funcionário
            presenca = row[1]  # Status de presença
            data = row[2].strftime("%d/%m/%Y")  # Formatar data
            self.tabela.insert("", "end", values=(nome, presenca, data))

    def adicionar_frequencia(self): 
        # Obter o tipo de presença selecionado
        tipo_presenca = self.tipo_presenca_combobox.get()

        # Obter o dia, mês e ano selecionados
        dia = self.dia_combobox.get()
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = self.ano_combobox.get()

        # Verificar se todos os campos necessários foram preenchidos
        if not tipo_presenca or not dia or not mes or not ano:
            messagebox.showerror("Erro", "Todos os campos de presença e data devem ser preenchidos.")
            return

        # Verificar se algum nome foi selecionado
        nomes_selecionados = [nome for nome, var in self.checkbox_vars.items() if var.get() == 'on']
        if not nomes_selecionados:
            messagebox.showerror("Erro", "Nenhum nome foi selecionado.")
            return

        # Converter a data selecionada em um formato datetime
        try:
            data_selecionada = datetime.datetime(int(ano), mes, int(dia))
        except ValueError:
            messagebox.showerror("Erro", "Data inválida selecionada.")
            return

        # Verificar se a data cai em um sábado ou domingo
        if data_selecionada.weekday() >= 5: # 5 e 6 correspondem a sábado e domingo, respectivamente
            messagebox.showerror("Erro", "Não é permitido adicionar frequência para sábados ou domingos.")
            return

        # Inicializar a lista para acumular os detalhes de sucesso
        detalhes_sucesso = []

        # Verificar se já existem registros de presença para os nomes na data selecionada
        novos_registros = []
        atestado_nomes = [] # Lista para armazenar os nomes com atestado
        nomes_com_dados_existentes = [] # Nomes que já possuem registros na data

        try:
            cursor = self.conn.cursor()

            for nome, var in self.checkbox_vars.items():
                if var.get() == 'on': # Verifica se a checkbox está marcada
                    # Obter o id_Nome do nome selecionado
                    cursor.execute("SELECT id_Nomes FROM Nome WHERE Nome = ? AND id_SiteEmpresa = ?",
                                (nome, self.selected_siteempresa_id))
                    id_nome = cursor.fetchone()[0]

                    # Verificar se já existe um registro para a data selecionada
                    cursor.execute("""
                        SELECT id_Controle, Presenca.Presenca 
                        FROM Controle
                        INNER JOIN Presenca ON Controle.id_Presenca = Presenca.id_Presenca
                        WHERE id_Nome = ? AND Data = ? AND id_SiteEmpresa = ?
                    """, (id_nome, data_selecionada, self.selected_siteempresa_id))

                    resultado = cursor.fetchone()

                    if resultado:
                        nomes_com_dados_existentes.append((nome, resultado[1])) # Guardar o nome e o tipo de presença existente
                    else:
                        # Verificar o último registro de presença para este nome apenas se o tipo selecionado for "atestado"
                        if tipo_presenca.lower() == "atestado":
                            cursor.execute("""
                                SELECT TOP 1 Presenca.Presenca
                                FROM Controle
                                INNER JOIN Presenca ON Controle.id_Presenca = Presenca.id_Presenca
                                WHERE id_Nome = ? AND id_SiteEmpresa = ?
                                ORDER BY Controle.Data DESC
                            """, (id_nome, self.selected_siteempresa_id))

                            ultimo_registro = cursor.fetchone()

                            if ultimo_registro and ultimo_registro[0].lower() == "atestado":
                                atestado_nomes.append(nome)
                            else:
                                novos_registros.append((id_nome, nome))
                        else:
                            # Se não for "atestado", diretamente adicionar o nome
                            novos_registros.append((id_nome, nome))

            # Perguntar ao usuário se deseja alterar os valores já existentes
            if nomes_com_dados_existentes:
                nomes_existentes_str = "\n".join([f"{nome}: {presenca}" for nome, presenca in nomes_com_dados_existentes])
                resposta = messagebox.askyesno(
                    "Confirmação",
                    f"Os seguintes nomes já possuem registros na data selecionada:\n\n{nomes_existentes_str}\n\n"
                    "Deseja alterar os valores existentes?"
                )

                if not resposta:
                    # Se o usuário não quiser alterar, remover os nomes com dados existentes da lista de novos registros
                    for nome, _ in nomes_com_dados_existentes:
                        novos_registros = [registro for registro in novos_registros if registro[1] != nome]

            # Verificar se há nomes com atestado no último registro
            if atestado_nomes:
                resposta_atestado = messagebox.askyesno(
                    "Confirmação",
                    f"Os seguintes nomes possuem 'atestado' no último registro: {', '.join(atestado_nomes)}.\n"
                    "Deseja marcar a nova frequência como 'atestado' clique em 'sim'.\n Quer colocar 'falta' para esses nomes, clique em 'não'."
                )
                tipo_presenca_atestado = "atestado" if resposta_atestado else "falta"

                # Inserir registros para os nomes com atestado
                for nome in atestado_nomes:
                    cursor.execute("SELECT id_Nomes FROM Nome WHERE Nome = ? AND id_SiteEmpresa = ?",
                                (nome, self.selected_siteempresa_id))
                    id_nome = cursor.fetchone()[0]

                    cursor.execute("SELECT id_Presenca FROM Presenca WHERE Presenca = ?", (tipo_presenca_atestado,))
                    id_presenca = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO Controle (id_Nome, id_Presenca, Data, id_SiteEmpresa)
                        VALUES (?, ?, ?, ?)
                    """, (id_nome, id_presenca, data_selecionada, self.selected_siteempresa_id))

                    detalhes_sucesso.append(f"{nome} - {tipo_presenca_atestado} em {data_selecionada.strftime('%d/%m/%Y')}")

            # Inserir novos registros para os outros nomes
            for id_nome, nome in novos_registros:
                cursor.execute("SELECT id_Presenca FROM Presenca WHERE Presenca = ?", (tipo_presenca,))
                id_presenca = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO Controle (id_Nome, id_Presenca, Data, id_SiteEmpresa)
                    VALUES (?, ?, ?, ?)
                """, (id_nome, id_presenca, data_selecionada, self.selected_siteempresa_id))

                detalhes_sucesso.append(f"{nome} - {tipo_presenca} em {data_selecionada.strftime('%d/%m/%Y')}")

            self.conn.commit() # Confirmar as alterações

            # Montar a mensagem de sucesso
            mensagem_sucesso = "Frequência adicionada com sucesso para:\n" + "\n".join(detalhes_sucesso)
            messagebox.showinfo("Sucesso", mensagem_sucesso)

            # Atualizar a tabela após adicionar a frequência
            self.preencher_tabela()

            # Limpar as checkboxes após adicionar
            for var in self.checkbox_vars.values():
                var.set('off')

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao adicionar frequência: {e}")

    def remover_frequencia(self):
        # Obter o dia, mês e ano selecionados
        dia = self.dia_combobox.get()
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = self.ano_combobox.get()

        # Verificar se o dia, mês e ano foram selecionados
        if not dia or not mes or not ano:
            messagebox.showerror("Erro", "Selecione um dia, mês e ano para remover registros.")
            return

        # Converter a data selecionada em um formato datetime
        try:
            data_selecionada = datetime.datetime(int(ano), mes, int(dia))
        except ValueError:
            messagebox.showerror("Erro", "Data inválida selecionada.")
            return

        # Inicializar a lista para acumular os detalhes dos registros a serem deletados
        registros_para_deletar = []

        try:
            cursor = self.conn.cursor()

            for nome, var in self.checkbox_vars.items():
                if var.get() == 'on':  # Verifica se a checkbox está marcada
                    # Obter o id_Nome do nome selecionado
                    cursor.execute("SELECT id_Nomes FROM Nome WHERE Nome = ? AND id_SiteEmpresa = ?",
                                   (nome, self.selected_siteempresa_id))
                    id_nome = cursor.fetchone()[0]

                    # Verificar se já existe um registro para a data selecionada
                    cursor.execute("""
                            SELECT id_Controle, Presenca.Presenca 
                            FROM Controle
                            INNER JOIN Presenca ON Controle.id_Presenca = Presenca.id_Presenca
                            WHERE id_Nome = ? AND Data = ? AND id_SiteEmpresa = ?
                        """, (id_nome, data_selecionada, self.selected_siteempresa_id))

                    resultado = cursor.fetchone()
                    if resultado:
                        registros_para_deletar.append((resultado[0], nome, resultado[1], data_selecionada))

            if not registros_para_deletar:
                messagebox.showinfo("Informação", "Não há registros para deletar na data selecionada.")
                return

            # Preparar a mensagem de confirmação com os detalhes dos registros a serem deletados
            detalhes_para_deletar = "\n".join(
                [f"{nome} - {presenca} em {data.strftime('%d/%m/%Y')}" for _, nome, presenca, data in
                 registros_para_deletar])
            resposta = messagebox.askyesno("Confirmação",
                                           f"Os seguintes registros serão deletados:\n\n{detalhes_para_deletar}\n\nDeseja continuar?")
            if not resposta:
                return

            # Deletar os registros selecionados
            for id_controle, _, _, _ in registros_para_deletar:
                cursor.execute("DELETE FROM Controle WHERE id_Controle = ?", (id_controle,))

            self.conn.commit()  # Confirmar as alterações

            messagebox.showinfo("Sucesso", "Registros deletados com sucesso.")
            self.preencher_tabela()  # Atualizar a tabela após deletar os registros

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao deletar registros: {e}")

    def filtrar_frequencia(self):
        # Obter o tipo de presença, dia, mês, ano e nomes selecionados
        tipo_presenca = self.tipo_presenca_combobox.get()
        dia = self.dia_combobox.get()
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = self.ano_combobox.get()

        nomes_selecionados = [nome for nome, var in self.checkbox_vars.items() if var.get() == 'on']

        # Verificar se algum critério foi selecionado
        if not (tipo_presenca or dia or mes or ano or nomes_selecionados):
            messagebox.showerror("Erro", "Selecione pelo menos um critério de filtragem.")
            return

        # Construir a consulta SQL com base nos filtros selecionados
        query = """
            SELECT Nome.Nome, Presenca.Presenca, Controle.Data
            FROM Presenca 
            INNER JOIN (Nome 
            INNER JOIN Controle ON Nome.id_Nomes = Controle.id_Nome) 
            ON Presenca.id_Presenca = Controle.id_Presenca
            WHERE Controle.id_SiteEmpresa = ?
        """

        params = [self.selected_siteempresa_id]

        # Adicionar filtros conforme os critérios selecionados
        if tipo_presenca:
            query += " AND Presenca.Presenca = ?"
            params.append(tipo_presenca)

        if dia:
            query += " AND DAY(Controle.Data) = ?"
            params.append(dia)

        if mes:
            query += " AND MONTH(Controle.Data) = ?"
            params.append(mes)

        if ano:
            query += " AND YEAR(Controle.Data) = ?"
            params.append(ano)

        if nomes_selecionados:
            placeholders = ', '.join(['?'] * len(nomes_selecionados))
            query += f" AND Nome.Nome IN ({placeholders})"
            params.extend(nomes_selecionados)

        # Executar a consulta e preencher a tabela
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)

            # Limpar a Treeview antes de adicionar os dados filtrados
            for row in self.tabela.get_children():
                self.tabela.delete(row)

            # Adicionar os dados filtrados à Treeview
            for row in cursor.fetchall():
                nome = row[0]
                presenca = row[1]
                data = row[2].strftime("%d/%m/%Y")
                self.tabela.insert("", "end", values=(nome, presenca, data))

            self.filter_active = True  # Sinalizar que o filtro está ativo

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao filtrar os dados: {e}")

    def toggle_filter(self):
        if self.filter_active:
            self.preencher_tabela()  # Exibir todos os registros
            self.filter_active = False
            self.filter_button.configure(text="Filtrar")  # Alterar o texto do botão para "Filtrar"
            messagebox.showinfo("Filtro", "Filtro removido.")
            self.tipo_presenca_combobox.set('')
        else:
            self.filtrar_frequencia()  # Aplicar o filtro
            self.filter_active = True
            self.filter_button.configure(text="Limpar Filtro")  # Alterar o texto do botão para "Limpar Filtro"


class AbaNomes:
    def __init__(self, app_, frame, my_dict, conn, selected_siteempresa_id):
        self.app = app_
        self.frame = frame
        self.my_dict = my_dict
        self.conn = conn
        self.selected_siteempresa_id = selected_siteempresa_id
        self.setup()

    def setup(self):
        label = ctk.CTkLabel(self.frame, text="Gerenciar Empresas e Nomes", text_color=self.my_dict['font'])
        label.pack(pady=20)

        # Frame para o conteúdo de Nomes
        frame_input_nome = ctk.CTkFrame(self.frame, fg_color=self.my_dict['preto'])
        frame_input_nome.pack(pady=10, padx=10, fill='both', expand=True)

        # Inserir Nome
        nome_label = ctk.CTkLabel(frame_input_nome, text="Inserir Nome:", text_color=self.my_dict['font'])
        nome_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.nome_entry = ctk.CTkEntry(frame_input_nome, fg_color=self.my_dict['preto'],
                                       placeholder_text="Insira o Nome aqui!",
                                       placeholder_text_color=self.my_dict['frames_ajuste'])
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        button_add_nome = ctk.CTkButton(frame_input_nome, text="Adicionar Nome", fg_color=self.my_dict['adicionar_btn'],
                                        command=self.add_nome)
        button_add_nome.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Remover Nome
        nome_label_remove = ctk.CTkLabel(frame_input_nome, text="Remover Nome:", text_color=self.my_dict['font'])
        nome_label_remove.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.nome_combobox = ctk.CTkComboBox(frame_input_nome, values=self.app.get_nomes(self.selected_siteempresa_id),
                                             state='readonly')
        self.nome_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        button_remove_nome = ctk.CTkButton(frame_input_nome, text="Remover Nome", fg_color=self.my_dict['remover_btn'],
                                           command=self.inativar_nome)
        button_remove_nome.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Reativar Nome
        reativar_nome_label = ctk.CTkLabel(frame_input_nome, text="Reativar Nome:", text_color=self.my_dict['font'])
        reativar_nome_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Preenchendo a ComboBox de nomes inativos corretamente
        self.nome_inativo_combobox = ctk.CTkComboBox(frame_input_nome,
                                                     values=self.app.get_nomes(self.selected_siteempresa_id,
                                                                               ativos=False), state='readonly')
        self.nome_inativo_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        button_reativar_nome = ctk.CTkButton(frame_input_nome, text="Reativar Nome",
                                             fg_color=self.my_dict['adicionar_btn'], command=self.reativar_nome)
        button_reativar_nome.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

    def add_nome(self):
        # Recuperar o nome inserido
        nome = self.nome_entry.get().strip()

        if not nome:
            messagebox.showerror("Erro", "O nome não pode estar vazio.")
            return

        try:
            cursor = self.conn.cursor()

            # Inserir o nome na tabela Nome usando o id_SiteEmpresa selecionado, e definindo Ativo como True
            cursor.execute("INSERT INTO Nome (Nome, id_SiteEmpresa, Ativo) VALUES (?, ?, True)",
                           (nome, self.selected_siteempresa_id))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Nome adicionado com sucesso!")

            # Limpar as entradas
            self.nome_entry.delete(0, 'end')

            # Atualizar a combobox de nomes
            self.nome_combobox['values'] = self.app.get_nomes(self.selected_siteempresa_id)

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao adicionar nome: {e}")

    def reativar_nome(self):
        """Reativa um nome inativo na tabela Nome."""
        nome = self.nome_inativo_combobox.get().strip()

        if not nome:
            messagebox.showerror("Erro", "Selecione um nome para reativar.")
            return

        try:
            cursor = self.conn.cursor()

            # Marcar o nome como ativo
            cursor.execute("UPDATE Nome SET Ativo = True WHERE Nome = ? AND id_SiteEmpresa = ?",
                           (nome, self.selected_siteempresa_id))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Nome reativado com sucesso!")

            # Atualizar os ComboBoxes de nomes ativos e inativos
            self.nome_combobox['values'] = self.app.get_nomes(self.selected_siteempresa_id)
            self.nome_inativo_combobox['values'] = self.app.get_nomes(self.selected_siteempresa_id, ativos=False)

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao reativar nome: {e}")

    def inativar_nome(self):
        """Inativa um nome na tabela Nome, garantindo que o site selecionado tenha pelo menos um nome ativo."""
        nome = self.nome_combobox.get().strip()

        if not nome:
            messagebox.showerror("Erro", "Selecione um nome para inativar.")
            return

        try:
            # Obter o ID do site_empresa e verificar quantos nomes ativos existem
            cursor = self.conn.cursor()
            query = """
                SELECT COUNT(*) 
                FROM Nome 
                WHERE id_SiteEmpresa = ? AND Ativo = True
            """
            cursor.execute(query, (self.selected_siteempresa_id,))
            count_ativos = cursor.fetchone()[0]

            if count_ativos <= 1:
                messagebox.showerror("Erro", "Não é possível inativar o último nome ativo do site.")
                return

            # Marcar o nome como inativo
            cursor.execute("UPDATE Nome SET Ativo = False WHERE Nome = ? AND id_SiteEmpresa = ?",
                           (nome, self.selected_siteempresa_id))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Nome inativado com sucesso!")

            # Atualizar a combobox de nomes
            self.nome_combobox['values'] = self.app.get_nomes(self.selected_siteempresa_id)

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao inativar nome: {e}")


class AbaEmpresas:
    def __init__(self, app_, frame, my_dict, conn, selected_siteempresa_id):
        self.app = app_
        self.frame = frame
        self.my_dict = my_dict
        self.conn = conn
        self.selected_siteempresa_id = selected_siteempresa_id
        self.setup()

    def setup(self):
        label = ctk.CTkLabel(self.frame, text="Gerenciar Empresas e Nomes", text_color=self.my_dict['font'])
        label.pack(pady=20)

        # Frame para o conteúdo de Empresas
        self.frame_input_empresa = ctk.CTkFrame(self.frame, fg_color=self.my_dict['preto'])
        self.frame_input_empresa.pack(pady=10, padx=10, fill='both', expand=True, side='left')

        # Inserir Empresa
        empresa_label = ctk.CTkLabel(self.frame_input_empresa, text="Inserir Empresa:", text_color=self.my_dict['font'])
        empresa_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.empresa_entry = ctk.CTkEntry(self.frame_input_empresa, fg_color=self.my_dict['preto'],
                                          placeholder_text="Insira a empresa aqui!",
                                          placeholder_text_color=self.my_dict['frames_ajuste'])
        self.empresa_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        button_add_empresa = ctk.CTkButton(self.frame_input_empresa, text="Adicionar Empresa",
                                           fg_color=self.my_dict['adicionar_btn'], command=self.add_empresa)
        button_add_empresa.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Desativar Empresa
        empresa_label_remove = ctk.CTkLabel(self.frame_input_empresa, text="Desativar Empresa:",
                                            text_color=self.my_dict['font'])
        empresa_label_remove.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.empresa_combobox = ctk.CTkComboBox(self.frame_input_empresa, values=self.get_empresas_ativas(),
                                                state='readonly')
        self.empresa_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        button_remove_empresa = ctk.CTkButton(self.frame_input_empresa, text="Desativar",
                                              fg_color=self.my_dict['remover_btn'], command=self.desativar_empresa)
        button_remove_empresa.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Ativar Empresa
        empresa_label_activate = ctk.CTkLabel(self.frame_input_empresa, text="Ativar Empresa:",
                                              text_color=self.my_dict['font'])
        empresa_label_activate.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.empresa_inativa_combobox = ctk.CTkComboBox(self.frame_input_empresa, values=self.get_empresas_inativas(),
                                                        state='readonly')
        self.empresa_inativa_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        button_ativar_empresa = ctk.CTkButton(self.frame_input_empresa, text="Ativar",
                                              fg_color=self.my_dict['adicionar_btn'], command=self.ativar_empresa)
        button_ativar_empresa.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

    def get_empresas_ativas(self):
        """Retorna a lista de empresas ativas associadas ao site selecionado."""
        empresas = self.app.get_empresas(self.app.selected_site_id)
        return [empresa[1] for empresa in empresas]

    def get_empresas_inativas(self):
        """Retorna a lista de empresas inativas associadas ao site selecionado."""
        if self.conn is None or not self.app.selected_site_id:
            return []

        cursor = self.conn.cursor()
        query = """
            SELECT Empresa.Empresas
            FROM Site_Empresa
            INNER JOIN Empresa ON Site_Empresa.id_Empresas = Empresa.id_Empresa
            WHERE Site_Empresa.id_Sites = ? AND Site_Empresa.Ativo = False
        """
        cursor.execute(query, (self.app.selected_site_id,))
        empresas_inativas = [row[0] for row in cursor.fetchall()]
        return empresas_inativas

    def ativar_empresa(self):
        """Ativa uma empresa inativa, garantindo que o site tenha pelo menos uma empresa ativa."""
        empresa_name = self.empresa_inativa_combobox.get().strip()

        if not empresa_name:
            messagebox.showerror("Erro", "Selecione uma empresa para ativar.")
            return

        try:
            # Obter o ID da empresa selecionada
            cursor = self.conn.cursor()
            query = """
                SELECT id_Empresa 
                FROM Empresa 
                WHERE Empresas = ?
            """
            cursor.execute(query, (empresa_name,))
            empresa_id = cursor.fetchone()[0]

            # Verificar se a empresa já está ativa
            active_empresas = self.get_empresas_ativas()
            if empresa_name in active_empresas:
                messagebox.showinfo("Informação", "Essa empresa já está ativa.")
                return

            # Atualizar o campo Ativo para True na tabela Site_Empresa
            cursor.execute("UPDATE Site_Empresa SET Ativo = True WHERE id_Sites = ? AND id_Empresas = ?",
                           (self.app.selected_site_id, empresa_id))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Empresa ativada com sucesso!")

            # Atualizar a combobox de empresas inativas e ativas
            self.empresa_inativa_combobox['values'] = self.get_empresas_inativas()
            self.empresa_combobox['values'] = self.get_empresas_ativas()

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao ativar empresa: {e}")

    def desativar_empresa(self):
        """Torna uma empresa não ativa, garantindo que o site selecionado tenha pelo menos uma empresa ativa."""
        empresa_name = self.empresa_combobox.get().strip()

        if not empresa_name:
            messagebox.showerror("Erro", "Selecione uma empresa para desativar.")
            return

        try:
            # Obter o ID da empresa selecionada
            empresas = self.app.get_empresas(self.app.selected_site_id)
            empresa_id = next((emp[0] for emp in empresas if emp[1] == empresa_name), None)

            if not empresa_id:
                messagebox.showerror("Erro", "Empresa não encontrada.")
                return

            # Verificar se há mais de uma empresa ativa no site
            if len(empresas) <= 1:
                messagebox.showerror("Erro", "Não é possível desativar a última empresa ativa do site.")
                return

            cursor = self.conn.cursor()

            # Desativar a empresa na tabela Site_Empresa
            cursor.execute("UPDATE Site_Empresa SET Ativo = False WHERE id_Sites = ? AND id_Empresas = ?",
                           (self.app.selected_site_id, empresa_id))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Empresa desativada com sucesso!")

            # Atualizar a combobox de empresas ativas e inativas
            self.empresa_combobox['values'] = self.get_empresas_ativas()
            self.empresa_inativa_combobox['values'] = self.get_empresas_inativas()

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao desativar empresa: {e}")

    def add_empresa(self):
        # Recuperar os valores inseridos
        empresa_nome = self.empresa_entry.get().strip()
        siteempresa_id = self.selected_siteempresa_id

        if not empresa_nome:
            messagebox.showerror("Erro", "O nome da empresa não pode estar vazio.")
            return

        try:
            cursor = self.conn.cursor()

            # Verificar se a empresa já existe na tabela Empresa
            cursor.execute("SELECT id_Empresa FROM Empresa WHERE Empresas = ?", (empresa_nome,))
            existing_empresa = cursor.fetchone()

            if existing_empresa:
                # Se a empresa já existe, alerta o usuário
                messagebox.showwarning("Atenção", "Já existe uma empresa com esse nome cadastrada.")
                return

            # Inserir a nova empresa na tabela Empresa
            cursor.execute("INSERT INTO Empresa (Empresas) VALUES (?)", (empresa_nome,))
            self.conn.commit()

            # Recuperar o id_Empresa da nova empresa inserida
            cursor.execute("SELECT @@IDENTITY AS ID_Empresa")
            id_empresa = cursor.fetchone()[0]

            # Obter o id_Site do Site_Empresa selecionado
            cursor.execute("SELECT id_Sites FROM Site_Empresa WHERE id_SiteEmpresa = ?", (siteempresa_id,))
            id_site = cursor.fetchone()[0]

            # Inserir na tabela Site_Empresa com Ativo=TRUE
            cursor.execute("INSERT INTO Site_Empresa (id_Sites, id_Empresas, Ativo) VALUES (?, ?, True)",
                           (id_site, id_empresa))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Empresa adicionada com sucesso!")

            # Limpar as entradas
            self.empresa_entry.delete(0, 'end')

            # Atualizar a combobox de empresas ativas e inativas
            self.empresa_combobox['values'] = self.get_empresas_ativas()
            self.empresa_inativa_combobox['values'] = self.get_empresas_inativas()

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao adicionar empresa: {e}")


class AbaRelatorioMes:
    def __init__(self, app_, frame, my_dict, conn, selected_siteempresa_id):
        self.app = app_
        self.frame = frame
        self.my_dict = my_dict
        self.conn = conn
        self.selected_siteempresa_id = selected_siteempresa_id
        self.setup()

    def setup(self):
        # Título
        label = ctk.CTkLabel(self.frame, text="Relatório Mensal para o site e empresa selecionados",
                             text_color=self.my_dict['font'])
        label.pack(pady=20)

        # Frame para filtros e informações
        filtro_frame = ctk.CTkFrame(self.frame, width=160, fg_color=self.my_dict['menu-inf'],
                                    bg_color=self.my_dict['preto'])
        filtro_frame.pack(padx=20, pady=20, side='left', fill='y', expand=False)

        # Mês
        mes_label = ctk.CTkLabel(filtro_frame, text="Mês:", text_color=self.my_dict['font'])
        mes_label.grid(row=0, column=0, padx=10, pady=5)
        self.mes_combobox = ctk.CTkComboBox(filtro_frame, values=list(self.app.meses_dict.values()), state='readonly')
        self.mes_combobox.grid(row=0, column=1, padx=10, pady=5)
        mes_atual = datetime.datetime.now().month
        self.mes_combobox.set(self.app.meses_dict[mes_atual])

        # Ano
        anos = self.app.get_anos()
        ano_label = ctk.CTkLabel(filtro_frame, text="Ano:", text_color=self.my_dict['font'])
        ano_label.grid(row=1, column=0, padx=10, pady=5)
        self.ano_combobox = ctk.CTkComboBox(filtro_frame, values=anos, state='readonly')
        self.ano_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.ano_combobox.set(str(datetime.datetime.now().year))

        # Botão para aplicar o filtro
        filtro_button = ctk.CTkButton(filtro_frame, text="Aplicar Filtro", command=self.aplicar_filtro)
        filtro_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        salvar_button = ctk.CTkButton(filtro_frame, text="Salvar como PDF", command=self.salvar_pdf)
        salvar_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Informações adicionais
        self.info_label = ctk.CTkLabel(filtro_frame, text="DIAS ÚTEIS: XXXX", text_color=self.my_dict['font'])
        self.info_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.faltas_label = ctk.CTkLabel(filtro_frame, text="FALTAS:", text_color=self.my_dict['font'])
        self.faltas_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.atestados_label = ctk.CTkLabel(filtro_frame, text="ATESTADOS:", text_color=self.my_dict['font'])
        self.atestados_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Frame para os gráficos e tabela
        self.frame_graficos = ctk.CTkFrame(self.frame, fg_color=self.my_dict['preto'])
        self.frame_graficos.pack(padx=20, pady=20, side='right', fill='both', expand=True)

        # Frame para o Gráfico de Dispersão
        self.frame_grafico_dispersao = ctk.CTkFrame(self.frame_graficos, fg_color=self.my_dict['frames_ajuste'])
        self.frame_grafico_dispersao.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.5)

        # Frame para o Gráfico de Pizza
        self.frame_grafico_pizza = ctk.CTkFrame(self.frame_graficos, fg_color=self.my_dict['preto'])
        self.frame_grafico_pizza.place(relx=0.05, rely=0.6, relwidth=0.4, relheight=0.35)

        # Frame para a Tabela
        self.frame_tabela = ctk.CTkFrame(self.frame_graficos, fg_color=self.my_dict['preto'])
        self.frame_tabela.place(relx=0.55, rely=0.6, relwidth=0.4, relheight=0.35)

        # Inicializar variáveis de gráficos
        self.chart_pizza = None
        self.chart_dispersao = None

        # Atualizar informações iniciais
        self.aplicar_filtro()

    def criar_tabela(self):
        for widget in self.frame_tabela.winfo_children():
            widget.destroy()
        # Criando a Treeview para exibir a tabela de presença
        self.tabela = ttk.Treeview(self.frame_tabela, columns=("Nome", "OK", "Falta", "Atestado", "Curso", 'Férias'),
                                   show='headings')
        self.tabela.column("Nome", width=60)  # Ajuste a largura conforme necessário
        self.tabela.column("OK", width=40)
        self.tabela.column("Falta", width=40)
        self.tabela.column("Atestado", width=40)
        self.tabela.column("Curso", width=40)
        self.tabela.column("Férias", width=40)

        self.treeScrollbar = ctk.CTkScrollbar(self.frame_tabela, command=self.tabela.yview)
        self.treeScrollbar.pack(side='right', fill='y')

        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("OK", text="OK")
        self.tabela.heading("Falta", text="Falta")
        self.tabela.heading("Atestado", text="Atestado")
        self.tabela.heading("Curso", text="Curso")
        self.tabela.heading("Férias", text="Férias")

        self.tabela.pack(fill='both', expand=True)
        self.tabela.configure(yscrollcommand=self.treeScrollbar.set)

    def aplicar_filtro(self):
        # Obter o mês e ano selecionados nas ComboBoxes
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = int(self.ano_combobox.get())

        cursor = self.conn.cursor()
        query = """
                    SELECT COUNT(*)
                    FROM Controle
                    WHERE id_SiteEmpresa = ? AND MONTH(Data) = ? AND YEAR(Data) = ?
                """
        cursor.execute(query, (self.selected_siteempresa_id, mes, ano))
        resultado = cursor.fetchone()

        if resultado[0] == 0:
            for widget in self.frame_grafico_dispersao.winfo_children():
                widget.pack_forget()

            for widget in self.frame_grafico_pizza.winfo_children():
                widget.pack_forget()

            for widget in self.frame_tabela.winfo_children():
                widget.pack_forget()

            no_data_message = f"Não há dados inseridos em {mes} de {ano}"

            no_data_label_dispersao = ctk.CTkLabel(self.frame_grafico_dispersao, text=no_data_message,
                                                   text_color='white')
            no_data_label_dispersao.pack(expand=True)

            no_data_label_pizza = ctk.CTkLabel(self.frame_grafico_pizza, text=no_data_message, text_color='white')
            no_data_label_pizza.pack(expand=True)

            no_data_label_tabela = ctk.CTkLabel(self.frame_tabela, text=no_data_message, text_color='white')
            no_data_label_tabela.pack(expand=True)

            return

        for widget in self.frame_grafico_dispersao.winfo_children():
            widget.pack_forget()

        for widget in self.frame_grafico_pizza.winfo_children():
            widget.pack_forget()

        # Esta função irá chamar as demais funções para atualizar as informações

        self.update_info()
        self.criar_tabela()
        self.update_tabela()
        self.criar_grafico_pizza()
        self.criar_grafico_dispersao()

    def update_info(self):
        # Obter o mês e ano selecionados nas ComboBoxes
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = int(self.ano_combobox.get())

        # Calcular e atualizar dias úteis
        dias_uteis = self.calcular_dias_uteis(mes, ano)
        self.info_label.configure(text=f"DIAS ÚTEIS: {dias_uteis}")

        # Calcular e atualizar faltas e atestados
        faltas, atestados = self.calcular_faltas_e_atestados(mes, ano)
        self.faltas_label.configure(text=f"FALTAS: {faltas}")
        self.atestados_label.configure(text=f"ATESTADOS: {atestados}")

    @staticmethod
    def calcular_dias_uteis(mes, ano):
        # Calcula o número de dias úteis (excluindo sábados e domingos) no mês e ano fornecidos
        cal = calendar.Calendar()
        dias_uteis = sum(1 for day in cal.itermonthdays2(ano, mes) if day[0] != 0 and day[1] < 5)
        return dias_uteis

    def calcular_faltas_e_atestados(self, mes, ano):
        # Calcula o número de faltas e atestados no mês e ano fornecidos
        cursor = self.conn.cursor()
        query = """
            SELECT Presenca.Presenca, COUNT(*)
            FROM Controle
            INNER JOIN Presenca ON Controle.id_Presenca = Presenca.id_Presenca
            WHERE id_SiteEmpresa = ? AND MONTH(Data) = ? AND YEAR(Data) = ?
            GROUP BY Presenca.Presenca
        """
        cursor.execute(query, (self.selected_siteempresa_id, mes, ano))

        faltas = 0
        atestados = 0
        for row in cursor.fetchall():
            if row[0].lower() == "falta":
                faltas = row[1]
            elif row[0].lower() == "atestado":
                atestados = row[1]

        return faltas, atestados

    def update_tabela(self):
        # Obter os dados da consulta e preencher a tabela
        cursor = self.conn.cursor()
        query = """
            SELECT 
                Nome.Nome,
                SUM(IIF(Presenca.Presenca = 'ok', 1, 0)) AS ok,
                SUM(IIF(Presenca.Presenca = 'falta', 1, 0)) AS falta,
                SUM(IIF(Presenca.Presenca = 'atestado', 1, 0)) AS atestado,
                SUM(IIF(Presenca.Presenca = 'curso', 1, 0)) AS curso,
                SUM(IIF(Presenca.Presenca = 'férias', 1, 0)) AS ferias
            FROM 
                (Controle
            INNER JOIN 
                Nome ON Controle.id_Nome = Nome.id_Nomes)
            INNER JOIN 
                Presenca ON Controle.id_Presenca = Presenca.id_Presenca
            WHERE 
                Controle.id_SiteEmpresa = ? AND MONTH(Controle.Data) = ? AND YEAR(Controle.Data) = ?
            GROUP BY 
                Nome.Nome;
        """
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = int(self.ano_combobox.get())
        cursor.execute(query, (self.selected_siteempresa_id, mes, ano))

        # Limpar a tabela antes de adicionar novos dados
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        # Preencher a tabela com os resultados da consulta
        for row in cursor.fetchall():
            # Remover as tuplas dos valores e formatar adequadamente como inteiros
            nome = row[0]  # Supondo que row[0] é uma string (o nome)
            ok = int(row[1])  # Convertendo para int
            falta = int(row[2])  # Convertendo para int
            atestado = int(row[3])  # Convertendo para int
            curso = int(row[4])  # Convertendo para int
            ferias = int(row[5])  # Convertendo para int
            # Inserir na tabela
            self.tabela.insert("", "end", values=(nome, ok, falta, atestado, curso, ferias))

    def criar_grafico_pizza(self):
        # Remover o gráfico de pizza anterior, se existir
        if self.chart_pizza:
            self.chart_pizza.get_tk_widget().destroy()

        # Obter os dados de presenças para o gráfico de pizza
        cursor = self.conn.cursor()
        query = """
            SELECT 
                SUM(IIF(Presenca.Presenca = 'ok', 1, 0)) AS ok,
                SUM(IIF(Presenca.Presenca = 'falta', 1, 0)) AS falta,
                SUM(IIF(Presenca.Presenca = 'atestado', 1, 0)) AS atestado,
                SUM(IIF(Presenca.Presenca = 'curso', 1, 0)) AS curso,
                SUM(IIF(Presenca.Presenca = 'férias', 1, 0)) AS ferias
            FROM 
                (Controle
            INNER JOIN 
                Presenca ON Controle.id_Presenca = Presenca.id_Presenca)
            WHERE 
                Controle.id_SiteEmpresa = ? AND MONTH(Controle.Data) = ? AND YEAR(Controle.Data) = ?
        """
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = int(self.ano_combobox.get())
        cursor.execute(query, (self.selected_siteempresa_id, mes, ano))

        row = cursor.fetchone()

        # Filtrar os valores e rótulos que não são zero
        labels = ['OK', 'Falta', 'Atestado', 'Curso', 'Férias']
        sizes = [row[0], row[1], row[2], row[3], row[4]]
        colors = ['#333', '#FF5733', '#FFC300', '#8E44AD', '#a5a5a5']  # Cores para cada categoria

        # Filtrar as categorias com base em valores diferentes de zero
        filtered_labels = []
        filtered_sizes = []
        filtered_colors = []

        for i in range(len(sizes)):
            if sizes[i] > 0:
                filtered_labels.append(labels[i])
                filtered_sizes.append(sizes[i])
                filtered_colors.append(colors[i])

        # Verificar se há valores a serem exibidos
        if not filtered_sizes:
            messagebox.showinfo("Informação", "Não há registros para o mês e ano selecionados.")
            return

        # Criando a figura do gráfico com fundo customizado
        self.figura = plt.Figure(figsize=(4, 4), facecolor=self.my_dict['preto'])
        ax = self.figura.add_subplot(111)

        wedges, texts, autotexts = ax.pie(
            filtered_sizes, labels=filtered_labels, colors=filtered_colors,
            autopct=lambda p: f'{int(p * sum(filtered_sizes) / 100)}',
            startangle=0, pctdistance=0.8,
            wedgeprops=dict(width=0.4)
        )

        # Customizando o texto dentro do gráfico
        for text in autotexts:
            text.set_color('white')
            text.set_fontsize(12)

        # Customizando o texto das labels (fora do gráfico)
        for text in texts:
            text.set_color('white')
            text.set_fontsize(12)

        ax.axis('equal')  # Assegura que o gráfico seja um círculo

        # Adicionar o gráfico ao Tkinter
        self.chart_pizza = FigureCanvasTkAgg(self.figura, self.frame_grafico_pizza)
        self.chart_pizza.get_tk_widget().pack()

        # Customizar o fundo do gráfico
        ax.set_facecolor(self.my_dict['preto'])
        self.figura.patch.set_facecolor(self.my_dict['preto'])

    def criar_grafico_dispersao(self):
        # Remover o gráfico de dispersão anterior, se existir
        if self.chart_dispersao:
            self.chart_dispersao.get_tk_widget().destroy()

        # Obter os dados de presença para o gráfico de dispersão
        cursor = self.conn.cursor()
        query = """
            SELECT 
                Nome.Nome,
                Controle.Data,
                Presenca.Presenca
            FROM 
                (Controle
            INNER JOIN 
                Nome ON Controle.id_Nome = Nome.id_Nomes)
            INNER JOIN 
                Presenca ON Controle.id_Presenca = Presenca.id_Presenca
            WHERE 
                Controle.id_SiteEmpresa = ? AND MONTH(Controle.Data) = ? AND YEAR(Controle.Data) = ?
            ORDER BY Controle.Data
        """
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = int(self.ano_combobox.get())
        cursor.execute(query, (self.selected_siteempresa_id, mes, ano))

        # Preparar os dados para o gráfico de dispersão
        data_dict = {
            'OK': {'datas': [], 'nomes': [], 'cor': '#333', 'marker': 'o'},
            'FALTA': {'datas': [], 'nomes': [], 'cor': '#FF5733', 'marker': 'x'},
            'ATESTADO': {'datas': [], 'nomes': [], 'cor': '#FFC300', 'marker': 'd'},
            'CURSO': {'datas': [], 'nomes': [], 'cor': '#8E44AD', 'marker': '*'},
            'FÉRIAS': {'datas': [], 'nomes': [], 'cor': '#a5a5a5', 'marker': 's'},
            'ALPHAVILLE':{'datas': [], 'nomes': [], 'cor': '#5D578E', 'marker': 's'},
        }

        nomes_unicos = set()
        for row in cursor.fetchall():
            nome = row[0]
            data = row[1]
            presenca = row[2].upper()

            nomes_unicos.add(nome)  # Armazena os nomes únicos para o eixo Y
            if presenca in data_dict:
                data_dict[presenca]['datas'].append(data)
                data_dict[presenca]['nomes'].append(nome)

        # Criar uma lista de todos os dias úteis no mês
        cal = calendar.Calendar()
        dias_uteis = [datetime.date(ano, mes, day) for day, weekday in cal.itermonthdays2(ano, mes) if
                      day != 0 and weekday < 5]

        # Criando a figura do gráfico com fundo customizado
        self.figura_dispersao = plt.Figure(figsize=(6, 4), facecolor=self.my_dict['preto'])
        ax = self.figura_dispersao.add_subplot(111)

        # Plotar os dados
        for tipo, info in data_dict.items():
            if info['datas']:
                # Para que os nomes apareçam corretamente no eixo Y, eles precisam ser numericamente codificados
                y_positions = [list(nomes_unicos).index(nome) + 1 for nome in info['nomes']]
                ax.scatter(info['datas'], y_positions, color=info['cor'], label=tipo, marker=info['marker'])

        ax.set_yticks(range(1, len(nomes_unicos) + 1))
        ax.set_yticklabels(list(nomes_unicos), fontsize=8, color='white')  # Nomes no eixo Y

        # Configurar o eixo X para mostrar apenas os dias úteis
        ax.set_xticks(dias_uteis)  # Define os dias úteis como pontos no eixo X
        ax.set_xticklabels([date.strftime('%d') for date in dias_uteis], fontsize=8, color='white')

        ax.set_facecolor(self.my_dict['preto'])
        self.figura_dispersao.patch.set_facecolor(self.my_dict['preto'])

        ax.spines['bottom'].set_color('white')
        # ax.spines['left'].set_color('white')
        ax.spines['left'].set_visible(False)

        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set(text=f'Presença por Nome - {self.mes_combobox.get()} de {ano}')
        ax.title.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white', labelsize=8)

        # Posicionar a legenda fora do gráfico
        legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor=self.my_dict['preto'],
                           edgecolor='white', fontsize=8)
        for text in legend.get_texts():
            text.set_color("white")

        # Adicionar o gráfico ao Tkinter
        self.chart_dispersao = FigureCanvasTkAgg(self.figura_dispersao, self.frame_grafico_dispersao)
        self.chart_dispersao.get_tk_widget().pack(expand=True, fill='both')

    def salvar_pdf(self):
        # Consulta SQL para obter os dados
        query = """
            SELECT 
                Nome.Nome,
                SUM(IIF(Presenca.Presenca = 'ok', 1, 0)) AS ok,
                SUM(IIF(Presenca.Presenca = 'falta', 1, 0)) AS falta,
                SUM(IIF(Presenca.Presenca = 'atestado', 1, 0)) AS atestado,
                SUM(IIF(Presenca.Presenca = 'curso', 1, 0)) AS curso,
                SUM(IIF(Presenca.Presenca = 'férias', 1, 0)) AS ferias
            FROM 
                (Controle
            INNER JOIN 
                Nome ON Controle.id_Nome = Nome.id_Nomes)
            INNER JOIN 
                Presenca ON Controle.id_Presenca = Presenca.id_Presenca
            WHERE 
                Controle.id_SiteEmpresa = ? AND MONTH(Controle.Data) = ? AND YEAR(Controle.Data) = ?
            GROUP BY 
                Nome.Nome;
        """
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = int(self.ano_combobox.get())

        cursor = self.conn.cursor()
        cursor.execute(query, (self.selected_siteempresa_id, mes, ano))

        # Criar o PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Configurar o título
        pdf.set_font("Helvetica", size=12)
        pdf.cell(200, 10, text=f"Relatório Mensal - {self.mes_combobox.get()} {self.ano_combobox.get()}",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

        # Configurar os cabeçalhos da tabela
        pdf.set_font("Helvetica", size=10)
        pdf.cell(40, 10, text="Nome", border=1)
        pdf.cell(30, 10, text="OK", border=1)
        pdf.cell(30, 10, text="Falta", border=1)
        pdf.cell(40, 10, text="Atestado", border=1)
        pdf.cell(30, 10, text="Curso", border=1)
        pdf.cell(30, 10, text="Férias", border=1)
        pdf.ln()

        # Adicionar os dados ao PDF
        for row in cursor.fetchall():
            pdf.cell(40, 10, text=str(row[0]), border=1)
            pdf.cell(30, 10, text=str(row[1]), border=1)
            pdf.cell(30, 10, text=str(row[2]), border=1)
            pdf.cell(40, 10, text=str(row[3]), border=1)
            pdf.cell(30, 10, text=str(row[4]), border=1)
            pdf.cell(30, 10, text=str(row[5]), border=1)
            pdf.ln()

        # Criar e salvar os gráficos de pizza por nome
        imagens_pizza = self.criar_grafico_pizza_por_nome_pdf()
        dispersao_img_path = self.criar_grafico_dispersao_pdf()

        # Adicionar os gráficos de pizza ao PDF
        for nome, img_path in imagens_pizza:
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            pdf.cell(200, 10, text=f"Gráfico de Pizza - {nome}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
            pdf.image(img_path, x=10, y=30, w=180)

        # Adicionar o gráfico de dispersão ao PDF
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.cell(200, 10, text="Gráfico de Dispersão", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.image(dispersao_img_path, x=10, y=30, w=180)

        # Adicionar a tabela em uma nova página
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.cell(200, 10, text="Tabela de Presenças", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(10)

        # Cabeçalhos da tabela
        pdf.set_font("Helvetica", size=10)
        pdf.cell(60, 10, text="Nome", border=1)
        pdf.cell(60, 10, text="Tipo de Presença", border=1)
        pdf.cell(60, 10, text="Data", border=1)
        pdf.ln()

        # Consultar os dados para a tabela
        query_tabela = """
            SELECT 
                Nome.Nome, 
                Presenca.Presenca, 
                FORMAT(Controle.Data, 'dd/MM/yyyy') AS Data
            FROM 
                (Controle
            INNER JOIN 
                Nome ON Controle.id_Nome = Nome.id_Nomes)
            INNER JOIN 
                Presenca ON Controle.id_Presenca = Presenca.id_Presenca
            WHERE 
                Controle.id_SiteEmpresa = ? AND MONTH(Controle.Data) = ? AND YEAR(Controle.Data) = ?
            ORDER BY 
                Controle.Data;
        """
        cursor.execute(query_tabela, (self.selected_siteempresa_id, mes, ano))

        # Adicionar os dados da tabela ao PDF e armazenar em uma lista para salvar em Excel
        tabela_dados = []
        for row in cursor.fetchall():
            pdf.cell(60, 10, text=row[0], border=1)
            pdf.cell(60, 10, text=row[1], border=1)
            pdf.cell(60, 10, text=row[2], border=1)
            pdf.ln()
            tabela_dados.append([row[0], row[1], row[2]])  # Assegurar que cada item seja uma lista de 3 elementos

        # Salvar o PDF no diretório de downloads
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        pdf_filename = f"relatorio_{self.mes_combobox.get()}_{self.ano_combobox.get()}.pdf"
        pdf_filepath = os.path.join(downloads_path, pdf_filename)
        pdf.output(pdf_filepath)

        # Remover as imagens temporárias
        for _, img_path in imagens_pizza:
            os.remove(img_path)
        os.remove(dispersao_img_path)

        # Salvar a tabela em um arquivo Excel
        df = pd.DataFrame(tabela_dados, columns=["Nome", "Tipo de Presença", "Data"])
        excel_filename = f"tabela_presencas_{self.mes_combobox.get()}_{self.ano_combobox.get()}.xlsx"
        excel_filepath = os.path.join(downloads_path, excel_filename)
        df.to_excel(excel_filepath, index=False)

        # Mostrar mensagem de confirmação
        messagebox.showinfo("Sucesso", f"PDF e Excel salvos com sucesso em: {downloads_path}")

        # Abrir a pasta Downloads
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(f'explorer "{downloads_path}"')
            elif os.name == 'posix':  # macOS, Linux
                subprocess.Popen(['xdg-open', downloads_path])
        except Exception as e:
            print(f"Erro ao abrir a pasta Downloads: {e}")

    def criar_grafico_dispersao_pdf(self):
        # Obter os dados de presença para o gráfico de dispersão
        cursor = self.conn.cursor()
        query = """
            SELECT 
                Nome.Nome,
                Controle.Data,
                Presenca.Presenca
            FROM 
                (Controle
            INNER JOIN 
                Nome ON Controle.id_Nome = Nome.id_Nomes)
            INNER JOIN 
                Presenca ON Controle.id_Presenca = Presenca.id_Presenca
            WHERE 
                Controle.id_SiteEmpresa = ? AND MONTH(Controle.Data) = ? AND YEAR(Controle.Data) = ?
            ORDER BY Controle.Data
        """
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = int(self.ano_combobox.get())
        cursor.execute(query, (self.selected_siteempresa_id, mes, ano))

        # Preparar os dados para o gráfico de dispersão
        data_dict = {
            'OK': {'datas': [], 'nomes': [], 'cor': '#333', 'marker': 'o'},
            'FALTA': {'datas': [], 'nomes': [], 'cor': '#FF5733', 'marker': 'x'},
            'ATESTADO': {'datas': [], 'nomes': [], 'cor': '#FFC300', 'marker': 'd'},
            'CURSO': {'datas': [], 'nomes': [], 'cor': '#8E44AD', 'marker': '*'},
            'FÉRIAS': {'datas': [], 'nomes': [], 'cor': '#A5A5A5', 'marker': 's'},
            'ALPHAVILLE':{'datas': [], 'nomes': [], 'cor': '#ccc', 'marker': 's'},
        }

        nomes_unicos = set()
        for row in cursor.fetchall():
            nome = row[0]
            data = row[1]
            presenca = row[2].upper()

            nomes_unicos.add(nome)  # Armazena os nomes únicos para o eixo Y
            if presenca in data_dict:
                data_dict[presenca]['datas'].append(data)
                data_dict[presenca]['nomes'].append(nome)

        # Criar uma lista de todos os dias úteis no mês
        cal = calendar.Calendar()
        dias_uteis = [datetime.date(ano, mes, day) for day, weekday in cal.itermonthdays2(ano, mes) if
                      day != 0 and weekday < 5]

        # Criando a figura do gráfico com fundo branco
        figura_dispersao = plt.Figure(figsize=(6, 4), facecolor='white')
        ax = figura_dispersao.add_subplot(111)

        # Plotar os dados
        for tipo, info in data_dict.items():
            if info['datas']:
                # Para que os nomes apareçam corretamente no eixo Y, eles precisam ser numericamente codificados
                y_positions = [list(nomes_unicos).index(nome) + 1 for nome in info['nomes']]
                ax.scatter(info['datas'], y_positions, color=info['cor'], label=tipo, marker=info['marker'])

        ax.set_yticks(range(1, len(nomes_unicos) + 1))
        ax.set_yticklabels(list(nomes_unicos), fontsize=8, color='black')  # Nomes no eixo Y

        # Configurar o eixo X para mostrar apenas os dias úteis
        ax.set_xticks(dias_uteis)  # Define os dias úteis como pontos no eixo X
        ax.set_xticklabels([date.strftime('%d') for date in dias_uteis], fontsize=8, color='black')

        # Customizar o fundo do gráfico e os elementos
        ax.set_facecolor('white')  # Fundo branco
        figura_dispersao.patch.set_facecolor('white')
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.tick_params(axis='x', colors='black')  # X ticks pretos
        ax.tick_params(axis='y', colors='black')  # Y ticks pretos

        # Adicionar a legenda
        legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor='white', edgecolor='black', fontsize=8)
        for text in legend.get_texts():
            text.set_color("black")

        # Salvar a figura como imagem
        dispersao_img_path = os.path.join(os.path.expanduser("~"), "dispersion_chart.png")
        figura_dispersao.savefig(dispersao_img_path, dpi=300, bbox_inches='tight')

        return dispersao_img_path

    def criar_grafico_pizza_por_nome_pdf(self):
        # Obter os nomes e presenças relacionados
        cursor = self.conn.cursor()
        query = """
            SELECT 
                Nome.Nome,
                SUM(IIF(Presenca.Presenca = 'ok', 1, 0)) AS ok,
                SUM(IIF(Presenca.Presenca = 'falta', 1, 0)) AS falta,
                SUM(IIF(Presenca.Presenca = 'atestado', 1, 0)) AS atestado,
                SUM(IIF(Presenca.Presenca = 'curso', 1, 0)) AS curso,
                SUM(IIF(Presenca.Presenca = 'férias', 1, 0)) AS ferias
            FROM 
                (Controle
            INNER JOIN 
                Nome ON Controle.id_Nome = Nome.id_Nomes)
            INNER JOIN 
                Presenca ON Controle.id_Presenca = Presenca.id_Presenca
            WHERE 
                Controle.id_SiteEmpresa = ? AND MONTH(Controle.Data) = ? AND YEAR(Controle.Data) = ?
            GROUP BY 
                Nome.Nome;
        """
        mes = list(self.app.meses_dict.keys())[list(self.app.meses_dict.values()).index(self.mes_combobox.get())]
        ano = int(self.ano_combobox.get())
        cursor.execute(query, (self.selected_siteempresa_id, mes, ano))

        # Armazenar os caminhos das imagens geradas para cada nome
        imagens_pizza = []

        # Iterar sobre os resultados e criar um gráfico de pizza para cada nome
        for row in cursor.fetchall():
            nome = row[0]
            sizes = [row[1], row[2], row[3], row[4], row[5]]
            labels = ['OK', 'Falta', 'Atestado', 'Curso', 'Férias']
            colors = ['#333', '#FF5733', '#FFC300', '#8E44AD', '#A5a5a5']

            # Filtrar as categorias com base em valores diferentes de zero
            filtered_labels = []
            filtered_sizes = []
            filtered_colors = []

            for i in range(len(sizes)):
                if sizes[i] > 0:
                    filtered_labels.append(labels[i])
                    filtered_sizes.append(sizes[i])
                    filtered_colors.append(colors[i])

            # Criar gráfico de pizza apenas se houver valores
            if filtered_sizes:
                figura = plt.Figure(figsize=(4, 4), facecolor='white')
                ax = figura.add_subplot(111)

                wedges, texts, autotexts = ax.pie(
                    filtered_sizes, labels=filtered_labels, colors=filtered_colors,
                    autopct=lambda p: f'{int(p * sum(filtered_sizes) / 100)}',
                    startangle=0, pctdistance=0.8,
                    wedgeprops=dict(width=0.4)
                )

                for text in autotexts:
                    text.set_color('black')
                    text.set_fontsize(12)

                for text in texts:
                    text.set_color('black')
                    text.set_fontsize(12)

                ax.axis('equal')
                ax.set_facecolor('white')
                figura.patch.set_facecolor('white')

                # Salvar a figura como imagem
                img_path = os.path.join(os.path.expanduser("~"), f"pizza_chart_{nome}.png")
                figura.savefig(img_path, dpi=300, bbox_inches='tight')
                imagens_pizza.append((nome, img_path))

        return imagens_pizza


# Para rodar o app:
if __name__ == "__main__":
    root = ctk.CTk()
    app = ControleApp(root)
    root.mainloop()