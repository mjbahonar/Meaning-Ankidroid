import pandas as pd
import os
import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from scraper_functions import (
    scrape_and_process_fastdic,
    scrape_and_process_faraazin_with_selenium,
    scrape_and_process_google_translate,
    download_images,
    scrape_and_process_google_define_with_selenium,
    scrape_and_process_cambridge_define_with_selenium,
    scrape_and_process_dictionary_com,
    scrape_and_process_thesaurus_com,
    scrape_and_process_fastdic_audio
)

# =================================================
# CONFIGURATION
# =================================================
AUTOSAVE_EVERY = 5          # 💾 autosave every N words
ENABLE_PARALLEL = True     # ⚡ turn parallel ON/OFF
MAX_WORKERS = 3            # threads for non-selenium tasks

# =================================================
# PATHS
# =================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "Output")
os.makedirs(output_dir, exist_ok=True)

# =================================================
# INPUT FILE
# =================================================
baseName = "words-test"
excel_file_path = os.path.join(script_dir, baseName + ".xlsx")
df = pd.read_excel(excel_file_path, header=None, names=["Words"])

# =================================================
# OUTPUT COLUMNS
# =================================================
COLUMNS = [
    "Processed_Content_Fastdic",
    "Processed_Content_Google_Translate",
    "Downloaded_Images_HTML",
    "Dictionary_com",
    "Thesaurus_com",
    "Processed_Content_Faraazin_Selenium",
    "Processed_Content_Google_Define_Selenium_processed",
    "Processed_Content_Cambridge_Define_Selenium",
    "Fastdic_Audio"

]

for col in COLUMNS:
    df[col] = ""

# =================================================
# AUTOSAVE FUNCTION
# =================================================
def autosave(df, suffix="autosave"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(output_dir, f"{suffix}_{timestamp}_{baseName}.xlsx")
    df.to_excel(path, index=False)
    print(f"\n💾 Autosaved: {path}")

# =================================================
# NON-SELENIUM TASK MAP
# =================================================
def run_non_selenium_tasks(word, word_number):
    return {
        #"Processed_Content_Fastdic": scrape_and_process_fastdic(word, word_number),
        "Processed_Content_Google_Translate": scrape_and_process_google_translate(word, word_number),
        "Downloaded_Images_HTML": download_images(word, word_number, n=4),
        "Dictionary_com": scrape_and_process_dictionary_com(word, word_number),
        #"Thesaurus_com": scrape_and_process_thesaurus_com(word, word_number),
        "Processed_Content_Fastdic_Audio": scrape_and_process_fastdic_audio(word, word_number)
    }

# =================================================
# MAIN LOOP (WORD BY WORD)
# =================================================
processed_count = 0

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing words"):
    word = str(row["Words"]).strip()
    word_number = idx + 1

    if not word or word.lower() == "nan":
        continue

    print(f"\n▶ WORD {word_number}: {word}")

    # -------------------------------
    # NON-SELENIUM (PARALLEL OPTIONAL)
    # -------------------------------
    if ENABLE_PARALLEL:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future = executor.submit(run_non_selenium_tasks, word, word_number)
            results = future.result()
    else:
        results = run_non_selenium_tasks(word, word_number)

    for col, value in results.items():
        df.at[idx, col] = value

    # -------------------------------
    # SELENIUM (SEQUENTIAL ONLY)
    # -------------------------------
    df.at[idx, "Processed_Content_Faraazin_Selenium"] = (scrape_and_process_faraazin_with_selenium(word, word_number))
    #df.at[idx, "Processed_Content_Google_Define_Selenium_processed"] = (scrape_and_process_google_define_with_selenium(word, word_number))
    #df.at[idx, "Processed_Content_Cambridge_Define_Selenium"] = (scrape_and_process_cambridge_define_with_selenium(word, word_number))

    processed_count += 1

    # -------------------------------
    # AUTOSAVE CHECK
    # -------------------------------
    if processed_count % AUTOSAVE_EVERY == 0:
        autosave(df)

# =================================================
# FINAL SAVE
# =================================================
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

final_excel = os.path.join(
    output_dir,
    f"output_{timestamp}_{baseName}.xlsx"
)

final_csv = os.path.join(
    output_dir,
    f"output_{timestamp}_{baseName}.csv"
)

df.to_excel(final_excel, index=False)
df.to_csv(final_csv, index=False, encoding="utf-8-sig")

print("\n" + "=" * 60)
print("✅ PROCESS COMPLETED SUCCESSFULLY")
print(f"Excel saved to: {final_excel}")
print(f"CSV saved to  : {final_csv}")
print("=" * 60)
