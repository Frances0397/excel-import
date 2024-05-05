import pandas as pd

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
        selected_columns = cleaned_data[['Codice', 'Ragione Sociale']]  # Replace 'Column1', 'Column2' with your desired column names
        print("\nSelected columns:")
        print(selected_columns)
