import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import os
#import subprocess
import pyodbc


class SimpleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.input_value = ctk.StringVar()  # Variável para armazenar o valor do input
        self.conn = self.connect_to_db()  # Conectar ao banco de dados
        self.path_ = ''
        self.my_dic = {
            'Frame_Preto': '#222',
            'Vermelho_Brad': '#cc092f',
            'Frame_Ajsute': '#666',
            'font': '#c2c2c2',
        }
        self.month_map = {
            '01': '01 - JANEIRO',
            '02': '02 - FEVEREIRO',
            '03': '03 - MARÇO',
            '04': '04 - ABRIL',
            '05': '05 - MAIO',
            '06': '06 - JUNHO',
            '07': '07 - JULHO',
            '08': '08 - AGOSTO',
            '09': '09 - SETEMBRO',
            '10': '10 - OUTUBRO',
            '11': '11 - NOVEMBRO',
            '12': '12 - DEZEMBRO'
        }
        self.title("Algoritmo de busca de OS")
        self.style_treeview = ttk.Style()

        self.geometry("500x500")
        self._set_appearance_mode('System')
        self.minsize(width=500, height=500)
        self.maxsize(width=500, height=500)

        # Frame principal
        self.frame = ctk.CTkFrame(self, width=60, height=60)
        self.frame.pack(fill='both', expand=True)

        # Adicionando um rótulo simples
        self.label = ctk.CTkLabel(self.frame, text="Código OS:")
        self.label.grid(row=0, column=0, padx=50, pady=10, sticky='e')

        entry = ctk.CTkEntry(self.frame, textvariable=self.input_value, width=300)
        entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='w')

        # Tipo Combobox
        self.label_tipo = ctk.CTkLabel(self.frame, text="Tipo da OS:")
        self.label_tipo.grid(row=1, column=0, padx=50, pady=10, sticky='e')

        self.tipo_combobox = ctk.CTkComboBox(self.frame, values=[], state='readonly')
        self.tipo_combobox.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.site_combobox = ctk.CTkComboBox(self.frame, values=[], state='readonly')
        self.site_combobox.grid(row=1, column=2, padx=10, pady=10, sticky='w')

        self.label_cat = ctk.CTkLabel(self.frame, text="Categoria da OS:")
        self.label_cat.grid(row=2, column=0, padx=25, pady=10, sticky='e')

        self.categoria_primaria = ctk.CTkComboBox(self.frame, values=[], state='readonly', command=self.trocar_combobox)
        self.categoria_primaria.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        self.categoria_secundaria = ctk.CTkComboBox(self.frame, values=[], state='readonly')
        self.categoria_secundaria.grid(row=2, column=2, padx=10, pady=10, sticky='w')

        button = ctk.CTkButton(self.frame, text="Buscar Arquivo", command=self.separar_input)
        button.grid(row=3, column=2, padx=0, pady=20)

        # Botão para abrir nova janela
        self.new_window_button = ctk.CTkButton(self.frame, text="Abrir Nova Janela", command=self.abrir_nova_janela)
        self.new_window_button.grid(row=3, column=1, padx=0, pady=20)

        # Tabela (Treeview) - frame
        tabela_frame = ctk.CTkFrame(self, fg_color=self.my_dic['Frame_Preto'])
        tabela_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.tabela = ttk.Treeview(tabela_frame, columns="Diretorio", show='headings')

        self.treeScrollbar = ctk.CTkScrollbar(tabela_frame, command=self.tabela.yview)
        self.treeScrollbar.pack(side='right', fill='y')

        # Configuração da tabela
        self.tabela.configure(yscrollcommand=self.treeScrollbar.set)
        self.style_treeview.theme_use('alt')
        self.style_treeview.configure("Treeview.Heading", background=self.my_dic['Frame_Preto'],
                                      foreground=self.my_dic['font'], borderwidth=1, relief='solid',
                                      font=('Arial', 10))
        self.style_treeview.map("Treeview.Heading", background=[('active', self.my_dic['Vermelho_Brad'])])
        self.style_treeview.configure("Treeview", background=self.my_dic['Frame_Preto'],
                                      foreground=self.my_dic['font'], fieldbackground=self.my_dic['Frame_Preto'],
                                      rowheight=25, borderwidth=1, relief='solid')
        self.style_treeview.map("Treeview", background=[('selected', self.my_dic['Vermelho_Brad'])],
                                fieldbackground=[('!selected', self.my_dic['Frame_Preto'])])

        self.tabela.heading("Diretorio", text="Diretorio")
        self.tabela.pack(fill='both', expand=True)

        self.center_window(500, 500)

        self.tabela.bind("<ButtonRelease-1>", self.linha_selecionada_treeview)

        # Carregar os valores dos comboboxes
        self.carregar_combobox_tipo()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f'{width}x{height}+{x}+{y}')

    @staticmethod
    def connect_to_db():
        try:
            con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Henrique\OneDrive\Anexos\Venv_projects\Busca_OS\BD_ANOS.accdb'
            conn = pyodbc.connect(con_string)
            return conn
        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
            return None

    def carregar_combobox_tipo(self):
        if self.conn:
            cursor = self.conn.cursor()
            try:

                # combobox OS
                cursor.execute("SELECT * FROM tblOS")
                tipos = [row[0] for row in cursor.fetchall()]
                self.tipo_combobox.configure(values=tipos)
                self.tipo_combobox.set(tipos[1])

                # combobox sites
                cursor.execute("SELECT * FROM tblSITES")
                sites = [row[0] for row in cursor.fetchall()]
                self.site_combobox.configure(values=sites)
                self.site_combobox.set(sites[0])

                # Combobox categoria_primaria
                cursor.execute("SELECT * FROM tblCATPRIM")
                categorias_primarias = [row[0] for row in cursor.fetchall()]
                self.categoria_primaria.configure(values=categorias_primarias)
                # self.categoria_primaria.set(categorias_primarias[0])

            except pyodbc.Error as e:
                messagebox.showerror("Erro", f"Erro ao carregar dados para o tipo_combobox: {e}")
            finally:
                cursor.close()
        else:
            messagebox.showerror("Erro", "Não foi possível estabelecer conexão com o banco de dados.")

    def filtrar_acesso(self, ano, mes, tipo_os, site, categoria_primaria, categoria_secundaria):
        try:
            cursor = self.conn.cursor()

            # Consulta para verificar se há categoria_secundaria não nula (None) para a combinação fornecida
            verificar_query = """
                SELECT COUNT(*)
                FROM Procura
                WHERE ANOS = ?
                  AND MES = ?
                  AND OS = ?
                  AND SITES = ?
                  AND [CATEGORIA_PRIMARIA] = ?
                  AND [CATEGORIA_SECUNDARIA] IS NOT NULL
            """
            cursor.execute(verificar_query, (ano, mes, tipo_os, site, categoria_primaria))
            count = cursor.fetchone()[0]

            # Se existir categoria_secundaria não nula (None), exibir mensagem de erro
            if count > 0 and not categoria_secundaria:
                messagebox.showerror("Erro", "Você deve selecionar uma categoria secundária.")
                cursor.close()
                return None

            # Construção da consulta principal
            base_query = """
                SELECT * FROM Procura
                WHERE ANOS = ?
                  AND MES = ?
                  AND OS = ?
                  AND SITES = ?
                  AND [CATEGORIA_PRIMARIA] = ?
            """

            # Adicionar categoria_secundaria à consulta se estiver preenchida
            if categoria_secundaria:
                base_query += " AND [CATEGORIA_SECUNDARIA] = ?"
                params = (ano, mes, tipo_os, site, categoria_primaria, categoria_secundaria)
            else:
                params = (ano, mes, tipo_os, site, categoria_primaria)

            cursor.execute(base_query, params)
            resultados = cursor.fetchall()

            # Fechar o cursor
            cursor.close()

            # Imprimir as duas últimas colunas dos resultados
            self.imprimir_ultimas_colunas(resultados)

            return resultados

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao filtrar dados: {e}")
            return None

    def imprimir_ultimas_colunas(self, resultados):
        print('\n', '-'*10, ' Imprimir as colunas \'ALVO\' ', '-'*10)
        if resultados:
            for row in resultados:
                print(f'\n [PATH]: {row[-2]}\n [CODIGO OS]: {row[-3]}\n [PATH_erro]: {row[-1]}\n')

                path = row[-2]
                code_os = row[-3]
                path_erro = row[-1]

                self.encontrar_os_path(path, code_os, path_erro)
        else:
            print("Nenhum resultado encontrado.")
            self.tabela.delete(*self.tabela.get_children())
            messagebox.showwarning("Aviso", "Nenhuma OS encontrada")

    def encontrar_os_path(self, path, code_os, path_erro):
        # Executa o os.listdir e adiciona os itens na Treeview
        lista_path = os.listdir(path)
        self.adiciona_itens_tabela(self.tabela, lista_path)

        if path_erro:
            # Se PATH_erro for True, apenas abre o diretório sem procurar pelo item específico
            #subprocess.run(['explorer', path], shell=True)
            messagebox.showinfo("Pasta aberta", f"O caminho foi aberto: {path}")
            return

        # Caso PATH_erro seja False, procura pelo item específico e abre o diretório correspondente
        os_ = code_os + self.input_value.get()
        os_space = code_os + ' ' + self.input_value.get()

        for item in lista_path:
            if item.startswith(os_) or item.startswith(os_space):
                print('\n', '*' * 10, ' encontrar_os_path [item solicitado] ', '*' * 10, f'\n Item: {item} \n')
                self.path_ = path
                path_ = os.path.join(path, item)
                #subprocess.run(['explorer', path_], shell=True)
                messagebox.showinfo("Pasta aberta", f"O caminho foi aberto: {path_}")
                break

    def linha_selecionada_treeview(self, event):
        # Capturar a seleção na Treeview
        for selected_item in self.tabela.selection():
            item = self.tabela.item(selected_item)
            record = item['values']

            # Concatena o path_ com o valor selecionado na Treeview
            path_selecionado = os.path.join(self.path_, record[0])

            # Abre o diretório no Explorer
            try:
                #subprocess.run(['explorer', path_selecionado], shell=True)
                return messagebox.showinfo("Resultado", f"Pasta aberta: {path_selecionado}")
            except Exception as e:
                return messagebox.showerror("Erro", f"Erro ao abrir a pasta: {e}")

    def adiciona_itens_tabela(self, treeview, lista_paths):
        treeview.delete(*treeview.get_children())
        for item in lista_paths:
            treeview.insert('', 'end', values=[item])

    def trocar_combobox(self, choice):
        if choice == 'CABEAMENTO':
            self.categoria_secundaria.configure(values=['', 'OPEN', 'MAINFRAME'])
        elif choice == 'MANUTENÇÃO':
            self.categoria_secundaria.configure(values=['', 'CORRETIVA', 'PREVENTIVA'])
        else:
            self.categoria_secundaria.configure(values=[''])

        self.categoria_secundaria.set('')

    def trocar_combobox_nova_janela(self, choice, categoria_secundaria_combobox):
        if choice == 'CABEAMENTO':
            categoria_secundaria_combobox.configure(values=['', 'OPEN', 'MAINFRAME'])
        elif choice == 'MANUTENÇÃO':
            categoria_secundaria_combobox.configure(values=['', 'CORRETIVA', 'PREVENTIVA'])
        else:
            categoria_secundaria_combobox.configure(values=[''])

        categoria_secundaria_combobox.set('')

    def separar_input(self):
        input_str = self.input_value.get()

        # If input length is exactly 7, perform the primary search
        if len(input_str) == 7:
            ano = '20' + input_str[:2]
            mes = input_str[2:4]
            mes_nome = self.month_map.get(mes, None)
            num = input_str[4:]
            if not mes_nome:
                return messagebox.showerror("Erro", "Mês inválido no código OS.")

            tipo_os = self.tipo_combobox.get()
            site = self.site_combobox.get()
            categoria_primaria = self.categoria_primaria.get()
            categoria_secundaria = self.categoria_secundaria.get()

            print('=' * 30, ' | Separar_input - Primeira Busca | ', '=' * 30)
            print(f'\n Ano: {ano} |\t Mês: {mes_nome} |\tNúmero: {num}')
            print(
                f'\n Tipo OS: {tipo_os}\n Site: {site}\n Categoria Primária: {categoria_primaria}\n Categoria Secundária: {categoria_secundaria}\n')

            # Attempt the primary search
            resultados = self.filtrar_acesso(ano, mes_nome, tipo_os, site, categoria_primaria, categoria_secundaria)

            # If no results and input string is longer than 7 characters, attempt secondary search
            if not resultados and len(input_str) > 7:
                print("Nenhum resultado encontrado. Iniciando segunda busca em OS_Referencia_Teste...")
                self.query_os_referencia_teste(input_str)

        # If input length is greater than 7, directly go to the secondary search
        elif len(input_str) > 7:
            print('=' * 30, ' | Separar_input - Segunda Busca | ', '=' * 30)
            print(f'Input excede 7 caracteres: {input_str}')
            print("Iniciando busca em OS_Referencia_Teste...")
            self.query_os_referencia_teste(input_str)

        # If input length is less than 7, show an error
        else:
            return messagebox.showerror("Erro", "Formato inválido. O input deve ter 7 caracteres.")

    def query_os_referencia_teste(self, input_str):
        try:
            cursor = self.conn.cursor()
            input_str_trimmed = input_str[:-3]
            print(input_str_trimmed)

            # Construct the query to search in "OS_Referencia_Teste"
            query = f"""
                SELECT 
                    [CODIGO OS] & Mid(CStr([ANOS]),3,2) & Left([MES],2) AS OS_Referencia, 
                    Procura.Código AS Codigo, 
                    Procura.[CATEGORIA_PRIMARIA] AS Categoria_Primaria_OS, 
                    Procura.[CATEGORIA_SECUNDARIA] AS Categoria_Secundaria_OS, 
                    Procura.SITES,
                    Procura.OS,
                    Procura.PATH, 
                    Procura.PATH_error
                FROM Procura
                WHERE ((([CODIGO OS] & Mid(CStr([ANOS]),3,2) & Left([MES],2))='{input_str_trimmed}'));
            """

            cursor.execute(query)
            resultados = cursor.fetchall()
            print(resultados)
            cursor.close()

            # Handle the results as necessary
            if resultados:
                print("Resultados encontrados na tabela OS_Referencia_Teste:")
                for row in resultados:
                    print(row)
                    self.tipo_combobox.set(row[5])
                    self.site_combobox.set(row[4])
                    self.categoria_primaria.set(row[2])
                    self.categoria_secundaria.set(row[3])

                    # You can add logic here to handle the retrieved rows.
                    # Example: self.tabela.insert("", "end", values=row)
                self.imprimir_ultimas_colunas(resultados)
            else:
                print("Nenhum resultado encontrado na tabela OS_Referencia_Teste.")
                self.tabela.delete(*self.tabela.get_children())

        except pyodbc.Error as e:
            print(f"Erro ao consultar a tabela OS_Referencia_teste: {e}")

    # Updated method to handle inserting/updating the OS
    def cadastrar_os(self):
        cursor = self.conn.cursor()

        # Obter os valores dos campos diretamente
        tipo_os = self.tipo_combobox_nova.get()
        site = self.site_combobox_nova.get()
        ano = self.ano_combobox_nova.get()
        mes = self.mes_combobox_nova.get()
        categoria_primaria = self.categoria_primaria_nova.get()
        categoria_secundaria = self.categoria_secundaria_nova.get()
        path = self.path_entry.get()
        codigo_os = self.codigo_os_entry.get()

        # Verificar se o caminho especificado é válido
        if not os.path.exists(path):
            messagebox.showerror("Erro", "O caminho especificado não é válido. Verifique o caminho e tente novamente.")
            self.input_value.set('')
            return  # Não continuar o código se o caminho for inválido

        try:
            # Verificar se o ano está na tabela relacionada, caso contrário, inserir
            cursor.execute("SELECT COUNT(*) FROM tblANOS WHERE ANOS = ?", (ano,))
            ano_existe = cursor.fetchone()[0]
            if not ano_existe:
                cursor.execute("INSERT INTO tblANOS (ANOS) VALUES (?)", (ano,))
                self.conn.commit()

            # Verificar se já existe uma linha com os mesmos valores
            verificar_query = """
                SELECT * FROM Procura
                WHERE OS = ? AND SITES = ? AND ANOS = ? AND MES = ? AND CATEGORIA_PRIMARIA = ? AND CATEGORIA_SECUNDARIA = ?
            """
            cursor.execute(verificar_query, (tipo_os, site, ano, mes, categoria_primaria, categoria_secundaria))
            resultado_existente = cursor.fetchone()
            print(resultado_existente)

            if resultado_existente:
                resposta = messagebox.askyesno("Atualizar OS", "Já existe uma OS com esses valores. Deseja atualizar?")
                if resposta:
                    update_query = """
                        UPDATE Procura
                        SET PATH = ?, PATH_error = ?
                        WHERE OS = ? AND SITES = ? AND ANOS = ? AND MES = ? AND CATEGORIA_PRIMARIA = ? AND CATEGORIA_SECUNDARIA = ?
                    """
                    cursor.execute(update_query, (
                        path, True, tipo_os, site, ano, mes, categoria_primaria, categoria_secundaria))
                    self.conn.commit()
                    messagebox.showinfo("Sucesso", "OS atualizada com sucesso!")
                else:
                    messagebox.showinfo("Ação Cancelada", "A atualização foi cancelada pelo usuário.")
            else:
                # Obter o próximo valor para a chave primária
                cursor.execute("SELECT MAX(Código) FROM Procura")
                max_codigo = cursor.fetchone()[0]
                if max_codigo is None:
                    max_codigo = 0
                novo_codigo = max_codigo + 1

                # Inserir a nova OS se não existir
                insert_query = """
                    INSERT INTO Procura (Código, [CODIGO OS], OS, SITES, ANOS, MES, CATEGORIA_PRIMARIA, CATEGORIA_SECUNDARIA, PATH, PATH_error)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(insert_query, (
                    novo_codigo, codigo_os, tipo_os, site, ano, mes, categoria_primaria, categoria_secundaria, path,
                    True))
                #print(cursor.execute)
                self.conn.commit()
                messagebox.showinfo("Sucesso", "OS inserida com sucesso!")

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao inserir ou atualizar OS: {e}")
            print(e)
        finally:
            cursor.close()

    def abrir_nova_janela(self):

        nova_janela = ctk.CTkToplevel(self)
        nova_janela.title("INSERIR OS")
        nova_janela.geometry("650x300")
        nova_janela.resizable(False, False)

        # Criando os comboboxes na nova janela
        label_tipo_nova = ctk.CTkLabel(nova_janela, text="Tipo da OS:")
        label_tipo_nova.grid(row=0, column=0, padx=20, pady=10)

        self.tipo_combobox_nova = ctk.CTkComboBox(nova_janela, values=self.tipo_combobox.cget("values"), state='readonly')
        self.tipo_combobox_nova.grid(row=0, column=1, padx=10, pady=10)

        label_site_nova = ctk.CTkLabel(nova_janela, text="Site:")
        label_site_nova.grid(row=0, column=2, padx=20, pady=10)

        self.site_combobox_nova = ctk.CTkComboBox(nova_janela, values=self.site_combobox.cget("values"), state='readonly')
        self.site_combobox_nova.grid(row=0, column=3, padx=10, pady=10)

        # Adicionando a ComboBox para o ano
        label_ano_nova = ctk.CTkLabel(nova_janela, text="Ano:")
        label_ano_nova.grid(row=1, column=0, padx=20, pady=10)

        self.ano_combobox_nova = ctk.CTkComboBox(nova_janela, values=[str(i) for i in range(2009, 2101)], state='readonly')
        self.ano_combobox_nova.grid(row=1, column=1, padx=10, pady=10)

        # Adicionando a ComboBox para o mês
        label_mes_nova = ctk.CTkLabel(nova_janela, text="Mês:")
        label_mes_nova.grid(row=1, column=2, padx=20, pady=10)

        self.mes_combobox_nova = ctk.CTkComboBox(nova_janela, values=list(self.month_map.values()), state='readonly')
        self.mes_combobox_nova.grid(row=1, column=3, padx=10, pady=10)

        label_cat_nova = ctk.CTkLabel(nova_janela, text="Categoria Primária:")
        label_cat_nova.grid(row=2, column=0, padx=20, pady=10)

        self.categoria_primaria_nova = ctk.CTkComboBox(nova_janela, values=self.categoria_primaria.cget("values"),
                                                  state='readonly')
        self.categoria_primaria_nova.grid(row=2, column=1, padx=10, pady=10)

        label_cat_sec_nova = ctk.CTkLabel(nova_janela, text="Categoria Secundária:")
        label_cat_sec_nova.grid(row=2, column=2, padx=20, pady=10)

        self.categoria_secundaria_nova = ctk.CTkComboBox(nova_janela, values=self.categoria_secundaria.cget("values"),
                                                    state='readonly')
        self.categoria_secundaria_nova.grid(row=2, column=3, padx=10, pady=10)

        # Campo de entrada para o caminho com width ajustado e ocupando duas colunas
        label_path = ctk.CTkLabel(nova_janela, text="Caminho:")
        label_path.grid(row=3, column=0, padx=20, pady=10)

        self.path_entry = ctk.CTkEntry(nova_janela)  # Ajuste do width
        self.path_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky='w')
        # Add this in the `abrir_nova_janela` method for creating a new window.
        label_codigo_os = ctk.CTkLabel(nova_janela, text="Código OS:")
        label_codigo_os.grid(row=3, column=2, padx=20, pady=10)

        self.codigo_os_entry = ctk.CTkEntry(nova_janela)
        self.codigo_os_entry.grid(row=3, column=3, padx=10, pady=10)

        # Configuração das colunas para garantir que os botões fiquem nas extremidades
        nova_janela.grid_columnconfigure(0, weight=1)
        nova_janela.grid_columnconfigure(1, weight=1)
        nova_janela.grid_columnconfigure(2, weight=1)
        nova_janela.grid_columnconfigure(3, weight=1)


        # Botão "Inserir OS"
        inserir_os_button = ctk.CTkButton(nova_janela, text="Inserir OS", command=self.cadastrar_os)
        inserir_os_button.grid(row=4, column=3, padx=10, pady=20, sticky='e')

        # Vinculando a função de atualização para o combobox de categoria primária na nova janela
        self.categoria_primaria_nova.configure(
            command=lambda choice: self.trocar_combobox_nova_janela(choice, self.categoria_secundaria_nova))

        self.iconify()


if __name__ == "__main__":
    app = SimpleApp()
    app.mainloop()
