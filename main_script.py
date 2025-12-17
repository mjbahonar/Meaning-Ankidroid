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
    scrape_and_process_thesaurus_com,
    scrape_and_process_fastdic_audio,
    scrape_and_process_b_amooz
)

from deep_translator import GoogleTranslator

# -------------------------------------------------
# HELPER FUNCTION FOR ANKI TAGS (NEW)
# -------------------------------------------------
def create_anki_fields(row):
    """
    Constructs the Anki sound tag and the combined front field
    based on the word, assuming the file was successfully downloaded
    by scrape_and_process_fastdic_audio.
    """
    word = str(row["Words"]).strip()
    
    if not word or word.lower() == "nan":
        return "", ""
        
    # 1. Prepare word for a safe filename (replace spaces with underscores)
    safe_word = word.replace(' ', '_') 
    
    # 2. Construct the filename: fastdic_word_us.mp3
    filename = f"fastdic_{safe_word}_us.mp3"
    
    # 3. Construct the Anki sound tag: [sound:filename]
    anki_sound_tag = f"[sound:{filename}]"
    
    # 4. Create the final Anki Front Field (Sound Tag + Word)
    anki_front_field = f"{word} {anki_sound_tag}"
    
    # Return as a tuple to unpack into two new columns
    return anki_sound_tag, anki_front_field


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
#df["Processed_Content_Fastdic"] = df.apply(lambda row: scrape_and_process_fastdic(row["Words"], row.name + 1),axis=1)
df["Processed_Content_Google_Translate"] = df.apply(lambda row: scrape_and_process_google_translate(row["Words"], row.name + 1),axis=1)
#df["Downloaded_Images_HTML"] = df.apply(lambda row: download_images(row["Words"], row.name + 1, n=4),axis=1)
df["Dictionary_com"] = df.apply(lambda row: scrape_and_process_dictionary_com(row["Words"], row.name + 1),axis=1)
#df["Thesaurus_com"] = df.apply(lambda row: scrape_and_process_thesaurus_com(row["Words"], row.name + 1),axis=1)
df['Processed_Content_Faraazin_Selenium'] = df.apply(lambda row: scrape_and_process_faraazin_with_selenium(row['Words'], row.name + 1), axis=1)
#df['Processed_Content_Google_Define_Selenium_processed'] = df.apply(lambda row: scrape_and_process_google_define_with_selenium(row['Words'], row.name + 1), axis=1)
#df['scrape_and_process_cambridge_define_with_selenium'] = df.apply(lambda row: scrape_and_process_cambridge_define_with_selenium(row['Words'], row.name + 1), axis=1)
df["Fastdic_Audio"] = df.apply(lambda row: scrape_and_process_fastdic_audio(row["Words"], row.name + 1),axis=1)
df["b_amooz"] = df.apply(lambda row: scrape_and_process_b_amooz(row["Words"], row.name + 1),axis=1)

# -------------------------------------------------
# ANKI FRONT FIELD POST-PROCESSING (NEW STEP)
# -------------------------------------------------
# This creates two new columns by applying the helper function row-wise
df[["Anki_US_Sound_Tag", "Anki_Front_Field"]] = df.apply(create_anki_fields,axis=1,result_type='expand')


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