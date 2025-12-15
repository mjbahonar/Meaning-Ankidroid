import pandas as pd
import csv
import os
import datetime

from scraper_functions import (
    scrape_and_process_fastdic,
    scrape_and_process_faraazin_with_selenium,
    scrape_and_process_google_translate,
    download_images,
    scrape_and_process_google_define_with_selenium,
    scrape_and_process_cambridge_define_with_selenium,
    scrape_and_process_dictionary_com,
    scrape_and_process_thesaurus_com
)

from deep_translator import GoogleTranslator

# -------------------------------------------------
# PATHS
# -------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))

# Output directory
output_dir = os.path.join(script_dir, "Output")
os.makedirs(output_dir, exist_ok=True)

# -------------------------------------------------
# INPUT FILE
# -------------------------------------------------
baseName = "words-test"
excel_file_name = baseName + ".xlsx"
excel_file_path = os.path.join(script_dir, excel_file_name)

# Read Excel file without headers
df = pd.read_excel(excel_file_path, header=None, names=["Words"])

# -------------------------------------------------
# PROCESS WORDS
# -------------------------------------------------
df["Processed_Content_Fastdic"] = df.apply(lambda row: scrape_and_process_fastdic(row["Words"], row.name + 1),axis=1)
df["Processed_Content_Google_Translate"] = df.apply(lambda row: scrape_and_process_google_translate(row["Words"], row.name + 1),axis=1)
df["Downloaded_Images_HTML"] = df.apply(lambda row: download_images(row["Words"], row.name + 1, n=4),axis=1)
df["Dictionary_com"] = df.apply(lambda row: scrape_and_process_dictionary_com(row["Words"], row.name + 1),axis=1)
df["Thesaurus_com"] = df.apply(lambda row: scrape_and_process_thesaurus_com(row["Words"], row.name + 1),axis=1)
#df['Processed_Content_Faraazin_Selenium'] = df.apply(lambda row: scrape_and_process_faraazin_with_selenium(row['Words'], row.name + 1), axis=1)
#df['Processed_Content_Google_Define_Selenium_processed'] = df.apply(lambda row: scrape_and_process_google_define_with_selenium(row['Words'], row.name + 1), axis=1)
#df['scrape_and_process_cambridge_define_with_selenium'] = df.apply(lambda row: scrape_and_process_cambridge_define_with_selenium(row['Words'], row.name + 1), axis=1)

# -------------------------------------------------
# SAVE OUTPUT FILES INTO Output/
# -------------------------------------------------
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

output_excel_file_path = os.path.join(
    output_dir,
    f"output_{current_datetime}_{baseName}.xlsx"
)

output_csv_file_path = os.path.join(
    output_dir,
    f"output_{current_datetime}_{baseName}.csv"
)

df.to_excel(output_excel_file_path, index=False)
df.to_csv(output_csv_file_path, index=False, encoding="utf-8-sig")

print("===================================")
print("PROCESS COMPLETED SUCCESSFULLY")
print(f"Excel saved to: {output_excel_file_path}")
print(f"CSV saved to  : {output_csv_file_path}")
print("===================================")
