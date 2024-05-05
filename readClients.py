import pandas as pd
from dotenv import load_dotenv
import os
import psycopg2

def connect_to_postgres():
    try:
        load_dotenv()
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv('PGHOST'),
            database=os.getenv('PGDATABASE'),
            user=os.getenv('PGUSER'),
            password=os.getenv('PGPASSWORD'),
        )
        print("Connected to PostgreSQL!")
        return conn
    except Exception as e:
        print("Unable to connect to PostgreSQL:", e)
        return None

def read_excel_file(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# Example usage
if __name__ == "__main__":
    file_path = "Lista clienti.xlsx"  # Change this to the path of your Excel file
    data = read_excel_file(file_path)
    if data is not None:
        print("Data read successfully:")
        cleaned_data = data.dropna()
        selected_columns = data[['Ragione Sociale']]  # Replace 'Column1', 'Column2' with your desired column names
        selected_rows = selected_columns[selected_columns['Ragione Sociale'].isna() == False]
        print("\nSelected columns:")
        print(selected_columns)
        print("\nSelected rows")
        print(selected_rows)
        
    conn = connect_to_postgres()
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    print(df)
    
    for row in selected_rows.iterrows():
        rag_sociale = row[1]['Ragione Sociale']
        sql_query = f"INSERT INTO customers (nome) VALUES ('{rag_sociale}') ON CONFLICT (nome) DO NOTHING"
        print(sql_query)
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                print("Insertion successful!")
        except Exception as e:
            print("Error executing SQL query:", e)
        
# Commit the transaction
conn.commit()

# Close the database connection
conn.close()