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
        self.base_path = "\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\"
        self.dic = {
        "2009":{
            "01 - CTI":{
                # base_path =f"\\\\mz-vv-fs-087\\D4250_4\\Compartilhado\\Entre_Secoes\\D4250S657\\Publica\\04 - ABERTURA DE OS\\OS EE\\04 - ANOS ANTERIORES\\{ano}\\{self.combobox_sites.get()}\\{self.combobox_tipos.get()}\\{mes_path}"
                # os_code = os_code.replace("EEc", "OS EEc")
                "11 - NOVEMBRO":"OS EEc", 
                "12 - DEZEMBRO":"OS EE ", 
            }
        },
        "2010":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"OS EE ", 
                        "02 - FEVEREIRO":"OS EE ", 
                        "03 - MARÇO":"OS EE ", 
                        "04 - ABRIL":"OS EE ", 
                        "05 - MAIO":"OS EE ", 
                        "06 - JUNHO":"OS EE ", 
                        "07 - JULHO":"OS EE ", 
                        "08 - AGOSTO":"OS EE ", 
                        "09 - SETEMBRO":"OS EE ", 
                        "10 - OUTUBRO":"OS EE ", 
                        "11 - NOVEMBRO":"OS EE ", 
                        "12 - DEZEMBRO":"OS EE ", 
                    },
                    "MAINFRAME":{
                        # "01 - JANEIRO":"OS EE", 
                        # "02 - FEVEREIRO":"OS EE", 
                        # "03 - MARÇO":"OS EE", 
                        # "04 - ABRIL":"OS EE", 
                        # "05 - MAIO":"OS EE", 
                        # "06 - JUNHO":"OS EE", 
                        # "07 - JULHO":"OS EE", 
                        # "08 - AGOSTO":"OS EE", 
                        "09 - SETEMBRO":"OS EE-MF ", 
                        "10 - OUTUBRO":"OS EE-MF ", 
                        "11 - NOVEMBRO":"OSEE-MF ", 
                        "12 - DEZEMBRO":"OSEE-MF ", 
                    }
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe ", 
                    "02 - FEVEREIRO":"OS EEe ", 
                    "03 - MARÇO":"OS EEe ", 
                    "04 - ABRIL":"OS EEe ", 
                    "05 - MAIO":"OS EEe ", 
                    "06 - JUNHO":"OS EE ", 
                    "07 - JULHO":"OS EE ", 
                    "08 - AGOSTO":"OS EE ", 
                    "09 - SETEMBRO":"OS EE ", 
                    "10 - OUTUBRO":"OS EE ", 
                    "11 - NOVEMBRO":"OS EE ", 
                    "12 - DEZEMBRO":"OS EE ",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO":"OS EEm ", 
                    "02 - FEVEREIRO":"OS EEm ", 
                    "03 - MARÇO":"OS EEm ", 
                    "04 - ABRIL":"OS EEm ", 
                    "05 - MAIO":"OS EEm ", 
                    "06 - JUNHO":"OS EEm ", 
                    "07 - JULHO":"OS EEm ", 
                    "08 - AGOSTO":"OS EEm ", 
                    "09 - SETEMBRO":"OS EEm ", 
                    "10 - OUTUBRO":"OS EEm ", 
                    "11 - NOVEMBRO":"OS EEm ", 
                    "12 - DEZEMBRO":"OS EEm ",  
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    # "02 - FEVEREIRO":"OS EE", 
                    # "03 - MARÇO":"OS EE", 
                    # "06 - JUNHO":"OS EE", 
                    # "11 - NOVEMBRO":"OS EE", 
                    "01 - JANEIRO":"OS EE ", 
                    "04 - ABRIL":"OS EE ", 
                    "05 - MAIO":"OS EE ", 
                    "07 - JULHO":"OS EE ", 
                    "08 - AGOSTO":"OS EE ", 
                    "09 - SETEMBRO":"OS EE ", 
                    "10 - OUTUBRO":"OS EE ", 
                    "12 - DEZEMBRO":"OS EE ", 
                    
                },
                "ELÉTRICA":{
                    # "02 - FEVEREIRO":"OS EE ", 
                    # "03 - MARÇO":"OS EEe ", 
                    # "05 - MAIO":"OS EEe ", 
                    # "06 - JUNHO":"OS EE ", 
                    # "09 - SETEMBRO":"OS EE ", 
                    # "10 - OUTUBRO":"OS EE ", 
                    # "11 - NOVEMBRO":"OS EE ", 
                    "01 - JANEIRO":"OS EE ", 
                    "04 - ABRIL":"OS EE ", 
                    "07 - JULHO":"OS-EE-", 
                    "08 - AGOSTO":"OS EE ", 
                    "12 - DEZEMBRO":"OS EE ",  
                },
                "MANUTENÇÃO":{
                    # VAZIA - NÃO TEM NADA
                }
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"OS EE ", 
                    "02 - FEVEREIRO":"OS EE ", 
                    "03 - MARÇO":"OS EE ", 
                    "04 - ABRIL":"OS EE ", 
                    "05 - MAIO":"OS EE ", 
                    "06 - JUNHO":"OS EE ", 
                    "07 - JULHO":"OS EE ", 
                    "08 - AGOSTO":"OS EE ", 
                    "09 - SETEMBRO":("OS EEp ","OS EEv ", "OS EEt"), 
                    "10 - OUTUBRO":("OS EEp - ","OS EEv - ", "OS EEt - "), 
                    "11 - NOVEMBRO":("OS EEp ","OS EEv ", "OS EEt"), 
                    "12 - DEZEMBRO":("OS EEp ","OS EEv ", "OS EEt"),
                },
                "ELÉTRICA":{
                    "03 - MARÇO":"OS EEe ",  
                    "04 - ABRIL":"OS EE ", 
                    "05 - MAIO":"OS EEe ", 
                    "08 - AGOSTO":"OS EE ", 
                    "09 - SETEMBRO":"OS EE ", 
                    "10 - OUTUBRO":"OS EEp ", 
                    "11 - NOVEMBRO":"OS EE ",  
                },
                "MANUTENÇÃO":{}
            }
        },
        "2011":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"OS EE ", 
                        "02 - FEVEREIRO":"OS EE ", 
                        "03 - MARÇO":"OS EE ", 
                        "04 - ABRIL":"OS EE ", 
                        "05 - MAIO":"OS EEc ", 
                        "06 - JUNHO":"OS EEc ", 
                        "07 - JULHO":"OS EEc ", 
                        "08 - AGOSTO":"OS EEc ", 
                        "09 - SETEMBRO":"OS EEc ", 
                        "10 - OUTUBRO":"OS EEc ", 
                        "11 - NOVEMBRO":"OS EEc ", 
                        "12 - DEZEMBRO":"OS EEc ", 
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"OSEE-MF ", 
                        "02 - FEVEREIRO":"OS EE-MF ", 
                        "03 - MARÇO":"OS EE MF ", 
                        "04 - ABRIL":"OS EE MF ", 
                        "05 - MAIO":"OS EE-MF", 
                        "06 - JUNHO":"OS EE-MF ", 
                        "07 - JULHO":"OS EE-MF ", 
                        "08 - AGOSTO":"OS EE-MF ", 
                        "09 - SETEMBRO":"OS EE-MF ", 
                        "10 - OUTUBRO":"OS EE-MF ", 
                        "11 - NOVEMBRO":"OSEE-MF ", 
                        # "12 - DEZEMBRO":"OSEE-MF ", 
                    }
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EE ", 
                    "02 - FEVEREIRO":"OS EE ", 
                    "03 - MARÇO":"OS EE ", 
                    "04 - ABRIL":"OS EE ", 
                    "05 - MAIO":"OS EE ", 
                    "06 - JUNHO":"OS EEe ", 
                    "07 - JULHO":"OS EEe ", 
                    "08 - AGOSTO":"OS EEe ", 
                    "09 - SETEMBRO":"OS EEe ", 
                    "10 - OUTUBRO":"OS EEe ", 
                    "11 - NOVEMBRO":"OS EEe ", 
                    "12 - DEZEMBRO":"OS EEe ",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO":"OS EEm ", 
                    "02 - FEVEREIRO":"OS EEm ", 
                    "03 - MARÇO":"OS EEm ", 
                    "04 - ABRIL":"OS EEm ", 
                    "05 - MAIO":"OS EEm ", 
                    "06 - JUNHO":"OS EEm ", 
                    "07 - JULHO":"OS EEm ", 
                    "08 - AGOSTO":"OS EEm ", 
                    "09 - SETEMBRO":"OS EEm ", 
                    "10 - OUTUBRO":"OS EEm ", 
                    "11 - NOVEMBRO":"OS EEm ", 
                    "12 - DEZEMBRO":"OS EEm ",  
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    # "01 - JANEIRO":"OS EE", 
                    # "02 - FEVEREIRO":"OS EE", 
                    # "03 - MARÇO":"OS EE", 
                    # "06 - JUNHO":"OS EE ", 
                    # "07 - JULHO":"OS EE", 
                    # "08 - AGOSTO":"OS EE ", 
                    # "10 - OUTUBRO":"OS EE", 
                    # "11 - NOVEMBRO":"OS EE", 
                    "04 - ABRIL":"OS EE ", 
                    "05 - MAIO":"OS EE ", 
                    "09 - SETEMBRO":"OS EE", 
                    "12 - DEZEMBRO":"OS EE", 

                },
                "ELÉTRICA":{
                    # "02 - FEVEREIRO":"OS EE ", 
                    # "03 - MARÇO":"OS EEe ", 
                    # "05 - MAIO":"OS EEe ", 
                    # "06 - JUNHO":"OS EE ", 
                    # "09 - SETEMBRO":"OS EE ", 
                    # "10 - OUTUBRO":"OS EE ", 
                    # "11 - NOVEMBRO":"OS EE ", 
                    # "01 - JANEIRO":"OS EE ", 
                    "04 - ABRIL":"OS EE ", 
                    # "07 - JULHO":"OS-EE-", 
                    # "08 - AGOSTO":"OS EE ", 
                    # "12 - DEZEMBRO":"OS EE ",  
                },
                "MANUTENÇÃO":{
                    "PREVENTIVA":{"06 - JUNHO":"OS EE "} 
                }
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"OS EERL ", 
                    "02 - FEVEREIRO":"OS EERL ", 
                    "03 - MARÇO":"OS EE RLE", 
                    "04 - ABRIL":"OS EERL ", 
                    # "05 - MAIO":"OS EE ", 
                    "06 - JUNHO":"OS EERLAN - ", 
                    "07 - JULHO":"OS EERL - ", 
                    "08 - AGOSTO":"OS EERL ", 
                    "09 - SETEMBRO":"OS EERL ", 
                    "10 - OUTUBRO":"OS EERL ", 
                    "11 - NOVEMBRO":"OS EERL ", 
                    # "12 - DEZEMBRO":"OS EERL ", 
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EE ",
                },
                "MANUTENÇÃO":{}
            },
            "Predio Vermelho e Prata":{
                "Elétrica":"OS EEV ",
                "Lógica":{
                    "01 - Janeiro":"0S EE ",
                    "02 - Fevereiro":"OS EEv ",
                    "03 - Março":"OS EEV ",
                    "04 - Abril":"OS EEv ",
                    "05 - Maio":"OS EEv ",
                    "06 - Junho":"OS EEv ",
                    "07 - Julho":"OS EEv ",
                    "08 - Agosto":"OS EEp ",
                    "09 - Setembro":"OS EEv ",
                    "10 - Outubro":"OS EEv ",
                    "11 - Novembro":"OS EEV ",
                    "10 - Dezembro":"OS EEv ",
                },
                "Manutenção":{
                    "03-Março":"OS EEV ",
                    "04-Abril":"OS EEV ",
                    "08-Agosto":"EEm ",
                    "10-Outubro":"EEm ",
                    "11 - Novembro":"OS EEm "
                }
            }
        },
        "2012":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"OS EEc ", 
                        "02 - FEVEREIRO":"OS EEc ", 
                        "03 - MARÇO":"OS EEc ", 
                        "04 - ABRIL":"OS EEc ", 
                        "05 - MAIO":"OS EEc ", 
                        "06 - JUNHO":"OS EEc ", 
                        "07 - JULHO":"OS EEc ", 
                        "08 - AGOSTO":"OS EEc ", 
                        "09 - SETEMBRO":"OS EEc", 
                        "10 - OUTUBRO":"EEc ", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ", 
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"OS EE-MF ", 
                        "02 - FEVEREIRO":"OS EE-MF ", 
                        "03 - MARÇO":"OS EE-MF ", 
                        "04 - ABRIL":"OS EE-MF ", 
                        "05 - MAIO":"OS EE-MF ", 
                        "06 - JUNHO":"OS EE-MF ", 
                        "07 - JULHO":"OS EE-MF ", 
                        "08 - AGOSTO":"OS EE-MF ", 
                        "09 - SETEMBRO":"OS EEMF ", 
                        "10 - OUTUBRO":"EE-MF ", 
                        "11 - NOVEMBRO":"EE-MF ", 
                        "12 - DEZEMBRO":"EE-MF ", 
                    }
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe ", 
                    "02 - FEVEREIRO":"OS EEe ", 
                    "03 - MARÇO":"OS EEe ", 
                    "04 - ABRIL":"OS EEe ", 
                    "05 - MAIO":"OS EEe ", 
                    "06 - JUNHO":"OS EEe ", 
                    "07 - JULHO":"OS EEe ", 
                    "08 - AGOSTO":"OS EEe ", 
                    "09 - SETEMBRO":"OS EEe ", 
                    "10 - OUTUBRO":"OS EEe ", 
                    "11 - NOVEMBRO":"OS EEe ", 
                    "12 - DEZEMBRO":"OS EEe ",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO":"OS EEm ", 
                    "02 - FEVEREIRO":"OS EEm ", 
                    "03 - MARÇO":"OS EEm ", 
                    "04 - ABRIL":"OS EEm ", 
                    "05 - MAIO":"OS EEm ", 
                    "06 - JUNHO":"OS EEm ", 
                    "07 - JULHO":"OS EEm ", 
                    "08 - AGOSTO":"OS EEm ", 
                    "09 - SETEMBRO":"OS EEm ", 
                    "10 - OUTUBRO":"OS EEm ", 
                    "11 - NOVEMBRO":"OS EEm ", 
                    "12 - DEZEMBRO":"OS EEm ",  
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "OPEN":{
                        "02 - FEVEREIRO":"OS EEAc ", 
                        "03 - MARÇO":"OS EE AL ", 
                        "04 - ABRIL":"OS EEc AL ", 
                        "05 - MAIO":"OS EEc AL ", 
                        "06 - JUNHO":"OS EE AL ", 
                        "07 - JULHO":"OS EE AL ", 
                        "08 - AGOSTO":"OS EEc AL ", 
                        "09 - SETEMBRO":"OS EEc AL ", 
                        "10 - OUTUBRO":"OS EEc  AL ", 
                        "11 - NOVEMBRO":"OS EEc AL ", 
                        "12 - DEZEMBRO":"OS EEc AL ", 
                    },
                    "MAINFRAME":{
                        # "01 - JANEIRO":"OS EEA-MF ", 
                        "02 - FEVEREIRO":"OS EEA-MF ",
                        "03 - MARÇO":"OS EEA-MF ", 
                        # "04 - ABRIL":"OS EEc AL ", 
                        "05 - MAIO":"OS EE AL ", 
                        # "06 - JUNHO":"OS EE AL ", 
                        "07 - JULHO":"OS EE AL ", 
                        # "08 - AGOSTO":"OS EEc AL ", 
                        # "09 - SETEMBRO":"OS EEc AL ", 
                        "10 - OUTUBRO":"OS EEc  AL ", 
                        # "11 - NOVEMBRO":"OS EEc AL ", 
                        "12 - DEZEMBRO":"OS EE-MF AL ", 
                    }
                },
                "ELÉTRICA":{
                    # "02 - FEVEREIRO":"OS EE ", 
                    # "03 - MARÇO":"OS EEe ", 
                    # "05 - MAIO":"OS EEe ", 
                    # "06 - JUNHO":"OS EE ", 
                    # "09 - SETEMBRO":"OS EE ", 
                    # "10 - OUTUBRO":"OS EE ", 
                    "11 - NOVEMBRO":"OS EEe ", 
                    # "01 - JANEIRO":"OS EE ", 
                    # "04 - ABRIL":"OS EE ", 
                    # "07 - JULHO":"OS-EE-", 
                    # "08 - AGOSTO":"OS EE ", 
                    "12 - DEZEMBRO":"OS EEe AL ",  
                },
                "MANUTENÇÃO":{
                    "04 - ABRIL":"OS EEm ",
                    "11 - NOVEMBRO":"OS EEm ",
                    "12 - DEZEMBRO":"OS EEm AL ",   
                }
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"OS EERL ", 
                    "02 - FEVEREIRO":"OS EERL ", 
                    "03 - MARÇO":"OS EERL ", 
                    # "04 - ABRIL":"OS EE ", 
                    "05 - MAIO":"OS EERL ", 
                    "06 - JUNHO":"OS EERL ", 
                    "07 - JULHO":"OS EERL ", 
                    "08 - AGOSTO":"OS EERL ", 
                    "09 - SETEMBRO":"OS EERL ", 
                    "10 - OUTUBRO":"OS EERL ", 
                    "11 - NOVEMBRO":"EERL ", 
                    "12 - DEZEMBRO":"OS EERL ",
                },
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "Predio Vermelho e Prata":{
                "01-Janeiro":"OS EEp ",
                "02-Fevereiro":"OS EEp ",
                "03-Março":"OS EEp ",
                "04-Abril":"OS EE p",
                "05-Maio":"OS EEp ",
                "06-Junho":"OS EEp ",
                "07-Julho":"OS EEv ",
                "08-Agosto":"OS EEv ",
                "09-Setembro":"OS EEp ",
                "10-Outubro":"OS EEv ",
                "11-Novembro":"OS EEp ",
                "12-Dezembro":"OS EEp ",
            }
        },
        "2013":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc ", 
                        "02 - FEVEREIRO":"OS EEc ", 
                        "03 - MARÇO":"Os EEc ", 
                        "04 - ABRIL":("OS EEc ", "Os EEc "), 
                        "05 - MAIO":"OS EEc ", 
                        "06 - JUNHO":"OS EEc ", 
                        "07 - JULHO":"OS EEc ", 
                        "08 - AGOSTO":"OS EEc ", 
                        "09 - SETEMBRO":"OS EEc", 
                        "10 - OUTUBRO":"OS EEc ", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ", 
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"EEMF ", 
                        "02 - FEVEREIRO":"EE MF ", 
                        "03 - MARÇO":"OS EE MF ", 
                        "04 - ABRIL":"OS EE MF ", 
                        "05 - MAIO":"OS EE MF ", 
                        "06 - JUNHO":"OS EE MF ", 
                        "07 - JULHO":"OS EE MF ", 
                        "08 - AGOSTO":"OS EE MF ", 
                        "09 - SETEMBRO":"OS EE MF ", 
                        "10 - OUTUBRO":"OS EE MF ", 
                        "11 - NOVEMBRO":"OS EE MF ", 
                        "12 - DEZEMBRO":"OS EE MF ", 
                    }
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe ", 
                    "02 - FEVEREIRO":"OS EEe ", 
                    "03 - MARÇO":"OS EEe ", 
                    "04 - ABRIL":"OS EEe ", 
                    "05 - MAIO":"OS EEe ", 
                    "06 - JUNHO":"OS EEe ", 
                    "07 - JULHO":"OS EEe ", 
                    "08 - AGOSTO":"EEe ", 
                    "09 - SETEMBRO":"EEe ", 
                    "10 - OUTUBRO":"OS EEe ", 
                    "11 - NOVEMBRO":"OS EEe ", 
                    "12 - DEZEMBRO":"OS EEe ",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO":"OS EEm ", 
                    "02 - FEVEREIRO":"OS EEm ", 
                    "03 - MARÇO":"OS EEm ", 
                    "04 - ABRIL":"OS EEm ", 
                    "05 - MAIO":"OS EEm ", 
                    "06 - JUNHO":"OS EEm ", 
                    "07 - JULHO":"OS EEm ", 
                    "08 - AGOSTO":{"MANUTENÇÕES PREVENTIVAS": "OS EEm "}, 
                    "09 - SETEMBRO":{"MANUTENÇÕES CORRETIVAS": "OS EEmc ",
                                    "MANUTENÇÕES PREVENTIVAS": "OS EEm "}, 
                    "10 - OUTUBRO":{"MANUTENÇÕES CORRETIVAS": "OS EEmc",
                                    "MANUTENÇÕES PREVENTIVAS": "OS EEm "}, 
                    "11 - NOVEMBRO":{"MANUTENÇÕES PREVENTIVAS": "OS EEm "},
                    "12 - DEZEMBRO":{"PREVENTIVAS": "OS EEm "},
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "02 - FEVEREIRO":"OS EEc AL ", 
                    "03 - MARÇO":"OS EEc AL", 
                    "04 - ABRIL":"OS EEc AL", 
                    "05 - MAIO":"OS EEc AL ", 
                    "06 - JUNHO":"OS EEc AL ", 
                    "07 - JULHO":"OS EEc AL ", 
                    "08 - AGOSTO":"OS EEc AL ", 
                    "09 - SETEMBRO":"OS EEc AL ", 
                    "10 - OUTUBRO":"OS EEc  AL ", 
                    "11 - NOVEMBRO":"OS EEc AL", 
                    "12 - DEZEMBRO":"OS EEc AL", 
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EE AL ",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL ", 
                    "05 - MAIO":"OS EEe AL ", 
                    "06 - JUNHO":"OS EE ", 
                    "07 - JULHO":"OS EEe AL ", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL ",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "CABEAMENTO":{},
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"OS EERL ", 
                    "02 - FEVEREIRO":"OS EERL ", 
                    "03 - MARÇO":"OS EERL ", 
                    "04 - ABRIL":"EERL ", 
                    "05 - MAIO":"EERL ", 
                    "06 - JUNHO":"EERL ", 
                    "07 - JULHO":"OS EERL ", 
                    "08 - AGOSTO":"OS EERL ", 
                    "09 - SETEMBRO":"OS EERL ", 
                    "10 - OUTUBRO":"OS EERL ", 
                    "11 - NOVEMBRO":"OS EERL ", 
                    "12 - DEZEMBRO":"EERL ",
                },
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "Prédios Prata e Vermelho":{
                "01-Janeiro":"OS EEp ",
                "02-Fevereiro":"OS EEp ",
                "03-Março":"OS EEp ",
                "04-Abril":"OS EEp ",
                "05-Maio":"OS EEmp ",
                "06-Junho":"Os EEmp ",
                "07-Julho":"Os EEmp ",
                "08-Agosto":"",
                "09-Setembro":"",
                "10-Outubro":"",
                "11-Novembro":"",
                "12-Dezembro":"",
            },
        },
        "2014":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc ", 
                        "02 - FEVEREIRO":"EEc ", 
                        "03 - MARÇO":"EEc ", 
                        "04 - ABRIL":"EEc ", 
                        "05 - MAIO":"EEc ", 
                        "06 - JUNHO":"EEc ", 
                        "07 - JULHO":"EEc ", 
                        "08 - AGOSTO":"EEc ", 
                        "09 - SETEMBRO":"OS EEc", 
                        "10 - OUTUBRO":"EEc ", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"", 
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"EE MF ", 
                        "02 - FEVEREIRO":"OS EE MF ", 
                        "03 - MARÇO":"OS EE MF ", 
                        "04 - ABRIL":"OS EE MF ", 
                        "05 - MAIO":"Os EE MF ", 
                        "06 - JUNHO":"EE MF ", 
                        "07 - JULHO":"EE MF ", 
                        "08 - AGOSTO":"EE MF ", 
                        "09 - SETEMBRO":"EE MF ", 
                        "10 - OUTUBRO":"EE MF ", 
                        "11 - NOVEMBRO":"EE MF ", 
                        "12 - DEZEMBRO":"EE MF ", 
                    }
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe ", 
                    "02 - FEVEREIRO":"OS EEe ", 
                    "03 - MARÇO":"OS EEe ", 
                    "04 - ABRIL":"OS EEe ", 
                    "05 - MAIO":"OS EEe ", 
                    "06 - JUNHO":"OS EEe ", 
                    "07 - JULHO":"OS EEe ", 
                    "08 - AGOSTO":"OS EEe ", 
                    "09 - SETEMBRO":"OS EEe ", 
                    "10 - OUTUBRO":"OS EEe ", 
                    "11 - NOVEMBRO":"OS EEe ", 
                    "12 - DEZEMBRO":"OS EEe ",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO":{"CORRETIVA": "OS EEmc ","PREVENTIVAS": "OS EEm "}, 
                    "02 - FEVEREIRO":{"MANUTENÇÃO CORRETIVA": "OS EEmc ",
                                "MANUTENÇÃO PREVENTIVA": "OS EEm "}, 
                    "03 - MARÇO":{"MANUTENÇÃO CORRETIVA": "OS EEmc ",
                                "MANUTENÇÃO PREVENTIVA": "OS EEm "}, 
                    "04 - ABRIL":{"MANUTENÇÃO PREVENTIVA": "OS EEm "}, 
                    "05 - MAIO":{"MANUTENÇÃO PREVENTIVA": "OS EEm "}, 
                    "06 - JUNHO":{"Manutenção Preventiva": "OS EEm "}, 
                    "07 - JULHO":{"Manutenção Corretiva": "OS EEmc ",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "08 - AGOSTO":{"Manutenção Corretiva": "OS EEmc ",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "09 - SETEMBRO":{"Manutenção Corretiva": "OS EEmc",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "10 - OUTUBRO":{"Manutenção Corretiva": "OS EEmc ",
                                    "Manutenção Preventiva": "OS EEm "}, 
                    "11 - NOVEMBRO":"",
                    "12 - DEZEMBRO":{"Manutenção Preventiva": "OS EEm "},
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "02 - FEVEREIRO":"OS EEc AL", 
                    "03 - MARÇO":"OS EEc AL", 
                    "04 - ABRIL":"OS EEc AL", 
                    "05 - MAIO":"OS EEc AL", 
                    "06 - JUNHO":"OS EEc AL", 
                    "07 - JULHO":"OS EEc AL", 
                    "08 - AGOSTO":"OS EEc AL", 
                    "09 - SETEMBRO":"OS EEc AL", 
                    "10 - OUTUBRO":"OS EEc  AL ", 
                    "11 - NOVEMBRO":"OS EEc AL", 
                    "12 - DEZEMBRO":"OS EEc AL", 
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EE AL",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL ", 
                    "05 - MAIO":"OS EEe AL ", 
                    "06 - JUNHO":"OS EE ", 
                    "07 - JULHO":"OS EEe AL ", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL ",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "CABEAMENTO":{},
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"OS EERL ", 
                    "02 - FEVEREIRO":"EERL", 
                    "03 - MARÇO":"EERL ", 
                    "04 - ABRIL":"EERL ", 
                    "05 - MAIO":"EERL ", 
                    "06 - JUNHO":"EERL ", 
                    "07 - JULHO":"EERL ", 
                    "08 - AGOSTO":"EERL ", 
                    "09 - SETEMBRO":"EERL ", 
                    "10 - OUTUBRO":"EERL ", 
                    "11 - NOVEMBRO":"EERL ", 
                    "12 - DEZEMBRO":"EERL ",
                },
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "PRÉDIO PRATA E VERMELHO":{
                "01 - JANEIRO":"", 
                "02 - FEVEREIRO":"OS EEp ", 
                "08 - AGOSTO":" ", 
                "09 - SETEMBRO":"OS EEv ",
                "11 - NOVEMBRO":"OS EEp ",
            },

        },
        "2015":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc", 
                        "02 - FEVEREIRO":"EEc", 
                        "03 - MARÇO":"EEc", 
                        "04 - ABRIL":"EEc", 
                        "05 - MAIO":"EEc", 
                        "06 - JUNHO":"EEc", 
                        "07 - JULHO":"EEc", 
                        "08 - AGOSTO":"EEc", 
                        "09 - SETEMBRO":"EEc", 
                        "10 - OUTUBRO":"EEc", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ", 
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"EEMF ", 
                        "02 - FEVEREIRO":"EEMF ", 
                        "03 - MARÇO":"EEMF ", 
                        "04 - ABRIL":"EEMF ", 
                        "05 - MAIO":"EEMF", 
                        "06 - JUNHO":"EEMF", 
                        "07 - JULHO":"EEMF", 
                        "08 - AGOSTO":"EEMF ", 
                        "09 - SETEMBRO":"EEMF ", 
                        "10 - OUTUBRO":"EEMF ", 
                        "11 - NOVEMBRO":"OS EEMF", 
                        "12 - DEZEMBRO":"", 
                    }
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"EEe ", 
                    "02 - FEVEREIRO":"OS EEe ", 
                    "03 - MARÇO":"OS EEe ", 
                    "04 - ABRIL":"EEe ", 
                    "05 - MAIO":"OS EEe ", 
                    "06 - JUNHO":"OS EEe", 
                    "07 - JULHO":"OS EEe ", 
                    "08 - AGOSTO":"OS EEe ", 
                    "09 - SETEMBRO":"OS EEe ", 
                    "10 - OUTUBRO":"OS EEe ", 
                    "11 - NOVEMBRO":"OS EEe", 
                    "12 - DEZEMBRO":"OS EEe",  
                },
                "MANUTENÇÃO":{
                    "01 - Janeiro":{"manutenção corretiva": "EEmc ",
                                    "manutenção preventiva": "OS EEm "}, 
                    "02 - Fevereiro":{"manutenção corretiva": "EEmc ",
                                    "manutenção preventiva": "OS EEm "}, 
                    "03 - Março":{"Manutenção Corretiva": "OS EEmc ",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "04 - Abril":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "05 - Maio":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "06 - Junho":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "07 - Julho":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "08 - Agosto":{"Corretiva": "",
                                "Preventiva": "OS EEm "}, 
                    "09 - Setembro":{"Corretiva": "",
                                "Preventiva": "OS EEm "}, 
                    "10 - Outubro":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "}, 
                    "11 - Novembro":{"Corretiva": "",
                                "Preventiva": "OS EEm "},
                    "12 - Dezembro":{"Corretiva": "",
                                "Preventiva": "OS EEm "},
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "02 - FEVEREIRO":"OS EEc AL", 
                    "03 - MARÇO":"OS EEc AL", 
                    "04 - ABRIL":"OS EEc AL", 
                    "05 - MAIO":"OS EEc AL", 
                    "06 - JUNHO":"OS EEc AL", 
                    "07 - JULHO":"OS EEc AL", 
                    "08 - AGOSTO":"OS EEc AL", 
                    "09 - SETEMBRO":"OS EEc AL", 
                    "10 - OUTUBRO":"OS EEc AL", 
                    "11 - NOVEMBRO":"OS EEc AL", 
                    "12 - DEZEMBRO":"OS EEc AL", 
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EE AL",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL", 
                    "05 - MAIO":"OS EEe AL", 
                    "06 - JUNHO":"OS EEe AL", 
                    "07 - JULHO":"OS EEe AL", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "CABEAMENTO":{},
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"EERL", 
                    "02 - FEVEREIRO":"EERL", 
                    "03 - MARÇO":"EERL", 
                    "04 - ABRIL":"EERL", 
                    "05 - MAIO":"EERL", 
                    "06 - JUNHO":"EERL", 
                    "07 - JULHO":"EERL", 
                    "08 - AGOSTO":"EERL", 
                    "09 - SETEMBRO":"EERL", 
                    "10 - OUTUBRO":"EERL", 
                    "11 - NOVEMBRO":"EERL", 
                    "12 - DEZEMBRO":"",
                },
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "PRÉDIO PRATA E VERMELHO":{
                "Cabeamento":("Dezembro", "EEPV"),
                "Serviços gerais":"EEmp",
            },

        },
        "2016":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc", 
                        "02 - FEVEREIRO":"EEc", 
                        "03 - MARÇO":"EEc", 
                        "04 - ABRIL":"EEc", 
                        "05 - MAIO":"EEc", 
                        "06 - JUNHO":"EEc", 
                        "07 - JULHO":"EEc", 
                        "08 - AGOSTO":"EEc", 
                        "09 - SETEMBRO":"EEc", 
                        "10 - OUTUBRO":"EEc", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ", 
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"EEMF ", 
                        "02 - FEVEREIRO":"EEMF ", 
                        "03 - MARÇO":"EEMF ", 
                        "04 - ABRIL":"EEMF", 
                        "05 - MAIO":"EEMF", 
                        "06 - JUNHO":"EEMF", 
                        "07 - JULHO":"EE MF", 
                        "08 - AGOSTO":"EEMF", 
                        "09 - SETEMBRO":"", 
                        "10 - OUTUBRO":"EEMF", 
                        "11 - NOVEMBRO":"EEMF", 
                        "12 - DEZEMBRO":"OS EE MF ", 
                    }
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe", 
                    "02 - FEVEREIRO":"OS EEe", 
                    "03 - MARÇO":"OS EEe", 
                    "04 - ABRIL":"OS EEe ", 
                    "05 - MAIO":"OS EEe", 
                    "06 - JUNHO":"OS EEe", 
                    "07 - JULHO":"OS EEe", 
                    "08 - AGOSTO":"OS EEe", 
                    "09 - SETEMBRO":"OS EEe ", 
                    "10 - OUTUBRO":"OS EEe", 
                    "11 - NOVEMBRO":"OS EEe", 
                    "12 - DEZEMBRO":"OS EEe ",  
                },
                "MANUTENÇÃO":{
                    "01 - Janeiro":{"manutenção corretiva": "OS EEmc ",
                                    "manutenção preventiva": "OS EEm "}, 
                    "02 - Fevereiro":{"manutenção corretiva": "OS EEmc ",
                                    "manutenção preventiva": "OS EEm "}, 
                    "03 - Março":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "04 - Abril":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "05 - Maio":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "06 - Junho":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "07 - Julho":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "08 - Agosto":{"Manutenção Corretiva": "OS EEmc ",
                                "Manutenção Preventiva": "OS EEm "}, 
                    "09 - Setembro":{"Manutenção Corretiva": "OS EM ",
                                "Manutenção Preventiva": "OS EEm "},
                    "10 - Outubro":{"Manutenção Corretiva": "OS EEM ",
                                "Matutenção Preventiva": "OS EEm "}, 
                    "11 - Novembro":{"Corretiva": "",
                                "Preventiva": "OS EEm "},
                    "12 - Dezembro":{"Corretiva": "",
                                "Preventiva": "OS EEm "},
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01-Janeiro":"OS EEc AL",
                        "02 - Fevereiro":"OS EEc AL", 
                        "03 - Março":"OS EEc AL", 
                        "04 - Abril":"OS EEc AL", 
                        "05 - Maio":"OS EEc AL", 
                        "06 - Junho":"OS EEc AL", 
                        "07 - Julho":"OS EEc AL", 
                        "08 - Agosto":"OS EEc AL", 
                        "09 - Setembro":"OS EEc AL", 
                        "10 - Outubro":"OS EEc AL", 
                        "11 - Novembro":"OS EEc AL", 
                        "12 - Dezembro":"OS EEc AL",
                    },
                    "MAINFRAME":{
                        "01 - Janeiro":"OS EEc MF AL",
                        "02 - Fevereiro":"OS EEc MF AL", 
                        "03 - Março":"", 
                        "04 - Abril":"OS EEc MF AL", 
                        "05 - Maio":"OS EEc MF AL", 
                        "06 - Junho":"OS EEc MF AL", 
                        "07 - Julho":"OS EEc MF AL", 
                        "08 - Agosto":"OS EEc MF AL", 
                        "09 - Setembro":"", 
                        "10 - Outubro":"OS EEc MF AL", 
                        "11 - Novembro":"OS EEc MF AL", 
                        # "12 - Dezembro":"OS EEc MF",
                    },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EEe AL",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL", 
                    "05 - MAIO":"OS EEe AL", 
                    "06 - JUNHO":"OS EEe AL", 
                    "07 - JULHO":"OS EEe AL", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "CABEAMENTO":{},
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"EERL", 
                    "02 - FEVEREIRO":"EERL", 
                    "03 - MARÇO":"", 
                    "04 - ABRIL":"", 
                    "05 - MAIO":"", 
                    "06 - JUNHO":"EERL ", 
                    "07 - JULHO":"EERL ", 
                    "08 - AGOSTO":"EERL", 
                    "09 - SETEMBRO":"EERL", 
                    "10 - OUTUBRO":"", 
                    "11 - NOVEMBRO":"EEc ", 
                    "12 - DEZEMBRO":"",
                },
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "PRÉDIO PRATA E VERMELHO":{
                "02 - fevereiro":"EEc",
                "03 - março":"EEc",
                "05 - Maio":"EEPR",
                "12 - dezembro":"EEc"
            },

        },
        "2017":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc", 
                        "02 - FEVEREIRO":"EEc", 
                        "03 - MARÇO":"EEc", 
                        "04 - ABRIL":"EEc", 
                        "05 - MAIO":"EEc", 
                        "06 - JUNHO":"EEc", 
                        "07 - JULHO":"EEc", 
                        "08 - AGOSTO":"EEc", 
                        "09 - SETEMBRO":"EEc", 
                        "10 - OUTUBRO":"EEc", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ", 
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"EE MF ", 
                        "02 - FEVEREIRO":"EE MF ", 
                        "03 - MARÇO":"EE MF ", 
                        "04 - ABRIL":"EE MF ", 
                        "05 - MAIO":"EE MF ", 
                        "06 - JUNHO":"OS EE MF ", 
                        "07 - JULHO":"OS EE MF", 
                        "08 - AGOSTO":"OS EE MF ", 
                        "09 - SETEMBRO":"OS EE MF ", 
                        "10 - OUTUBRO":"OS EE MF ", 
                        "11 - NOVEMBRO":"EE MF ", 
                        "12 - DEZEMBRO":"", 
                    }
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe", 
                    "02 - FEVEREIRO":"OS EEe", 
                    "03 - MARÇO":"OS EEe", 
                    "04 - ABRIL":"EEe ", 
                    "05 - MAIO":"OS EEe", 
                    "06 - JUNHO":"OS EEe", 
                    "07 - JULHO":"OS EEe", 
                    "08 - AGOSTO":"OS EEe", 
                    "09 - SETEMBRO":"OS EEe ", 
                    "10 - OUTUBRO":"OS EEe", 
                    "11 - NOVEMBRO":"OS EEe", 
                    "12 - DEZEMBRO":"OS EEe  ",  
                },
                "MANUTENÇÃO":{
                    "01 - Janeiro":{"manutenção corretiva": "OS EEmc ",
                                    "manutenção preventiva": "OS EEm "}, 
                    
                    "02 - Fevereiro":{"manutenção corretiva": "OS EEmc ",
                                    "manutenção preventiva": "OS EEm "}, 
                    
                    "03 - Março":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    
                    "04 - Abril":"OS EEm ", 
                    
                    "05 - Maio":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "}, 
                    
                    "06 - Junho":{"Manutenção Corretiva": "OS EEMC ",
                                "Manutenção Preventiva": "OS EEm "}, 
                    
                    "07 - Julho":{"Manutenção Corretiva": "EEmc",
                                "Manutenção Preventiva": "OS EEm "}, 
                    
                    "08 - Agosto":{"MANUTENÇÃO CORRETIVA": "OS EEmc ",
                                "MANUTENÇÃO PREVENTIVA": "OS EEm "}, 
                    
                    "09 - Setembro":{"Manutenção Corretiva": "",
                                "Manutenção Preventiva": "OS EEm "},
                    
                    "10 - Outubro":{"Manutenção Corretiva": "OS EEMC ",
                                "Matutenção Preventiva": "OS EEm "}, 
                    
                    "11 - Novembro":{"Manutenção Corretiva": "OS EEmc ",
                                "Manutenção Preventiva": "OS EEm "},
                    
                    "12 - Dezembro":{"Manutenção Corretiva": "OS EEmc ",
                                "Manutenção Preventiva": "OS EEm "},
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01-Janeiro":"OS EEc AL",
                        "02 - Fevereiro":"OS EEc AL", 
                        "03 - Março":"OS EEc AL", 
                        "04 - Abril":"OS EEc AL", 
                        "05 - Maio":"OS EEc AL", 
                        "06 - Junho":"OS EEc AL", 
                        "07 - Julho":"OS EEc AL", 
                        "08 - Agosto":"OS EEc AL", 
                        "09 - Setembro":"OS EEc AL", 
                        "10 - Outubro":"OS EEc AL", 
                        "11 - Novembro":"OS EEc AL", 
                        "12 - Dezembro":"OS EEc AL",
                    },
                    "MAINFRAME":{
                        "01 - Janeiro":"OS EEc MF AL",
                        "02 - Fevereiro":"OS EEc MF AL", 
                        "03 - Março":"OS EEc MF AL", 
                        "04 - Abril":"OS EEc MF AL", 
                        "05 - Maio":"OS EEc MF AL", 
                        "06 - Junho":"OS EEc MF AL", 
                        "07 - Julho":"OS EEc MF AL", 
                        "08 - Agosto":"OS EEc MF AL", 
                        "09 - Setembro":"OS EEc MF AL", 
                        "10 - Outubro":"OS EEc MF AL", 
                        "11 - Novembro":"OS EEc MF AL", 
                        # "12 - Dezembro":"OS EEc MF",
                    },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EEe AL",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL", 
                    "05 - MAIO":"OS EEe AL", 
                    "06 - JUNHO":"OS EEe AL", 
                    "07 - JULHO":"OS EEe AL", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "CABEAMENTO":{
                    "OPEN":{
                        "08 - AGOSTO":"EEcx",
                        "09 - SETEMBRO":"EEcx",
                        "10 - OUTUBRO":"EEcx",
                        "11 - NOVEMBRO":"EEcx",
                        "12 - DEZEMBRO":"EEcx",
                    },
                    "MAINFRAME":{
                        "03 - MARÇO":"OS EE MFC ",
                        "04 - ABRIL":"OS EE MFC",
                        "05 - MAIO":"OS EE cx MF ",
                        "10 - OUTUBRO":"OS EE MF ",
                    },
                },
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"Os EERL ", 
                    "02 - FEVEREIRO":"OS EERL ", 
                    "03 - MARÇO":"OS EERL ", 
                    "04 - ABRIL":"EERL", 
                    "05 - MAIO":"EERL", 
                    "06 - JUNHO":"EERL", 
                    "07 - JULHO":"EERL", 
                    "08 - AGOSTO":"EERL", 
                    "09 - SETEMBRO":"EERL", 
                    "10 - OUTUBRO":"EERL", 
                    "11 - NOVEMBRO":"EERL", 
                    "12 - DEZEMBRO":"EERL",
                },
                "ELÉTRICA":{},
                "MANUTENÇÃO":{}
            },
            "PRÉDIO PRATA E VERMELHO":{
                "01 - janeiro":"EEc Pv",
                "05 - Maio": "EEc Pv"
            },

        },
        "2018":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc", 
                        "02 - FEVEREIRO":"EEc", 
                        "03 - MARÇO":"OS EEc", 
                        "04 - ABRIL":"OS EEc", 
                        "05 - MAIO":"EEc", 
                        "06 - JUNHO":"EEC", 
                        "07 - JULHO":"EEc", 
                        "08 - AGOSTO":"EEc", 
                        "09 - SETEMBRO":"EEc", 
                        "10 - OUTUBRO":"EEc", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ", 
                    },
                    "MAINFRAME":{
                        "01 - Janeiro":"EE MF ", 
                        "02 - Fevereiro":"EE MF ", 
                        "03 - Março":"EE MF ", 
                        "04 - Abril":"EE MF ", 
                        "05 - Maio":"OS EE MF ", 
                        "06 - Junho":"OS EE MF ", 
                        "07 - Julho":"EE MF", 
                        "08 - Agosto":"EE MF ", 
                        "09 - Setembro":"EE MF ", 
                        "10 - Outubro":"OS EE MF ", 
                        "11 - Novembro":"EE MF ", 
                        "12 - Dezembro":"EE MF", 
                    }
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe", 
                    "02 - FEVEREIRO":"OS EEe", 
                    "03 - MARÇO":"OS EEe", 
                    "04 - ABRIL":"EEe ", 
                    "05 - MAIO":"OS EEe", 
                    "06 - JUNHO":"OS EEe", 
                    "07 - JULHO":"OS EEe", 
                    "08 - AGOSTO":"OS EEe", 
                    "09 - SETEMBRO":"OS EEe", 
                    "10 - OUTUBRO":"OS EEe", 
                    "11 - NOVEMBRO":"OS EEe", 
                    "12 - DEZEMBRO":"OS EEe",  
                },
                "MANUTENÇÃO":{
                    "01 - Janeiro":{"manutenção corretiva": "",
                                    "manutenção preventiva": "OS EEm "}, 
                    
                    "02 - Fevereiro":{"Manutenção Corretiva": "OS EEmc ",
                                    "Manutenção Preventiva": "OS EEm "}, 
                    
                    "03 - Março":{"Manutenção Corretiva": "OS EEmc ",
                                "Manutenção Preventiva": "OS EEm "}, 
                    
                    "04 - Abril":{"Manutenção Corretiva": "OS EEmc ",
                                "Manutenção Preventiva": "OS EEm "},
                    
                    "05 - Maio":{"Manutenção Corretiva": "OS EEMC ",
                                "Manutenção Preventiva": "OS EEm "}, 
                    
                    "06 - Junho":{"Manutenção Corretiva": "OS EEmc ",
                                "Manutenção Preventiva": "OS EEm "}, 
                    
                    "07 - Julho":{"Manutenção Corretiva": "OS EEmc",
                                "Manutenção Preventiva": "OS EEm "}, 
                    
                    "08 - Agosto":{"Manutenção Corretiva": "OS EEmc",
                                "Manutenção Preventiva": "OS EEm "}, 
                    
                    "09 - Setembro":"OS EEm ",
                    
                    "10 - Outubro":{"Corretiva": "",
                                "Preventiva": "OS EEm "}, 
                    
                    "11 - Novembro":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "12 - Dezembro":{"Corretiva": "OS EEmc ",}
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"OS EEc AL",
                        "02 - FEVEREIRO":"OS EEc AL", 
                        "03 - MARÇO":"OS EEc AL", 
                        "04 - ABRIL":"OS EEc AL", 
                        "05 - MAIO":"OS EEc AL", 
                        "06 - JUNHO":"OS EEc AL", 
                        "07 - JULHO":"OS EEc AL", 
                        "08 - AGOSTO":"OS EEc AL", 
                        "09 - SETEMBRO":"OS EEc AL", 
                        "10 - OUTUBRO":"OS EEc AL", 
                        "11 - NOVEMBRO":"OS EEc AL", 
                        "12 - DEZEMBRO":"OS EEc AL",
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"OS EEc MF AL",
                        "02 - FEVEREIRO":"OS EEc MF AL", 
                        "03 - MARÇO":"OS EEc MF AL", 
                        "04 - ABRIL":"OS EEc MF AL", 
                        "05 - MAIO":"OS EEc MF AL", 
                        "06 - JUNHO":"OS EEc MF AL", 
                        "07 - JULHO":"OS EEc MF AL", 
                        "08 - AGOSTO":"OS EEc MF AL", 
                        "09 - SETEMBRO":"OS EEc MF AL", 
                        "10 - OUTUBRO":"OS EEc MF AL", 
                        "11 - NOVEMBRO":"OS EEc MF AL", 
                        # "12 - DEZEMBRO":"OS EEc MF",
                    },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EEe AL",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL", 
                    "05 - MAIO":"OS EEe AL", 
                    "06 - JUNHO":"OS EEe AL", 
                    "07 - JULHO":"OS EEe AL", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    # "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "CABEAMENTO":{
                    "01 - Janeiro": "EECX",
                    "02 - Fevereiro":"EEcx",
                    "03 - Março":"EEcx",
                    "04 - Abril":"EEcx",
                    "05 - Maio":"EEcx",
                    "06 - Junho":"EEcx",
                    "07 - Julho":"EEcx",
                    "08 - Agosto":"EEcx",
                    "09 - Setembro":"EEcx",
                    "10 - Outubro":"EEcx",
                    "11 - Novembro":"EEcx",
                    "12 - Dezembro":"EEcx",
                    
                },
                "ELÉTRICA":{
                    "06 - JUNHO":"EEeX ",
                    "07 - JULHO":"EEeX ",
                    "08 - AGOSTO":"EEeX ",
                    "09 - SETEMBRO":"OS EE ",
                    "10 - OUTUBRO":"RES OS EE ",

                },
                "MANUTENÇÃO":{}
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - Janeiro":"EERL", 
                    "02 - Fevereiro":"", 
                    "03 - Março":"EERL", 
                    "04 - Abril":"EERL ", 
                    "05 - Maio":"EERL", 
                    "06 - Junho":"EERL", 
                    "07 - Julho":"EERL", 
                    "08 - Agosto":"EERL", 
                    "09 - Setembro":"EERL", 
                    "10 - Outubro":"EERL", 
                    "11 - Novembro":"EERL", 
                    "12 - Dezembro":"EERL",
                },
                "ELÉTRICA":{
                    "DEZEMBRO": "OS EERL"
                },
                "MANUTENÇÃO":{
                    
                }
            }

        },
        "2019":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc", 
                        "02 - FEVEREIRO":"EEc", 
                        "03 - MARÇO":"OS EEc", 
                        "04 - ABRIL":"OS EEc", 
                        "05 - MAIO":"EEc", 
                        "06 - JUNHO":"EEC", 
                        "07 - JULHO":"EEc", 
                        "08 - AGOSTO":"EEc", 
                        "09 - SETEMBRO":"EEc", 
                        "10 - OUTUBRO":"EEc", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ", 
                    },
                    "MAINFRAME":{
                        "01 - Janeiro":"EE MF ", 
                        "02 - Fevereiro":"EE MF ", 
                        "03 - Março":"EE MF ", 
                        "04 - Abril":"EE MF ", 
                        "05 - Maio":"OS EE MF ", 
                        "06 - Junho":"OS EE MF ", 
                        "07 - Julho":"EE MF", 
                        "08 - Agosto":"EE MF ", 
                        "09 - Setembro":"EE MF ", 
                        "10 - Outubro":"OS EE MF ", 
                        "11 - Novembro":"EE MF ", 
                        # "12 - Dezembro":"EE MF", 
                    }
                },
                "ELÉTRICA":{
                    "01 - Janeiro":"OS EEe", 
                    "02 - Fevereiro":"OS EEe", 
                    "03 - Março":"OS EEe", 
                    "04 - Abril":"OS EEe ", 
                    "05 - Maio":"OS EEe", 
                    "06 - Junho":"OS EEe", 
                    "07 - Julho":"OS EEe", 
                    "08 - Agosto":"OS EEe", 
                    "09 - Setemrbo":"OS EEe", 
                    "10 - Outubro":"OS EEe", 
                    "11 - Novembro":"OS EEe", 
                    "12 - Dezembro":"OS EEe",  
                },
                "MANUTENÇÃO":{
                    "01 - Janeiro":{"CORRETIVA": "OS EEmc ",
                                    "PREVENTIVA": "OS EEm "}, 
                    
                    "02 - Fevereiro":{"Corretiva": "OS EEmc ",
                                    "Preventiva": "OS EEm "}, 
                    
                    "03 - Março":{"Corretiva": "",
                                "Preventiva": "OS EEm "}, 
                    
                    "04 - Abril":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "05 - Maio":{"Corretiva": "OS EEMC ",
                                "Preventiva": "OS EEm "}, 
                    
                    "06 - Junho":{"Corretiva": "",
                                "Preventiva": "OS EEm "}, 
                    
                    "07 - Julho":{"Corretiva": "OS EEmc",
                                "Preventiva": "OS EEm "}, 
                    
                    "08 - Agosto":{"Corretiva": "EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "09 - Setembro":{"Corretiva": "EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "10 - Outubro":{"Preventiva": "OS EEm "}, 
                    
                    "11 - Novembro":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "12 - Dezembro":"OS EEm "
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"OS EEc AL",
                        "02 - FEVEREIRO":"OS EEc AL", 
                        "03 - MARÇO":"OS EEc AL", 
                        "04 - ABRIL":"OS EEc AL", 
                        "05 - MAIO":"OS EEc AL", 
                        "06 - JUNHO":"OS EEc AL", 
                        "07 - JULHO":"OS EEc AL", 
                        "08 - AGOSTO":"OS EEc AL", 
                        "09 - SETEMBRO":"OS EEc AL", 
                        "10 - OUTUBRO":"OS EEc AL", 
                        "11 - NOVEMBRO":"OS EEc AL", 
                        "12 - DEZEMBRO":"OS EEc AL",
                    },
                    "MAINFRAME":{
                        # "01 - JANEIRO":"OS EEc MF AL",
                        "02 - FEVEREIRO":"OS EEc MF AL", 
                        "03 - MARÇO":"OS EEc MF AL", 
                        "04 - ABRIL":"OS EEc MF AL", 
                        "05 - MAIO":"OS EEc MF AL", 
                        "06 - JUNHO":"OS EEc MF AL", 
                        "07 - JULHO":"OS EEc MF AL", 
                        "08- AGOSTO":"OS EEc MF AL", 
                        "09- SETEMBRO":"OS EEc MF AL", 
                        "10 - OUTUBRO":"OS EEc MF AL", 
                        "11 - NOVEMBRO":"OS EEc MF AL", 
                        # "12 - DEZEMBRO":"OS EEc MF",
                    },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EEe AL",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL", 
                    "05 - MAIO":"OS EEe AL", 
                    "06 - JUNHO":"OS EEe AL", 
                    "07 - JULHO":"OS EEe AL", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    # "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "CABEAMENTO":{
                    "01 - Janeiro": "EECX",
                    "02 - Fevereiro":"EECX",
                    "03 - Março":"EECX",
                    "04 - Abril":"EECX",
                    "05 - Maio":"EECX",
                    "06 - Junho":"EECX",
                    "07 - Julho":"EECX",
                    "08 - Agosto":"EECX",
                    "09 - Setembro":"EECX",
                    "10 - Outubro":"EEcx",
                    "11 - Novembro":"EEcx",
                    "12 - Dezembro":"EEcx",
                    
                },
                "ELÉTRICA":{
                    "02 - FEVEREIRO": "RES OSS EE",
                    "04 - ABRIL":"RES OS EE",
                    
                    "09 - SETEMBRO":"OS EE ",
                    

                },
                "MANUTENÇÃO":{}
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - Janeiro":"EERL", 
                    "02 - Fevereiro":"EERL", 
                    "03 - Março":"EE RL ", 
                    "04 - Abril":"EE RL ", 
                    "05 - Maio":"EERL ", 
                    "06 - Junho":"EERL ", 
                    "07 - Julho":"EERL ", 
                    "08 - Agosto":"EERL ", 
                    "09 - Setembro":"EERL ", 
                    "10 - Outubro":"EERL ", 
                    "11 - Novembro":"EERL ", 
                    # "12 - Dezembro":"EERL",
                },
                "ELÉTRICA":{
                    "DEZEMBRO": "OS EERL ",
                    "NOVEMBRO": "OS EERL ",
                    "OUTUBRO":"OS EERL ",
                },
                "MANUTENÇÃO":"OS EEMRL ",
            }

        },
        "2020":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc", 
                        "02 - FEVEREIRO":"EEc", 
                        "03 - MARÇO":"OS EEc", 
                        "04 - ABRIL":"OS EEc", 
                        "05 - MAIO":"EEc", 
                        "06 - JUNHO":"EEC", 
                        "07 - JULHO":"EEc", 
                        "08 - AGOSTO":"EEc", 
                        "09 - SETEMBRO":"EEc", 
                        "10 - OUTUBRO":"EEc", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ",
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"EE MF ", 
                        "02 - FEVEREIRO":"EE MF ", 
                        "03 - MARÇO":"EE MF ", 
                        # "04 - ABRIL":"EE MF ", 
                        # "05 - MAIO":"EEc", 
                        "06 - JUNHO":"EE MF ", 
                        "07 - JULHO":"EE MF ", 
                        "08 - AGOSTO":"EE MF ", 
                        "09 - SETEMBRO":"EE MF ", 
                        "10 - OUTUBRO":"EE MF ", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ",
                    },
                    
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe", 
                    "02 - FEVEREIRO":"OS EEe", 
                    "03 - MARÇO":"OS EEe", 
                    "04 - ABRIL":"OS EEe", 
                    "05 - MAIO":"OS EEe", 
                    "06 - JUNHO":"OS EEe", 
                    "07 - JULHO":"OS EEe", 
                    "08 - AGOSTO":"OS EEe", 
                    "09 - SETEMBRO":"OS EEe", 
                    "10 - OUTUBRO":"OS EEe", 
                    "11 - NOVEMBRO":"OS EEe", 
                    "12 - DEZEMBRO":"OS EEe",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO":{"Preventiva": "OS EEm "}, 
                    
                    "02 - FEVEREIRO":{"Preventiva": "OS EEm "}, 
                    
                    "03 - MARÇO":{"Preventiva": "OS EEm "}, 
                    
                    "04 - ABRIL":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "05 - MAIO":{"Preventiva": "OS EEm "}, 
                    
                    "06 - JUNHO":{"Corretiva": "OS EEmc",
                                "Preventiva": "OS EEm "}, 
                    
                    "07 - JULHO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm"}, 
                    
                    "08 - AGOSTO":{"Corretiva": "EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "09 - SETEMBRO":{"Corretiva": "OS EEmc",
                                "Preventiva": "OS EEm "},
                    
                    "10 - OUTUBRO":{"Preventiva": "OS EEm "}, 
                    
                    "11 - NOVEMBRO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "12 - DEZEMBRO":"OS EEm "
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"OS EEc AL",
                        "02 - FEVEREIRO":"OS EEc AL", 
                        "03 - MARÇO":"OS EEc AL", 
                        "04 - ABRIL":"OS EEc AL", 
                        "05 - MAIO":"OS EEc AL", 
                        "06 - JUNHO":"OS EEc AL", 
                        "07 - JULHO":"OS EEc AL", 
                        "08 - AGOSTO":"OS EEc AL", 
                        "09 - SETEMBRO":"OS EEc AL", 
                        "10 - OUTUBRO":"OS EEc AL", 
                        "11 - NOVEMBRO":"OS EEc AL", 
                        "12 - DEZEMBRO":"OS EEc AL",
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"OS EEc MF AL",
                        "02 - FEVEREIRO":"OS EEc MF AL", 
                        "03 - MARÇO":"OS EEc MF AL", 
                        "04 - ABRIL":"OS EEc MF AL", 
                        "05 - MAIO":"OS EEc MF AL", 
                        "06 - JUNHO":"OS EEc MF AL", 
                        "07 - JULHO":"OS EEc MF AL", 
                        "08- AGOSTO":"OS EEc MF AL", 
                        "09- SETEMBRO":"OS EEc MF AL", 
                        "10 - OUTUBRO":"OS EEc MF AL", 
                        "11 - NOVEMBRO":"OS EEc MF AL", 
                        "12 - DEZEMBRO":"OS EEc MF",
                    },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EEe AL",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL", 
                    "05 - MAIO":"OS EEe AL", 
                    "06 - JUNHO":"OS EEe AL", 
                    "07 - JULHO":"OS EEe AL", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "CABEAMENTO":{
                    "01 - JANEIRO":"EECX",
                    "02 - FEVEREIRO":"EECX", 
                    "03 - MARÇO":"EECX", 
                    "04 - ABRIL":"EECX", 
                    "05 - MAIO":"EECX", 
                    "06 - JUNHO":"EECX", 
                    "07 - JULHO":"EECX", 
                    "08 - AGOSTO":"EECX", 
                    "09 - SETEMBRO":"EECX", 
                    "10 - OUTUBRO":"EECX", 
                    "11 - NOVEMBRO":"EECX", 
                    "12 - DEZEMBRO":"EECX",
                },
                "ELÉTRICA":{      },
                "MANUTENÇÃO":{}
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"EERL",
                    "02 - FEVEREIRO":"EERL", 
                    "03 - MARÇO":"EERL", 
                    "04 - ABRIL":"EERL", 
                    "05 - MAIO":"EERL", 
                    "06 - JUNHO":"EERL", 
                    "07 - JULHO":"EERL", 
                    "08 - AGOSTO":"EERL", 
                    "09 - SETEMBRO":"EERL", 
                    "10 - OUTUBRO":"EERL", 
                    "11 - NOVEMBRO":"EERL", 
                    "12 - DEZEMBRO":"EECX",
                    # "12 - DEZEMBRO":"EERL",
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO":"EEMRL", 
                    "02- FEVEREIRO":"OS EEMRL",  
                    "08 - AGOSTO":"OS EEMRL", 
                    
                },
            }

        },
        "2021":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc", 
                        "02 - FEVEREIRO":"EEc", 
                        "03 - MARÇO":"OS EEc", 
                        "04 - ABRIL":"OS EEc", 
                        "05 - MAIO":"EEc", 
                        "06 - JUNHO":"EEC", 
                        "07 - JULHO":"EEc", 
                        "08 - AGOSTO":"EEc", 
                        "09 - SETEMBRO":"EEc", 
                        "10 - OUTUBRO":"EEc", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ",
                        
                    },
                    "MAINFRAME":{
                            "01 - JANEIRO":"EE MF ", 
                            "02 - FEVEREIRO":"EE MF ", 
                            "03 - MARÇO":"EE MF ", 
                            # "04 - ABRIL":"EE MF ", 
                            "05 - MAIO":"EE MF ", 
                            "06 - JUNHO":"EE MF ", 
                            "07 - JULHO":"EE MF ", 
                            "08 - AGOSTO":"EE MF ", 
                            "09 - SETEMBRO":"EE MF ", 
                            "10 - OUTUBRO":"EE MF ", 
                            "11 - NOVEMBRO":"EE MF ", 
                            "12 - DEZEMBRO":"EE MF ",
                        },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe", 
                    "02 - FEVEREIRO":"OS EEe", 
                    "03 - MARÇO":"OS EEe", 
                    "04 - ABRIL":"OS EEe", 
                    "05 - MAIO":"OS EEe", 
                    "06 - JUNHO":"OS EEe", 
                    "07 - JULHO":"OS EEe", 
                    "08 - AGOSTO":"OS EEe", 
                    "09 - SETEMBRO":"OS EEe", 
                    "10 - OUTUBRO":"OS EEe", 
                    "11 - NOVEMBRO":"OS EEe", 
                    "12 - DEZEMBRO":"OS EEe",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO":{"Preventiva": "OS EEm ",
                                    "Corretiva":"OS EEmc "}, 
                    
                    "02 - FEVEREIRO":{"Preventiva": "OS EEm "}, 
                    
                    "03 - MARÇO":{"Preventiva": "OS EEm "}, 
                    
                    "04 - ABRIL":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "05 - MAIO":{"Preventiva": "OS EEm "}, 
                    
                    "06 - JUNHO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "07 - JULHO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "08 - AGOSTO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "09 - SETEMBRO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "10 - OUTUBRO":{"Preventiva": "OS EEm ",
                                    "Corretiva": "OS EEmc "}, 
                    
                    "11 - NOVEMBRO":{"Preventiva": "OS EEm "},
                    
                    "12 - DEZEMBRO":{"PREVENTIVA": "OS EEm "}
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"OS EEc AL",
                        "02 - FEVEREIRO":"OS EEc AL", 
                        "03 - MARÇO":"OS EEc AL", 
                        "04 - ABRIL":"OS EEc AL", 
                        "05 - MAIO":"OS EEc AL", 
                        "06 - JUNHO":"OS EEc AL", 
                        "07 - JULHO":"OS EEc AL", 
                        "08 - AGOSTO":"OS EEc AL", 
                        "09 - SETEMBRO":"OS EEc AL", 
                        "10 - OUTUBRO":"OS EEc AL", 
                        "11 - NOVEMBRO":"OS EEc AL", 
                        "12 - DEZEMBRO":"OS EEc AL",
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"OS EEc MF AL",
                        "02 - FEVEREIRO":"OS EEc MF AL", 
                        "03 - MARÇO":"OS EEc MF AL", 
                        "04 - ABRIL":"OS EEc MF AL", 
                        "05 - MAIO":"OS EEc MF AL", 
                        "06 - JUNHO":"OS EEc MF AL", 
                        "07 - JULHO":"OS EEc MF AL", 
                        "08- AGOSTO":"OS EEc MF AL", 
                        "09- SETEMBRO":"OS EEc MF AL", 
                        "10 - OUTUBRO":"OS EEc MF AL", 
                        "11 - NOVEMBRO":"OS EEc MF AL", 
                        # "12 - DEZEMBRO":"OS EEc MF AL",
                    },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EEe AL",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL", 
                    "05 - MAIO":"OS EEe AL", 
                    "06 - JUNHO":"OS EEe AL", 
                    "07 - JULHO":"OS EEe AL", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "CABEAMENTO":{
                    "01 - JANEIRO":"EECX",
                    "02 - FEVEREIRO":"EECX", 
                    "03 - MARÇO":"EECX", 
                    "04 - ABRIL":"EECX", 
                    "05 - MAIO":"EECX", 
                    "06 - JUNHO":"EECX", 
                    "07 - JULHO":"EECX", 
                    "08 - AGOSTO":"EECX", 
                    "09 - SETEMBRO":"EECX", 
                    "10 - OUTUBRO":"EECX", 
                    "11 - NOVEMBRO":"EECX ", 
                    "12 - DEZEMBRO":"EECX",
                },
                "ELÉTRICA":{      },
                "MANUTENÇÃO":{}
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"OS EERL",
                    "02 - FEVEREIRO":"EERL", 
                    "03 - MARÇO":"EERL", 
                    "04 - ABRIL":"EERL", 
                    "05 - MAIO":"EERL ", 
                    "06 - JUNHO":"EERL", 
                    "07 - JULHO":"EERL", 
                    "08 - AGOSTO":"EERL", 
                    "09 - SETEMBRO":"EERL", 
                    "10 - OUTUBRO":"EERL", 
                    "11 - NOVEMBRO":"EERL", 
                    # "12 - DEZEMBRO":"EECX",
                    "12 - DEZEMBRO":"EER",
                },
                "ELÉTRICA":{
                    "05 - MAIO":"EERL",
                },
                "MANUTENÇÃO":{},
            }

        },
        "2022":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc", 
                        "02 - FEVEREIRO":"EEc", 
                        "03 - MARÇO":"OS EEc", 
                        "04 - ABRIL":"OS EEc", 
                        "05 - MAIO":"EEc", 
                        "06 - JUNHO":"EEC", 
                        "07 - JULHO":"EEc", 
                        "08 - AGOSTO":"EEc", 
                        "09 - SETEMBRO":"EEc", 
                        "10 - OUTUBRO":"EEc", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ",
                        
                    },
                    "MAINFRAME":{
                            "01 - JANEIRO":"EE MF ", 
                            "02 - FEVEREIRO":"OS EE MF ", 
                            "03 - MARÇO":"OS EE MF ", 
                            "04 - ABRIL":"OS EE MF ", 
                            "05 - MAIO":"OS EE MF ", 
                            "06 - JUNHO":"OS EE MF ", 
                            "07 - JULHO":"OS EE MF ", 
                            "08 - AGOSTO":"OS EE MF ", 
                            "09 - SETEMBRO":"OS EE MF ", 
                            "10 - OUTUBRO":"OS EE MF ", 
                            "11 - NOVEMBRO":"OS EE MF ", 
                            "12 - DEZEMBRO":"OS EE MF ",
                        },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe", 
                    "02 - FEVEREIRO":"OS EEe", 
                    "03 - MARÇO":"OS EEe", 
                    "04 - ABRIL":"OS EEe", 
                    "05 - MAIO":"OS EEe", 
                    "06 - JUNHO":"OS EEe", 
                    "07 - JULHO":"OS EEe", 
                    "08 - AGOSTO":"OS EEe", 
                    "09 - SETEMBRO":"OS EEe", 
                    "10 - OUTUBRO":"OS EEe", 
                    "11 - NOVEMBRO":"OS EEe", 
                    "12 - DEZEMBRO":"OS EEe",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO":{"Preventiva": "OS EEm ",
                                    "Corretiva":"OS EEmc "}, 
                    
                    "02 - FEVEREIRO":{"Corretiva":"OS EEmc ",
                        "Preventiva": "OS EEm "}, 
                    
                    "03 - MARÇO":{"Corretiva":"OS EEmc ",
                        "Preventiva": "OS EEm "}, 
                    
                    "04 - ABRIL":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "05 - MAIO":{"Preventiva": "OS EEm "}, 
                    
                    "06 - JUNHO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "07 - JULHO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "08 - AGOSTO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "09 - SETEMBRO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "10 - OUTUBRO":{"Preventiva": "OS EEm ",
                                    "Corretiva": "OS EEmc "}, 
                    
                    "11 - NOVEMBRO":{"Preventiva": "OS EEm "},
                    
                    "12 - DEZEMBRO":{"PREVENTIVA": "OS EEm "}
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"OS EEc AL",
                        "02 - FEVEREIRO":"OS EEc AL", 
                        "03 - MARÇO":"OS EEc AL", 
                        "04 - ABRIL":"OS EEc AL", 
                        "05 - MAIO":"OS EEc AL", 
                        "06 - JUNHO":"OS EEc AL", 
                        "07 - JULHO":"OS EEc AL", 
                        "08 - AGOSTO":"OS EEc AL", 
                        "09 - SETEMBRO":"OS EEc AL", 
                        "10 - OUTUBRO":"OS EEc AL", 
                        "11 - NOVEMBRO":"OS EEc AL", 
                        "12 - DEZEMBRO":"OS EEc AL",
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"OS EEc MF AL",
                        "02 - FEVEREIRO":"OS EEc MF AL", 
                        "03 - MARÇO":"OS EEc MF AL", 
                        "04 - ABRIL":"OS EEc MF AL", 
                        "05 - MAIO":"OS EEc MF AL", 
                        "06 - JUNHO":"OS EEc MF AL", 
                        "07 - JULHO":"OS EEc MF AL", 
                        "08- AGOSTO":"OS EEc MF AL", 
                        "09- SETEMBRO":"OS EEc MF AL", 
                        "10 - OUTUBRO":"OS EEc MF AL", 
                        "11 - NOVEMBRO":"OS EEc MF AL", 
                        "12 - DEZEMBRO":"OS EEc MF AL",
                    },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EEe AL",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL", 
                    "05 - MAIO":"OS EEe AL", 
                    "06 - JUNHO":"OS EEe AL", 
                    "07 - JULHO":"OS EEe AL", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "01 - JANEIRO":"EECX",
                "02 - FEVEREIRO":"EECX", 
                "03 - MARÇO":"EECX", 
                "04 - ABRIL":"EECX", 
                "05 - MAIO":"EECX", 
                "06 - JUNHO":"EECX", 
                "07 - JULHO":"EECX", 
                "08 - AGOSTO":"EECX", 
                "09 - SETEMBRO":"EECX", 
                "10 - OUTUBRO":"EECX", 
                "11 - NOVEMBRO":"EECX ", 
                "12 - DEZEMBRO":"EECX",
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"EERL",
                    # "02 - FEVEREIRO":"EERL",
                    "03 - MARÇO":"EERL", 
                    "04 - ABRIL":"EERL", 
                    "05 - MAIO":"EE RL ", 
                    "06 - JUNHO":"EERL", 
                    "07 - JULHO":"EERL", 
                    "08 - AGOSTO":"EERL", 
                    "09 - SETEMBRO":"EERL", 
                    "10 - OUTUBRO":"EERL", 
                },
                "MANUTENÇÃO":{},
            }

        },
        "2023":{
            "01 - CTI":{
                "CABEAMENTO": {
                    "OPEN":{
                        "01 - JANEIRO":"EEc", 
                        "02 - FEVEREIRO":"EEc", 
                        "03 - MARÇO":"OS EEc", 
                        "04 - ABRIL":"OS EEc", 
                        "05 - MAIO":"EEc", 
                        "06 - JUNHO":"EEC", 
                        "07 - JULHO":"EEc", 
                        "08 - AGOSTO":"EEc", 
                        "09 - SETEMBRO":"EEc", 
                        "10 - OUTUBRO":"EEc", 
                        "11 - NOVEMBRO":"EEc ", 
                        "12 - DEZEMBRO":"EEc ",
                        
                    },
                    "MAINFRAME":{
                            "01 - JANEIRO":"EE MF ", 
                            "02 - FEVEREIRO":"OS EE MF ", 
                            "03 - MARÇO":"OS EEc MF ", 
                            "04 - ABRIL":"OS EE MF ", 
                            "05 - MAIO":"OS EE MF ", 
                            "06 - JUNHO":"OS EE MF ", 
                            "07 - JULHO":"OS EE MF ", 
                            "08 - AGOSTO":"OS EE MF ", 
                            "09 - SETEMBRO":"EEc MF ", 
                            "10 - OUTUBRO":"EEc MF ", 
                            "11 - NOVEMBRO":"EEc MF ", 
                            # "12 - DEZEMBRO":"OS EE MF ",
                        },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO":"OS EEe", 
                    "02 - FEVEREIRO":"OS EEe", 
                    "03 - MARÇO":"OS EEe", 
                    "04 - ABRIL":"OS EEe", 
                    "05 - MAIO":"OS EEe", 
                    "06 - JUNHO":"OS EEe", 
                    "07 - JULHO":"OS EEe", 
                    "08 - AGOSTO":"OS EEe", 
                    "09 - SETEMBRO":"OS EEe", 
                    "10 - OUTUBRO":"OS EEe", 
                    "11 - NOVEMBRO":"OS EEe", 
                    "12 - DEZEMBRO":"OS EEe",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO":{"Preventiva": "OS EEm ",
                                    "Corretiva":"OS EEmc "}, 
                    
                    "02 - FEVEREIRO":{"Corretiva":"OS EEmc ",
                        "Preventiva": "OS EEm "}, 
                    
                    "03 - MARÇO":{"Corretiva":"OS EEmc ",
                        "Preventiva": "OS EEm "}, 
                    
                    "04 - ABRIL":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "05 - MAIO":{"Preventiva": "OS EEm "}, 
                    
                    "06 - JUNHO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "07 - JULHO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "08 - AGOSTO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "}, 
                    
                    "09 - SETEMBRO":{"Corretiva": "OS EEmc ",
                                "Preventiva": "OS EEm "},
                    
                    "10 - OUTUBRO":{"Preventiva": "OS EEm ",
                                    "Corretiva": "OS EEmc "}, 
                    
                    "11 - NOVEMBRO":{"Preventiva": "OS EEm "},
                    
                    "12 - DEZEMBRO":{"PREVENTIVA": "OS EEm "}
                }
            },
            "02 - ALPHAVILLE":{
                "CABEAMENTO LÓGICO": {
                    "OPEN":{
                        "01 - JANEIRO":"OS EEc AL",
                        "02 - FEVEREIRO":"OS EEc AL", 
                        "03 - MARÇO":"OS EEc AL", 
                        "04 - ABRIL":"OS EEc AL", 
                        "05 - MAIO":"OS EEc AL", 
                        "06 - JUNHO":"OS EEc AL", 
                        "07 - JULHO":"OS EEc AL", 
                        "08 - AGOSTO":"OS EEc AL", 
                        "09 - SETEMBRO":"OS EEc AL", 
                        "10 - OUTUBRO":"OS EEc AL", 
                        "11 - NOVEMBRO":"OS EEc AL", 
                        "12 - DEZEMBRO":"OS EEc AL",
                    },
                    "MAINFRAME":{
                        "01 - JANEIRO":"OS EEc MF AL",
                        "02 - FEVEREIRO":"OS EEc MF AL", 
                        "03 - MARÇO":"OS EEc MF AL", 
                        "04 - ABRIL":"OS EEc MF AL", 
                        "05 - MAIO":"OS EEc MF AL", 
                        "06 - JUNHO":"OS EEc MF AL", 
                        "07 - JULHO":"OS EEc MF AL", 
                        "08- AGOSTO":"OS EEc MF AL", 
                        "09- SETEMBRO":"OS EEc MF AL", 
                        "10 - OUTUBRO":"OS EEc MF AL", 
                        "11 - NOVEMBRO":"OS EEc MF AL", 
                        "12 - DEZEMBRO":"OS EEc MF AL",
                    },
                },
                "ELÉTRICA":{
                    "01 - JANEIRO": "OS EEe AL",
                    "02 - FEVEREIRO":"OS EEe AL", 
                    "03 - MARÇO":"OS EEe AL", 
                    "04 - ABRIL":"OS EEe AL", 
                    "05 - MAIO":"OS EEe AL", 
                    "06 - JUNHO":"OS EEe AL", 
                    "07 - JULHO":"OS EEe AL", 
                    "08 - AGOSTO":"OS EEe AL", 
                    "09 - SETEMBRO":"OS EEe AL", 
                    "10 - OUTUBRO":"OS EEe AL", 
                    "11 - NOVEMBRO":"OS EEe AL",
                    "12 - DEZEMBRO":"OS EEe AL",  
                },
                "MANUTENÇÃO":{
                    "01 - JANEIRO": "OS EEm AL",
                    "02 - FEVEREIRO":"OS EEm AL", 
                    "03 - MARÇO":"OS EEm AL", 
                    "04 - ABRIL":"OS EEm AL", 
                    "05 - MAIO":"OS EEm AL", 
                    "06 - JUNHO":"OS EEm AL", 
                    "07 - JULHO":"OS EEm AL", 
                    "08 - AGOSTO":"OS EEm AL", 
                    "09 - SETEMBRO":"OS EEm AL", 
                    "10 - OUTUBRO":"OS EEm AL", 
                    "11 - NOVEMBRO":"OS EEm AL",
                    "12 - DEZEMBRO":"OS EEm AL", 
                }
            },
            "03 - XAXIM":{
                "01 - JANEIRO":"EECX",
                "02 - FEVEREIRO":"EECX", 
                "03 - MARÇO":"EECX", 
                "04 - ABRIL":"EECX", 
                "05 - MAIO":"EECX", 
                "06 - JUNHO":"EECX", 
                "07 - JULHO":"EECX", 
                "08 - AGOSTO":"EECX", 
                "09 - SETEMBRO":"EECX", 
                "10 - OUTUBRO":"EECX", 
                "11 - NOVEMBRO":"EECX ", 
                "12 - DEZEMBRO":"EECX",
            },
            "04 - REDE LAN":{
                "CABEAMENTO": {
                    "01 - JANEIRO":"EERL",
                    "02 - FEVEREIRO":"EERL",
                    "03 - MARÇO":"EERL", 
                    "04 - ABRIL":"EERL", 
                    "05 - MAIO":"EE RL ", 
                    "06 - JUNHO":"EERL", 
                    "07 - JULHO":"OS EERL", 
                    # "08 - AGOSTO":"EERL", 
                    "09 - SETEMBRO":"OS EERL", 
                    "10 - OUTUBRO":"OS EERL", 
                    "11 - NOVEMBRO":"OS EERL",
                    "12 - DEZEMBRO":"OS EERL",
                },
                "MANUTENÇÃO":{},
            }

        },

    }
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