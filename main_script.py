import pandas as pd
import os
import datetime
from scraper_functions import scrape_and_process_fastdic, scrape_and_process_faraazin_with_selenium, scrape_and_process_google_translate
import requests

# Read Excel file without headers
script_dir = os.path.dirname(os.path.abspath(__file__))
baseName = 'test'
excel_file_name  = baseName + '.xlsx'
excel_file_path = os.path.join(script_dir, excel_file_name)
df = pd.read_excel(excel_file_path, header=None, names=['Words'])

# Process each word and store results in the second and third columns
df['Processed_Content_Faraazin_Selenium'] = df.apply(lambda row: scrape_and_process_faraazin_with_selenium(row['Words'], row.name + 1), axis=1)
df['Processed_Content_Fastdic'] = df.apply(lambda row: scrape_and_process_fastdic(row['Words'], row.name + 1), axis=1)
df['Processed_Content_Google_Translate'] = df.apply(lambda row: scrape_and_process_google_translate(row['Words'], row.name + 1), axis=1)
# df['Processed_Content_Google_Define_Selenium_processed'] = df.apply(lambda row: scrape_and_process_google_define_with_selenium(row['Words'], row.name + 1), axis=1)

# Save the updated DataFrame to a new Excel file
current_datetime = datetime.datetime.now()
output_excel_file_path = os.path.join(script_dir, f'output_{current_datetime.strftime("%Y-%m-%d_%H-%M-%S")}_{baseName}.xlsx')
df.to_excel(output_excel_file_path, index=False)

# Save the updated DataFrame to a new CSV file
output_csv_file_path = os.path.join(script_dir, f'output_{current_datetime.strftime("%Y-%m-%d_%H-%M-%S")}_{baseName}.csv')
df.to_csv(output_csv_file_path, index=False, encoding='utf-8-sig')

print(f'Processed data (with Selenium) saved to: {output_excel_file_path}')
