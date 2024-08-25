import customtkinter as ctk
import pyodbc
from tkinter import ttk
from tkinter import messagebox  # Importando o messagebox do tkinter
import datetime
class ControleApp:
    def __init__(self, root):
        self.root = root
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

    def connect_to_db(self):
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

    def get_nomes(self, siteempresa_id):
        """Obtém os nomes associados ao ID_SiteEmpresas."""
        cursor = self.conn.cursor()
        query = """
            SELECT Nome.Nome
            FROM Nome
            WHERE id_SiteEmpresa = ?
        """
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
        button_texts = ["Controle de Frequencia", "Empresas", "Relatorio Mensal"]

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
                button.configure(fg_color='transparent', border_color=self.my_dict['menu-sup'])

        # Adiciona novo conteúdo baseado no botão pressionado
        if frame_name == "Controle de Frequencia":
            if self.selected_siteempresa_id:
                Aba_Controle(self, self.frame_tela, self.my_dict, self.conn, self.selected_siteempresa_id)
            else:
                self.show_initial_message()
        elif frame_name == "Relatorio Mensal":
            if self.selected_siteempresa_id:
                Aba_relatorio_mes(self, self.frame_tela, self.my_dict, self.conn, self.selected_siteempresa_id)
            else:
                self.show_initial_message()
        elif frame_name == "Empresas":
            if self.selected_siteempresa_id:
                Aba_empresas(self, self.frame_tela, self.my_dict, self.conn, self.selected_siteempresa_id)
            else:
                self.show_initial_message()


class Aba_Controle:
    def __init__(self, app, frame, my_dict, conn, selected_siteempresa_id):
        self.app = app
        self.frame = frame
        self.my_dict = my_dict
        self.conn = conn
        self.selected_siteempresa_id = selected_siteempresa_id

        self.setup()

    def setup(self):
        # Obter os nomes relacionados ao ID_SiteEmpresas
        nomes = self.app.get_nomes(self.selected_siteempresa_id)

        # Exibir os nomes na aba de controle
        label = ctk.CTkLabel(self.frame, text=f"Nomes associados ao site e empresa selecionados:", text_color=self.my_dict['font'])
        label.pack(pady=10)

        self.frame_checkbox = ctk.CTkFrame(self.frame, fg_color=self.my_dict['preto'],height=50)
        self.frame_checkbox.pack(pady=10, padx=10, fill='x')

        self.checkbox_vars = {}  # Dicionário para armazenar as variáveis das checkboxes
        row, col = 0, 0
        max_columns = 9  # Defina o número máximo de colunas por linha

        for nome in nomes:
            var = ctk.StringVar(value='off')
            checkbox = ctk.CTkCheckBox(self.frame_checkbox, text=nome, variable=var, onvalue='on', offvalue='off', font=('Arial', 15), hover_color=self.my_dict['Heading_color'])
            checkbox.grid(row=row, column=col, padx=5, pady=5)
            self.checkbox_vars[nome] = var  # Armazena a variável da checkbox
            col += 1

            if col >= max_columns:
                col = 0
                row += 1
