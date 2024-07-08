import customtkinter as ctk
# from rich import print
# from rich.pretty import Pretty

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.dic = {}
        ctk.set_appearance_mode('dark')
        root.geometry('700x400')
        root.title('Busca de arquivos')
        root.minsize(700, 400)
        # self.dic_anos = {}
        self.center_window(700, 400)  # Centraliza a janela

        self.my_dict = {
            'font': '#c2c2c2',
            'preto': '#111',
            'hover': '#111',
            'selecionado': '#111',  
            'menu-sup': '#333',
            'menu-inf': '#222',
            'borda': '#a3a3a3'
        }

        self.buttons = {}  # Dicionário para armazenar os botões
        self.input_value = ctk.StringVar()  # Variável para armazenar o valor do input
        self.setup_auto()

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

        # Abrir 01 - CTI por padrão
        self.show_frame("01 - CTI")

    def add_buttons_menu(self, frame):
        button_texts = ["01 - CTI", "02 - ALPHAVILLE", "03 - XAXIM", "04 - REDE LAN"]

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
        if frame_name == "01 - CTI":
            Aba_cti(self, self.frame_tela, self.my_dict, self.input_value)
        elif frame_name == "02 - ALPHAVILLE":
            Aba_alpha(self, self.frame_tela, self.my_dict, self.input_value)
        elif frame_name == "03 - XAXIM":
            Aba_xax(self, self.frame_tela, self.my_dict, self.input_value)
        elif frame_name == "04 - REDE LAN":
            Aba_redl(self, self.frame_tela, self.my_dict, self.input_value)

    def buscar_arquivo(self):
        input_str = self.input_value.get()
        if len(input_str) == 7:
            
            ano = input_str[:2]
            mes = input_str[2:4]
            num = input_str[4:]
            os_code = ''
            return {
                'Ano': ano,
                'Mês': mes,
                'Número': num,
                'Código OS': os_code,
            }
        else:
            return "Formato inválido. O input deve ter 7 caracteres."

class Aba_cti:
    def __init__(self, parent, master, my_dict, input_var):
        self.parent = parent  # Referência para a instância da classe pai
        self.frame = ctk.CTkFrame(master, fg_color=my_dict['preto'])
        self.frame.pack(fill='both', expand=True)
        label = ctk.CTkLabel(self.frame, text="Conteúdo da 01 - CTI", text_color=my_dict['font'])
        label.pack(pady=5, padx=5)
        entry = ctk.CTkEntry(self.frame, textvariable=input_var,)
        entry.pack(pady=20, padx=20)
        button = ctk.CTkButton(self.frame, text="Buscar Arquivo", command=self.mostrar_resultado)
        button.pack(pady=20, padx=20)
        self.site_combobox = ctk.CTkComboBox(self.frame, values=['01 - CTI', '02 - ALPHAVILLE','03 - XAXIM','04 - REDE LAN'], state='readonly')
        self.site_combobox.pack(pady=20, padx=20)
        
        self.tipo_combobox = ctk.CTkComboBox(self.frame, values=['CABEAMENTO', 'ELÉTRICA', 'MANUTENÇÃO'], state='readonly', command=self.trocar_combobox)
        self.tipo_combobox.pack(pady=20, padx=20)

        self.tipo_cabeamento = ctk.CTkComboBox(self.frame, values=[''], state='readonly')
        self.tipo_cabeamento.pack(pady=20, padx=20)
        # self.trocar_combobox()
        

    def mostrar_resultado(self):
        resultado = self.parent.buscar_arquivo()
        print(resultado)  # Usando Pretty para formatar o output

    def trocar_combobox(self, choice):
        if choice == 'CABEAMENTO':
            self.tipo_cabeamento.configure(values=['OPEN', 'MAINFRAME'])
        elif choice == 'MANUTENÇÃO':
            self.tipo_cabeamento.configure(values=['CORRETIVA', 'PREVENTIVA'])
        else:
            self.tipo_cabeamento.configure(values=[''])

        self.tipo_cabeamento.set('')  

class Aba_alpha:
    def __init__(self, parent, master, my_dict, input_var):
        self.parent = parent  # Referência para a instância da classe pai
        self.frame = ctk.CTkFrame(master, fg_color=my_dict['preto'])
        self.frame.pack(fill='both', expand=True)
        label = ctk.CTkLabel(self.frame, text="Conteúdo da 02 - ALPHAVILLE", text_color=my_dict['font'])
        label.pack(pady=20, padx=20)
        entry = ctk.CTkEntry(self.frame, textvariable=input_var, fg_color=my_dict['font'])
        entry.pack(pady=20, padx=20)
        button = ctk.CTkButton(self.frame, text="Buscar Arquivo", command=self.mostrar_resultado)
        button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def mostrar_resultado(self):
        resultado = self.parent.buscar_arquivo()
        print(resultado)

class Aba_xax:
    def __init__(self, parent, master, my_dict, input_var):
        self.parent = parent  # Referência para a instância da classe pai
        self.frame = ctk.CTkFrame(master, fg_color=my_dict['preto'])
        self.frame.pack(fill='both', expand=True)
        label = ctk.CTkLabel(self.frame, text="Conteúdo da 03 - XAXIM", text_color=my_dict['font'])
        label.pack(pady=20, padx=20)
        entry = ctk.CTkEntry(self.frame, textvariable=input_var, fg_color=my_dict['font'])
        entry.pack(pady=20, padx=20)
        button = ctk.CTkButton(self.frame, text="Buscar Arquivo", command=self.mostrar_resultado)
        button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def mostrar_resultado(self):
        resultado = self.parent.buscar_arquivo()
        print(resultado)

class Aba_redl:
    def __init__(self, parent, master, my_dict, input_var):
        self.parent = parent  # Referência para a instância da classe pai
        self.frame = ctk.CTkFrame(master, fg_color=my_dict['preto'])
        self.frame.pack(fill='both', expand=True)
        label = ctk.CTkLabel(self.frame, text="Conteúdo da 04 - REDE LAN", text_color=my_dict['font'])
        label.pack(pady=20, padx=20)
        entry = ctk.CTkEntry(self.frame, textvariable=input_var, fg_color=my_dict['font'])
        entry.pack(pady=20, padx=20)
        button = ctk.CTkButton(self.frame, text="Buscar Arquivo", command=self.mostrar_resultado)
        button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def mostrar_resultado(self):
        resultado = self.parent.buscar_arquivo()
        print(resultado)

if __name__ == '__main__':
    root = ctk.CTk()
    app = MenuApp(root)
    root.mainloop()
