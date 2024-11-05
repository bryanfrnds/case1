import pandas as pd
import pyodbc


excel_file_path = 'D:/Case1/case1-xlsm-sql-bi/usuarios.xlsm'  # Replace with the actual file path
sheet_name = 'tb_clientes'  


try:
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, engine='openpyxl')
    print("Excel file read successfully.")
    df.iloc[:, 2] = pd.to_datetime(df.iloc[:, 2], errors='coerce')
    print("Third column converted to datetime format.")


except Exception as e:
    print(f"Error reading Excel file: {e}")


server = 'ROMULUS'
database = 'case1'
username = 'sa'
password = 'admin'


connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

try:

    conn = pyodbc.connect(connection_string)
    print("Database connection established.")
    cursor = conn.cursor()


    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO TB_Clientes (NOME_DO_CLIENTE, CEP, DATA_DE_NASCIMENTO) 
            VALUES (?, ?, ?)
        """, row[0], row[1], row[2])


    conn.commit()
    print("Data inserted successfully into TB_Clientes.")

except pyodbc.Error as e:
    print(f"Database connection or operation error: {e}")

finally:

    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()