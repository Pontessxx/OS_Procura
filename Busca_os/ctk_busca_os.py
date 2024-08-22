import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import os
import subprocess
from PIL import Image   



console = Console()
class SimpleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('C:\\Users\\Henrique\\OneDrive\\Anexos\\FIAP_2024\\OS_Procura\\Busca_os\\img\\bradimg.ico')
        self.input_value = ctk.StringVar()  # Variável para armazenar o valor do input
        
        self.my_dic = {
            'Frame_Preto': '#222',
            'Vermelho_Brad': '#cc092f',
            'Frame_Ajsute': '#666',
            'font': '#c2c2c2',
        }
        self.iconbitmap('\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\Cabling\\Busca OS\\img\\bradimg.ico')
        self.title("Algoritimo de busca de OS")
        self.style_treeview = ttk.Style()

        self.geometry("500x200")
        self._set_appearance_mode('System')
        self.minsize(width=500,height=500)
        self.maxsize(width=500,height=500)


        # Frame principal
        self.frame = ctk.CTkFrame(self,width=60, height=60)
        self.frame.pack( fill='both', expand=True)
        
        # Adding a simple label
        self.label = ctk.CTkLabel(self.frame, text="Digite o código OS:")
        self.label.grid(row=0, column=0, padx=20, pady=20)
        
        entry = ctk.CTkEntry(self.frame, textvariable=self.input_value)
        entry.grid(row=0, column=1, padx=20, pady=20)
        
        # Site Combobox
        self.site_combobox = ctk.CTkComboBox(self.frame, values=['01 - CTI', '02 - ALPHAVILLE', '03 - XAXIM', '04 - REDE LAN', 'PRÉDIO PRATA E VERMELHO'], state='readonly')
        self.site_combobox.grid(row=0, column=2, padx=20, pady=20)
        # tipo Combobox
        self.label2 = ctk.CTkLabel(self.frame, text="Tipo da OS: ")
        self.label2.grid(row=1, column=0, padx=20, pady=20)
        self.tipo_combobox = ctk.CTkComboBox(self.frame, values=['CABEAMENTO', 'ELÉTRICA', 'MANUTENÇÃO'], state='readonly', command=self.trocar_combobox)
        self.tipo_combobox.grid(row=1, column=1, padx=20, pady=20)

        self.tipo_cabeamento = ctk.CTkComboBox(self.frame, values=[''], state='readonly')
        self.tipo_cabeamento.grid(row=1, column=2, padx=20, pady=20)
        
        # button = ctk.CTkButton(self.frame, image=self.ctk_img_arquivo, text="Buscar Arquivo", command=self.mostrar_resultado)
        button = ctk.CTkButton(self.frame, text="Buscar Arquivo", command=self.mostrar_resultado)
        button.grid(row=2, column=2, padx=20, pady=20, )



        self.site_combobox.set('01 - CTI')
        
        # Tabela (Treeview) - frame
        tabela_frame = ctk.CTkFrame(self, fg_color=self.my_dic['Frame_Preto'])
        tabela_frame.pack(pady=10, padx=10, fill='both', expand=True)


        
        self.tabela = ttk.Treeview(tabela_frame, columns="Diretorio", show='headings',)


        self.treeScrollbar = ctk.CTkScrollbar(tabela_frame,command=self.tabela.yview,)
        self.treeScrollbar.pack(side='right', fill='y',)

        # Tree configuration
        self.tabela.configure(yscrollcommand=self.treeScrollbar.set,)
        self.style_treeview.theme_use('clam')
        self.style_treeview.configure("Treeview.Heading", background=self.my_dic['Frame_Preto'], foreground=self.my_dic['font'], borderwidth=1, relief='solid', font=('Arial', 10))
        self.style_treeview.map("Treeview.Heading", background=[('active', self.my_dic['Vermelho_Brad'])])
        self.style_treeview.configure("Treeview", background=self.my_dic['Frame_Preto'], foreground=self.my_dic['font'], fieldbackground=self.my_dic['Frame_Preto'], rowheight=25, borderwidth=1, relief='solid')
        self.style_treeview.map("Treeview", background=[('selected', self.my_dic['Vermelho_Brad'])], fieldbackground=[('!selected', self.my_dic['Frame_Preto'])])

        self.tabela.heading("Diretorio", text="Diretorio",)
        self.tabela.pack(fill='both', expand=True)

        self.tabela.bind("<ButtonRelease-1>", self.linha_selecionada_treeview)

        self.center_window(500, 500)
        
    def print_section_header(self,title, description):
        """ Função para imprimir cabeçalhos de seção com estilo Markdown usando o rich. """
        title_text = Text(title, style="bold yellow")
        description_text = Text(description, style="white")
        panel = Panel(description_text, title=title_text, border_style="green")
        console.print(panel)

    def linha_selecionada_treeview(self, event):
        for selected_item in self.tabela.selection():
            item = self.tabela.item(selected_item)
            record = item['values']
            self.path = self.path + '\\' + record[0]
            self.print_section_header("TREEVIEW SELECIONADA", f"\n\n- {item}\n\n- {record}\n\n- {self.base_path}\n\n- {self.path}")
            subprocess.run(['explorer', self.path], shell=True)
            return messagebox.showinfo("Resultado", f"Pasta aberta: {self.path}")

    def add_items_to_treeview(self, treeview, lista_paths):
            treeview.delete(*treeview.get_children())
            for item in lista_paths:
                treeview.insert('', 'end', values=[item])


    def separar_input(self):
        input_str = self.input_value.get()
        if len(input_str) == 7:
            ano = input_str[:2]
            mes = input_str[2:4]
            num = input_str[4:]
            procurar_input = self.procura(ano, self.site_combobox.get(), self.tipo_combobox.get(), mes, self.tipo_cabeamento.get())
            if procurar_input is not None:
                os_code = procurar_input[0] + input_str
                lista_paths = os.listdir(self.base_path) 

                self.print_section_header("Algoritimo de procura", f"\n\n- {procurar_input}\n\n- {input_str}\n\n- {os_code}\n\n- {self.base_path}")  
                
                console.print('\n\n[bold green]____________ LISTA DE CAMINHOS ____________[/bold green]\n\n')
                console.print(lista_paths)
                print('\n\n')
                os_path = self.encontrar_string_por_codigo(lista_paths,os_code)
                self.add_items_to_treeview(self.tabela, lista_paths)
                # abrir a pasta selecionada
                self.path = self.base_path
                self.base_path = self.base_path+'\\'+os_path
                subprocess.run(['explorer', self.base_path], shell=True)
                
                # return os_path
                return messagebox.showinfo("Resultado", f"Pasta aberta: {self.base_path}")
            else:
                return messagebox.showerror('Não Encontrado', 'Foras de parâmetros!\n(Tipo, ano ou mes)')
        else:
            return messagebox.showerror("Erro", "Formato inválido. O input deve ter 7 caracteres.")

    def mostrar_resultado(self):
        resultado = self.separar_input()
        console.print(resultado)
    

    def trocar_combobox(self, choice):
        if choice == 'CABEAMENTO':
            self.tipo_cabeamento.configure(values=['OPEN', 'MAINFRAME'])
        elif choice == 'MANUTENÇÃO':
            self.tipo_cabeamento.configure(values=['CORRETIVA', 'PREVENTIVA'])
        else:
            self.tipo_cabeamento.configure(values=[''])

        self.tipo_cabeamento.set('')  
    
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f'{width}x{height}+{x}+{y}')

    def encontrar_string_por_codigo(self,lista, codigo):
            console.print('\n\n[bold yellow]____________ DEF - encontrar_string_por_codigo ____________[/bold yellow]\n\n')
            for item in lista:
                if item.startswith(codigo):
                    return item
            return None

    def procura(self, ano, site, tipo, mes, tipo_cabeamento):
        console.print('[bold blue]____________ DEF - PROCURA ____________[/bold blue]')
        found = False
        ano = '20'+ ano
        if ano in self.dic:
            if ano in ['2009']:
                console.print('\n[on green] 2009 [/on green]') #base_path => OK
                return self._handle_2009(ano, site, mes)
            elif ano in ['2010']:                                               #manutenção ok
                console.print('\n[on green] 2010 [/on green]')                     
                return self._handle_2010(ano, site, tipo, mes, tipo_cabeamento)
            elif ano in ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2021', '2022']:
                console.print(f'\n[on green] {ano} [/on green]')
                return self._handle_2011_2022(ano, site, tipo, mes, tipo_cabeamento)
            elif ano in ['2023']:                                               # manutenção ok
                console.print(f'\n[on green] {ano} [/on green]')
                return self._handle_2023(ano, site, tipo, mes, tipo_cabeamento)
            elif ano in ['2020']:                                               # manutenção ok
                console.print(f'\n[on green] {ano} [/on green]')
                return self._handle_2020(ano, site, tipo, mes, tipo_cabeamento)

        return console.print('[bold red]VAZIO - nao encontrado[bold red]')

    def _handle_2009(self, ano, site, mes):
        console.print(f'\n\n{ano}            | \t if site in dic[ano]:')
        for key_mes in self.dic[ano][site]:
            if key_mes.startswith(mes):
                console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')

                # * Passando path 
                self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                teste = (self.dic[ano][site][key_mes], self.base_path,self.path)
                return teste         

    def _handle_2010(self, ano, site, tipo, mes, tipo_cabeamento):
        console.print(f'\n\n{ano}            | \t if site in dic[ano]:')
        if site in self.dic[ano]:
            console.print(f'{site}        | \t\t if tipo in dic[ano][site]:')
            if site in ['01 - CTI']:
                if tipo == 'CABEAMENTO':
                    console.print(f'{tipo}      | \t\t tipo == CABEAMENTO')
                    console.print('\n[on yellow] VERIFICANDO TIPO DE CABEAMENTO [/on yellow]')

                    if tipo_cabeamento in self.dic[ano][site][tipo]:
                        console.print(f'{tipo_cabeamento}        | \t\t\t tipo_cabeamento')
                        for key_mes in self.dic[ano][site][tipo][tipo_cabeamento]:
                            if key_mes.startswith(mes):
                                console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                                self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                                self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                                teste = (self.dic[ano][site][tipo][tipo_cabeamento][key_mes], self.base_path,self.path)
                                return teste
            
                            
                elif tipo in ['ELÉTRICA', 'MANUTENÇÃO']:
                    for key_mes in self.dic[ano][site][tipo]:
                        if key_mes.startswith(mes):
                            console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                            self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                            self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                            teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                            return teste
                        
            if site in ['02 - ALPHAVILLE']:
                if tipo == 'CABEAMENTO':
                    console.print(f'{tipo}      | \t\t tipo == CABEAMENTO')
                    console.print('\n[on yellow] ALPHAVILLE [/on yellow]')
                    tipo_cabeamento =''
                    console.print(f'{tipo_cabeamento}        | \t\t\t tipo_cabeamento')
                    for key_mes in self.dic[ano][site][tipo]:
                        if key_mes.startswith(mes):
                            console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                            # return self.dic[ano][site][tipo][tipo_cabeamento][key_mes]

                            self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                            self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                            teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                            return teste
                
                                
                if tipo in ['ELÉTRICA', 'MANUTENÇÃO']:
                    for key_mes in self.dic[ano][site][tipo]:
                        if key_mes.startswith(mes):
                            console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                            self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                            self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                            teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                            return teste        #   self.dic[ano][site][tipo][key_mes]


            if site == '04 - REDE LAN':
                for key_mes in self.dic[ano][site][tipo]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                        self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                        return teste 

    def _handle_2011_2022(self, ano, site, tipo, mes, tipo_cabeamento):
        console.print(f'\n\n{ano}            | \t if site in dic[ano]:')
        if site in self.dic[ano]:
            console.print(f'{site}        | \t\t if tipo in dic[ano][site]:')
            if ano in ['2022'] and site in '03 - XAXIM': # * criar mensagem de erro
                for key_mes in self.dic[ano][site]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t\t\t key_mes.startswith(mes)')
                        self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{key_mes}'
                        self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{key_mes}'
                        teste = (self.dic[ano][site][key_mes], self.base_path,self.path)
                        return teste

            if tipo == 'CABEAMENTO':
                console.print(f'{tipo}      | \t\t tipo == CABEAMENTO')
                if tipo_cabeamento in self.dic[ano][site][tipo]:
                    console.print(f'{tipo_cabeamento}      | \t\t\t tipo_cabeamento')
                    for key_mes in self.dic[ano][site][tipo][tipo_cabeamento]:
                        if key_mes.startswith(mes):
                            console.print(f'{key_mes}   | \t\t\t\t\t key_mes.startswith(mes)')
                            self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                            self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                            teste = (self.dic[ano][site][tipo][tipo_cabeamento][key_mes], self.base_path,self.path)
                            return teste

            if tipo in ['ELÉTRICA']:
                for key_mes in self.dic[ano][site][tipo]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                        self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                        return teste

            if tipo == 'MANUTENÇÃO':
                teste = self._handle_manutencao(ano, site, tipo, mes, tipo_cabeamento)
                self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{teste[2]}\\{self.tipo_cabeamento.get()}'
                self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{teste[2]}\\{self.tipo_cabeamento.get()}'
                juntando = (teste[0], self.base_path,self.path)
                return juntando
                
            if site in ['03 - XAXIM'] and ano in ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2021']:
                if tipo == 'CABEAMENTO':
                    console.print('[on green] 03 - XAXIM [/on green]')
                    for key_mes in self.dic[ano][site][tipo]:
                        if key_mes.startswith(mes):
                            console.print(f'{key_mes}   | \t\t\t\t\t key_mes.startswith(mes)')
                            self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                            self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                            teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                            return teste
                            # return self.dic[ano][site][tipo][key_mes]

            if site == '04 - REDE LAN':
                for key_mes in self.dic[ano][site][tipo]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                        self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                        return teste 

    def _handle_manutencao(self, ano, site, tipo, mes, tipo_cabeamento):
        console.print('\n[on white] MANUTENCAO - FUNCAO [/on white]') 
        for key_mes, value in self.dic[ano][site][tipo].items():
            if key_mes.startswith(mes):
                console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                console.print(f'{value}   | \t\t\t value')
                dic_manutencao = value
                chave = None
                # console.print(self.dic[ano][site][tipo].items())
                if tipo_cabeamento.lower() == 'preventiva':
                    for key, val in dic_manutencao.items():
                        if tipo_cabeamento.lower() in key.lower():
                            chave = key
                            if val:
                                console.print(val)
                                lista_return = (val, chave,key_mes)
                                return lista_return

                elif tipo_cabeamento.lower() == 'corretiva':
                    for key, val in dic_manutencao.items():
                        if tipo_cabeamento.lower() in key.lower():
                            chave = key
                            if val:
                                console.print(val)
                                lista_return = (val, chave,key_mes)
                                return lista_return

                if chave is None:
                    return ''
        return ''

    def _handle_2023(self, ano, site, tipo, mes, tipo_cabeamento):
        if site == '02 - ALPHAVILLE':
            console.print(f'{site}        | \t\t if tipo in dic[ano][site]:')
            if tipo == 'CABEAMENTO':
                console.print(f'{tipo}      | \t\t tipo == CABEAMENTO')
                tipo = 'CABEAMENTO LÓGICO'
                if tipo_cabeamento in self.dic[ano][site][tipo]:
                    console.print(f'{tipo_cabeamento}      | \t\t\t tipo_cabeamento')
                    for key_mes in self.dic[ano][site][tipo][tipo_cabeamento]:
                        if key_mes.startswith(mes):
                            console.print(f'{key_mes}   | \t\t\t\t\t key_mes.startswith(mes)')
                            self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{tipo}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                            self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{tipo}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                            teste = (self.dic[ano][site][tipo][tipo_cabeamento][key_mes], self.base_path,self.path)
                            return teste

            if tipo == 'ELÉTRICA':
                for key_mes in self.dic[ano][site][tipo]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                        self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                        return teste
                    
            if tipo == 'MANUTENÇÃO':
                for key_mes in self.dic[ano][site][tipo]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                        self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                        return teste
                    
        if site == '01 - CTI':
            console.print(f'{site}        | \t\t if tipo in dic[ano][site]:')
            if tipo == 'CABEAMENTO':
                console.print(f'{tipo}      | \t\t tipo == CABEAMENTO')
                for key_mes in self.dic[ano][site][tipo][tipo_cabeamento]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t\t\t key_mes.startswith(mes)')
                        self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                        self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                        teste = (self.dic[ano][site][tipo][tipo_cabeamento][key_mes], self.base_path,self.path)
                        return teste
            
            if tipo == 'ELÉTRICA':
                for key_mes in self.dic[ano][site][tipo]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                        self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\ELETRICA\\{key_mes}'
                        self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\ELETRICA\\{key_mes}'
                        teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                        return teste
                    
            if tipo == 'MANUTENÇÃO':
                teste = self._handle_manutencao(ano, site, tipo, mes, tipo_cabeamento)
                self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{teste[2]}\\{self.tipo_cabeamento.get()}'
                self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{teste[2]}\\{self.tipo_cabeamento.get()}'
                juntando = (teste[0], self.base_path, self.path)
                return juntando
        

        if site == '03 - XAXIM':
            for key_mes in self.dic[ano][site]:
                if key_mes.startswith(mes):
                    console.print(f'{key_mes}   | \t\t\t\t\t key_mes.startswith(mes)')
                    self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{key_mes}'
                    self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{key_mes}'
                    teste = (self.dic[ano][site][key_mes], self.base_path, self.path)
                    return teste 

        if site == '04 - REDE LAN':
            for key_mes in self.dic[ano][site][tipo]:
                if key_mes.startswith(mes):
                    console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                    self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{key_mes}'
                    self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{key_mes}'
                    teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                    return teste 

    def _handle_2020(self, ano, site, tipo, mes, tipo_cabeamento):
        console.print(f'\n\n{ano}            | \t if site in dic[ano]:')
        if site == '01 - CTI':
            console.print(f'{site}        | \t\t if tipo in dic[ano][site]:')
            if tipo == 'CABEAMENTO':
                for key_mes in self.dic[ano][site][tipo][tipo_cabeamento]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t\t\t key_mes.startswith(mes)')
                        if tipo_cabeamento in 'MAINFRAME':
                            self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\OPEN\\{self.tipo_cabeamento.get()}\\{key_mes}'
                            self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\OPEN\\{self.tipo_cabeamento.get()}\\{key_mes}'
                            teste = (self.dic[ano][site][tipo][tipo_cabeamento][key_mes], self.base_path,self.path)
                            return teste
                        else:
                            self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                            teste = (self.dic[ano][site][tipo][tipo_cabeamento][key_mes], self.base_path)
                            return teste

        if site == '02 - ALPHAVILLE':
            if tipo == 'CABEAMENTO':
                console.print(f'{tipo}      | \t\t tipo == CABEAMENTO')
                for key_mes in self.dic[ano][site][tipo][tipo_cabeamento]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t\t\t key_mes.startswith(mes)')
                        self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                        self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{self.tipo_cabeamento.get()}\\{key_mes}'
                        teste = (self.dic[ano][site][tipo][tipo_cabeamento][key_mes], self.base_path,self.path)
                        return teste

        if site == '03 - XAXIM':
            if tipo == 'CABEAMENTO':
                console.print(f'{tipo}      | \t\t tipo == CABEAMENTO')
                for key_mes in self.dic[ano][site][tipo]:
                    if key_mes.startswith(mes):
                        console.print(f'{key_mes}   | \t\t\t\t\t key_mes.startswith(mes)')
                        self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                        teste = (self.dic[ano][site][tipo][key_mes], self.base_path, self.path)
                        return teste 
        
        if tipo == 'MANUTENÇÃO':
            teste = self._handle_manutencao(ano, site, tipo, mes, tipo_cabeamento)
            self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{teste[2]}\\{self.tipo_cabeamento.get()}'
            self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{teste[2]}\\{self.tipo_cabeamento.get()}'
            juntando = (teste[0], self.base_path,self.path)
            return juntando
        
        if tipo == 'ELÉTRICA':
            for key_mes in self.dic[ano][site][tipo]:
                if key_mes.startswith(mes):
                    console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                    self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                    self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                    teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                    return teste 

        if site == '04 - REDE LAN':
            for key_mes in self.dic[ano][site][tipo]:
                if key_mes.startswith(mes):
                    console.print(f'{key_mes}   | \t\t\t key_mes.startswith(mes)')
                    self.base_path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                    self.path = f'\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.site_combobox.get()}\\{self.tipo_combobox.get()}\\{key_mes}'
                    teste = (self.dic[ano][site][tipo][key_mes], self.base_path,self.path)
                    return teste

if __name__ == "__main__":
    app = SimpleApp()
    app.mainloop()