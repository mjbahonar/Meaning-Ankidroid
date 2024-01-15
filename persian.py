import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import requests  # Import the requests module
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests.exceptions import ChunkedEncodingError
import time
import os
from googletrans import Translator


# Read Excel file without headers
excel_file_path = 'word.xlsx'
df = pd.read_excel(excel_file_path, header=None, names=['Words'])

# Function to scrape content and remove specified classes for the first link
def scrape_and_process_fastdic(word, word_number):
    url = f'https://fastdic.com/word/{word}'
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            target_section = soup.find('section', class_='results__container')

            if target_section:
                # Remove specified classes from the section
                classes_to_remove = ['suggestion-form-btn', 'yn']
                for class_to_remove in classes_to_remove:
                    elements_to_remove = target_section.find_all(class_=class_to_remove)
                    for element in elements_to_remove:
                        element.extract()

                content = target_section.prettify()
                print(f"Word {word_number}: '{word}' done by fastdic")
                return content
            else:
                return f'Word "{word}" not found.'
        else:
            return f'Error: {response.status_code}'
    except ChunkedEncodingError as e:
        return f'Error: {e}'

# Function to scrape content for the second link using Selenium
def scrape_and_process_faraazin_with_selenium(word, word_number):
    url = f'https://www.faraazin.ir/?q={word}'
    
    # Get the current script's directory
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Specify the path to ChromeDriver relative to the script's directory
    chromedriver_path = os.path.join(script_directory, 'chromedriver-win64', 'chromedriver.exe')
    
    # Initialize the driver outside the try block
    driver = None
    
    try:
        # Set up a headless browser using Selenium with the specified path
        options = Options()
        options.headless = True
        options.add_argument('--headless')  # Add this line
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        driver = webdriver.Chrome(executable_path=chromedriver_path)
        driver.get(url)

        # Allow time for JavaScript to execute (you may need to adjust the sleep duration)
        time.sleep(2)

        # Get the page source after JavaScript execution
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        target_div = soup.find('div', class_='translate-details')

        if target_div:
            for a_tag in target_div.find_all('a', href=True):
                a_tag.replace_with(a_tag.text)
            content = target_div.prettify()
            print(f"Word {word_number}: '{word}' done by faraazin (with Selenium)")
            return content
        else:
            return f'Details for word "{word}" not found.'
    except Exception as e:
        return f'Error: {e}'
    finally:
        # Close the browser window if it was opened
        if driver:
            driver.quit()

# Function to scrape content using Google Translate
def scrape_and_process_google_translate(word, word_number):
    translator = Translator()

    try:
        translation = translator.translate(word, src='en', dest='fa')
        translated_text = translation.text
        print(f"Word {word_number}: '{word}' translated by Google Translate: '{translated_text}'")
        return translated_text
    except Exception as e:
        return f'Error in Google Translate: {e}'


# Process each word and store results in the second and third columns
df['Processed_Content_Faraazin_Selenium'] = df.apply(lambda row: scrape_and_process_faraazin_with_selenium(row['Words'], row.name + 1), axis=1)
df['Processed_Content_Fastdic'] = df.apply(lambda row: scrape_and_process_fastdic(row['Words'], row.name + 1), axis=1)
df['Processed_Content_Google_Translate'] = df.apply(lambda row: scrape_and_process_google_translate(row['Words'], row.name + 1), axis=1)


# Save the updated DataFrame to a new Excel file
output_file_path = 'output_processed_words_with_selenium.xlsx'
df.to_excel(output_file_path, index=False)

# Save the updated DataFrame to a new CSV file
output_csv_path = 'output_processed_words_with_selenium.csv'
df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

print(f'Processed data (with Selenium) saved to: {output_file_path}')