class Aba_empresas:
    def __init__(self, app, frame, my_dict, conn, selected_siteempresa_id):
        self.app = app
        self.frame = frame
        self.my_dict = my_dict
        self.conn = conn
        self.selected_siteempresa_id = selected_siteempresa_id
        self.setup()

    def setup(self):
        label = ctk.CTkLabel(self.frame, text="Gerenciar Empresas e Nomes", text_color=self.my_dict['font'])
        label.pack(pady=20)
        
        # Frame para o conteúdo de Nomes
        self.frame_input_nome = ctk.CTkFrame(self.frame, fg_color=self.my_dict['preto'])
        self.frame_input_nome.pack(pady=10, padx=10, fill='both', expand=True,side='left')

        # Inserir Nome
        nome_label = ctk.CTkLabel(self.frame_input_nome, text="Inserir Nome:", text_color=self.my_dict['font'])
        nome_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.nome_entry = ctk.CTkEntry(self.frame_input_nome, fg_color=self.my_dict['preto'],
                                       placeholder_text="Insira o Nome aqui!", placeholder_text_color=self.my_dict['frames_ajuste'])
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        button_add_nome = ctk.CTkButton(self.frame_input_nome, text="Adicionar Nome", fg_color=self.my_dict['adicionar_btn'], command=self.add_nome)
        button_add_nome.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Remover Nome
        nome_label_remove = ctk.CTkLabel(self.frame_input_nome, text="Remover Nome:", text_color=self.my_dict['font'])
        nome_label_remove.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.nome_combobox = ctk.CTkComboBox(self.frame_input_nome, values=self.app.get_nomes(self.selected_siteempresa_id), state='readonly')
        self.nome_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        button_remove_nome = ctk.CTkButton(self.frame_input_nome, text="Remover Nome", fg_color=self.my_dict['remover_btn'], command=self.remover_nome)
        button_remove_nome.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        
        # Frame para o conteúdo de Empresas
        self.frame_input_empresa = ctk.CTkFrame(self.frame, fg_color=self.my_dict['preto'])
        self.frame_input_empresa.pack(pady=10, padx=10, fill='both', expand=True, side='left')
        
        # Inserir Empresa
        empresa_label = ctk.CTkLabel(self.frame_input_empresa, text="Inserir Empresa:", text_color=self.my_dict['font'])
        empresa_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.empresa_entry = ctk.CTkEntry(self.frame_input_empresa, fg_color=self.my_dict['preto'], placeholder_text="Insira a empresa aqui!",placeholder_text_color=self.my_dict['frames_ajuste'])
        self.empresa_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        button_add_empresa = ctk.CTkButton(self.frame_input_empresa, text="Adicionar Empresa", fg_color=self.my_dict['adicionar_btn'], command=self.add_empresa)
        button_add_empresa.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Desativar Empresa
        empresa_label_remove = ctk.CTkLabel(self.frame_input_empresa, text="Desativar Empresa:", text_color=self.my_dict['font'])
        empresa_label_remove.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.empresa_combobox = ctk.CTkComboBox(self.frame_input_empresa, values=self.get_empresas_ativas(), state='readonly')
        self.empresa_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        button_remove_empresa = ctk.CTkButton(self.frame_input_empresa, text="Desativar", fg_color=self.my_dict['remover_btn'], command=self.desativar_empresa)
        button_remove_empresa.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Ativar Empresa
        empresa_label_activate = ctk.CTkLabel(self.frame_input_empresa, text="Ativar Empresa:", text_color=self.my_dict['font'])
        empresa_label_activate.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.empresa_inativa_combobox = ctk.CTkComboBox(self.frame_input_empresa, values=self.get_empresas_inativas(), state='readonly')
        self.empresa_inativa_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        button_ativar_empresa = ctk.CTkButton(self.frame_input_empresa, text="Ativar", fg_color=self.my_dict['adicionar_btn'], command=self.ativar_empresa)
        button_ativar_empresa.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        # Ajustar colunas para se expandirem igualmente
        self.frame_input_nome.grid_columnconfigure(1, weight=1)
        self.frame_input_empresa.grid_columnconfigure(1, weight=1)

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
        """Ativa uma empresa inativa."""
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
            
            # Atualizar o campo Ativo para True na tabela Site_Empresa
            cursor.execute("UPDATE Site_Empresa SET Ativo = True WHERE id_Sites = ? AND id_Empresas = ?", (self.app.selected_site_id, empresa_id))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Empresa ativada com sucesso!")

            # Atualizar a combobox de empresas inativas e ativas
            self.empresa_inativa_combobox['values'] = self.get_empresas_inativas()
            self.empresa_combobox['values'] = self.get_empresas_ativas()

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao ativar empresa: {e}")

    def remover_nome(self):
        """Remove um nome da tabela Nome."""
        nome = self.nome_combobox.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Selecione um nome para remover.")
            return

        try:
            cursor = self.conn.cursor()

            # Remover o nome da tabela Nome com base no id_SiteEmpresa e no nome
            cursor.execute("DELETE FROM Nome WHERE Nome = ? AND id_SiteEmpresa = ?", (nome, self.selected_siteempresa_id))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Nome removido com sucesso!")

            # Atualizar a combobox de nomes
            self.nome_combobox['values'] = self.app.get_nomes(self.selected_siteempresa_id)

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao remover nome: {e}")

    def desativar_empresa(self):
        """Torna uma empresa não ativa."""
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

            cursor = self.conn.cursor()

            # Desativar a empresa na tabela Site_Empresa
            cursor.execute("UPDATE Site_Empresa SET Ativo = False WHERE id_Sites = ? AND id_Empresas = ?", (self.app.selected_site_id, empresa_id))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Empresa desativada com sucesso!")

            # Atualizar a combobox de empresas ativas e inativas
            self.empresa_combobox['values'] = self.get_empresas_ativas()
            self.empresa_inativa_combobox['values'] = self.get_empresas_inativas()

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao desativar empresa: {e}")

    def add_nome(self):
        # Recuperar o nome inserido
        nome = self.nome_entry.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "O nome não pode estar vazio.")
            return

        try:
            cursor = self.conn.cursor()

            # Inserir o nome na tabela Nome usando o id_SiteEmpresa selecionado
            cursor.execute("INSERT INTO Nome (Nome, id_SiteEmpresa) VALUES (?, ?)", (nome, self.selected_siteempresa_id))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Nome adicionado com sucesso!")

            # Limpar as entradas
            self.nome_entry.delete(0, 'end')

            # Atualizar a combobox de nomes
            self.nome_combobox['values'] = self.app.get_nomes(self.selected_siteempresa_id)

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao adicionar nome: {e}")

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
            cursor.execute("INSERT INTO Site_Empresa (id_Sites, id_Empresas, Ativo) VALUES (?, ?, True)", (id_site, id_empresa))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Empresa adicionada com sucesso!")

            # Limpar as entradas
            self.empresa_entry.delete(0, 'end')

            # Atualizar a combobox de empresas ativas e inativas
            self.empresa_combobox['values'] = self.get_empresas_ativas()
            self.empresa_inativa_combobox['values'] = self.get_empresas_inativas()

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao adicionar empresa: {e}")

class Aba_relatorio_mes:
    def __init__(self, app, frame, my_dict, conn, selected_siteempresa_id):
        self.app = app
        self.frame = frame
        self.my_dict = my_dict
        self.conn = conn
        self.selected_siteempresa_id = selected_siteempresa_id
        self.setup()

    def setup(self):
        label = ctk.CTkLabel(self.frame, text=f"Relatório Mensal para o site e empresa selecionados", text_color=self.my_dict['font'])
        label.pack(pady=20)
        
        filtro_frame = ctk.CTkFrame(self.frame, width=160, fg_color=self.my_dict['menu-inf'], bg_color=self.my_dict['preto'])
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

# Para rodar o app:
if __name__ == "__main__":
    root = ctk.CTk()
    app = ControleApp(root)
    root.mainloop()
