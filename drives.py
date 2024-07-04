import pyodbc

#  ! Microsoft Access Driver (*.mdb, *.accdb)
# msa_drivers = [x for x in pyodbc.drivers() if 'ACCESS' in x.upper()]
# print(f'msa_drivers= {msa_drivers}')

try: 
    con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Henrique\OneDrive\Anexos\FIAP_2024\OS_Procura\ControleDataBase.accdb'
    conn = pyodbc.connect(con_string)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tblControle")  # Ajuste a tabela para "tblControle"
    for row in cursor.fetchall():
        # Formatar a data
        # id, data, nome, status = row
        # data_formatada = data.strftime('%d/%m/%Y')
        # print((id, data_formatada, nome, status))
        print(row)

except pyodbc.Error as e:
    print(f'Error: {e}')
