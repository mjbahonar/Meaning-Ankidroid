import csv

def replace_double_quotes(input_file, output_file, column_index):
    # Read the CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    # Replace '""' with '"' in the specified column
    for row in rows:
        if len(row) > column_index:
            row[column_index] = row[column_index].replace('""', '"')

    # Write the modified data back to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

# Usage
input_file = 'output_2024-06-21_11-15-55_test.csv'
output_file = 'output.csv'
column_index = 1  # Change this to the nth column (0-based index)

replace_double_quotes(input_file, output_file, column_index)
