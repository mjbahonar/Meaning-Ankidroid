import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import pyperclip
import datetime
import csv
import html  # Import html for escaping

def scrape_and_process_google_define_with_selenium(word, word_number):
    url = f'https://www.google.com/search?client=firefox-b-d&q=define+{word}'
    script_directory = os.path.dirname(os.path.realpath(__file__))
    chromedriver_path = os.path.join(script_directory, 'chromedriver-win64', 'chromedriver.exe')
    driver = None

    try:
        options = Options()
        options.headless = True
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        driver.get(url)
        time.sleep(2)
        lr_container_element = driver.find_element(By.CLASS_NAME, "lr_container.yc7KLc.mBNN3d")

        if lr_container_element:
            soup = BeautifulSoup(lr_container_element.get_attribute("outerHTML"), 'html.parser')
            for script_or_style in soup(['script', 'style']):
                script_or_style.extract()

            allowed_tags = ['p', 'ol', 'li']
            for tag in soup.find_all(True):
                if tag.name not in allowed_tags:
                    tag.unwrap()

            # Change all <li> tags to <div> tags
            for li_tag in soup.find_all('li'):
                li_tag.name = 'div'

            # Find and style occurrences of "Similar" and "Opposite"
            for tag in soup.find_all(text=True):
                if 'Similar' in tag:
                    tag.replace_with(tag.replace('Similar', '<span style="color: red; font-weight: bold;">Similar</span>'))
                if 'Opposite' in tag:
                    tag.replace_with(tag.replace('Opposite', '<span style="color: blue; font-weight: bold;">Opposite</span>'))

            # Get the prettified HTML content as a string
            cleaned_html = soup.prettify(formatter=None)  # Disable automatic entity conversion
            
            # Read style.css file content
            style_css_path = os.path.join(script_directory, 'style.css')
            if os.path.exists(style_css_path):
                with open(style_css_path, 'r') as css_file:
                    css_content = css_file.read()
                
                # Inject CSS into the head of the HTML
                style_tag = soup.new_tag('style')
                style_tag.string = css_content
                soup.head.append(style_tag)
            
            # Get the updated prettified HTML content
            cleaned_html_with_style = soup.prettify(formatter=None)

            # Escape HTML content
            cleaned_html_with_style = html.escape(cleaned_html_with_style)

            print(f"Word {word_number}: '{word}' processed content from Google (Selenium)")
            # Copy the string to the clipboard
            pyperclip.copy(cleaned_html_with_style)

            # Optionally, you can verify if the copying was successful
            copied_text = pyperclip.paste()
            print(f"Copied text: {copied_text}")
            return cleaned_html_with_style
        else:
            return f'Content for word "{word}" not found with the specific class on Google.'
    except Exception as e:
        return f'Error: {str(e)}'
    finally:
        if driver:
            driver.quit()

script_dir = os.path.dirname(os.path.abspath(__file__))
baseName = 'test'
excel_file_name  = baseName + '.xlsx'
excel_file_path = os.path.join(script_dir, excel_file_name)
df = pd.read_excel(excel_file_path, header=None, names=['Words'])

# Process each word and store results in the second and third columns
df['Processed_Content_Google_Define_Selenium_processed'] = df.apply(lambda row: scrape_and_process_google_define_with_selenium(row['Words'], row.name + 1), axis=1)

# Save the updated DataFrame to a new Excel file
current_datetime = datetime.datetime.now()
output_excel_file_path = os.path.join(script_dir, f'output_{current_datetime.strftime("%Y-%m-%d_%H-%M-%S")}_{baseName}.xlsx')
df.to_excel(output_excel_file_path, index=False)

# Save the updated DataFrame to a new CSV file using custom CSV writer
output_csv_file_path = os.path.join(script_dir, f'output_{current_datetime.strftime("%Y-%m-%d_%H-%M-%S")}_{baseName}.csv')

# Custom CSV writing function
def save_to_csv(dataframe, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(dataframe.columns)  # Write headers
        for index, row in dataframe.iterrows():
            writer.writerow(row)

save_to_csv(df, output_csv_file_path)

print(f'Processed data (with Selenium) saved to: {output_excel_file_path}')
