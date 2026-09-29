import pandas as pd
import json
import os
class Analyzer:
    def __init__(self, filename,path,format):
        self.filename = filename
        self.path = path
        self.format = format
    def open_file(self):
        match self.format:
            case 'csv':
                df = pd.read_csv(self.path)
                print("CSV Data:")
                print(df)

            case 'json':
                with open(self.path, 'r') as f:
                    data = json.load(f)
                    print(f"JSON Data: {data}")
            case 'xlsx':
                    df = pd.read_excel(self.path)
                    print(f"Excel Data: {df}")
            case 'txt':
                    try:
                        # Read a number from a file
                        with open(self.path, 'r') as f:
                            text = f.read()


                        print(f"Result: {text}")
                    except FileNotFoundError:
                        print("Could not find number.txt")
                    except ValueError:
                        print("File doesn't contain a valid number")
                    except ZeroDivisionError:
                        print("Cannot divide by zero")






"""
# Read the CSV file
df = pd.read_csv('data/sales.csv')
print("CSV Data:")
print(df)
print(f"\nShape: {df.shape[0]} rows, {df.shape[1]} columns")
#Read other file format

# JSON
df = pd.read_json('data/file.json')
# or for simple JSON:
with open('data/config.json', 'r') as f:
    data = json.load(f)

# Excel
df = pd.read_excel('data/file.xlsx')

# Text files
with open('data/file.txt', 'r') as f:
    text = f.read()

# Quick operation: calculate total for each row
df['total'] = df['quantity'] * df['price']
print("\nWith totals:")
print(df)

# Create output directory
os.makedirs('output', exist_ok=True)

# Save as different formats
# 1. JSON format (good for web APIs)
df.to_json('output/sales_data.json', orient='records', indent=2)

# 2. Excel format (good for sharing)
df.to_excel('output/sales_data.xlsx', index=False)
df = pd.DataFrame({
    "date": df["date"],
    "product": df["product"],
    "quantity": df["quantity"],
    "price": df["price"],
})
df["date"] = df["date"].astype(str).str.replace(".", ",")
df["product"] = df["product"].astype(str).str.replace(".", ",")
df["quantity"] = df["quantity"].astype(str).str.replace(".", ",")
df["price"] = df["price"].astype(str).str.replace(".", ",")
# 3. Updated CSV (with our new total column)
df.to_csv('output/sales_with_totals.csv', index=False)

print("\nFiles saved:")
print("- output/sales_data.json")
print("- output/sales_data.xlsx")
print("- output/sales_with_totals.csv")
"""
