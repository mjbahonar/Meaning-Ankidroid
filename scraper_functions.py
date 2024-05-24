import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from requests.exceptions import ChunkedEncodingError
import time
import os
from googletrans import Translator
from PIL import Image
from io import BytesIO

def download_images(keywords, n=5):
    # Get the current working directory
    directory = os.getcwd()
    
    # Directory to save images
    images_directory = r"C:\Users\mjbah\AppData\Roaming\Anki2\User 1\collection.media"
    
    # Create the Images directory if it doesn't exist
    local_images_directory = os.path.join(directory, 'Images')
    if not os.path.exists(local_images_directory):
        os.makedirs(local_images_directory)
    
    # Google Image URL
    url = "https://www.google.com/search?hl=en&tbm=isch&q=" + "+".join(keywords.split())+"+clipart"
    
    # Header to mimic a browser visit
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    # Send request to Google
    response = requests.get(url, headers=headers)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    image_elements = soup.find_all('img', limit=n+1)  # +1 to skip the first irrelevant image
    
    img_paths = []
    HTML_paths = []
    
    # Download and save images
    for i, img in enumerate(image_elements[1:], start=1):  # Skip the first irrelevant result
        try:
            # Get image URL
            img_url = img['src']
            img_response = requests.get(img_url)
            
            # Open and save the image locally
            img = Image.open(BytesIO(img_response.content))
            
            # Save image to the local directory
            local_img_path = os.path.join(local_images_directory, f"{keywords.replace(' ', '_')}_{i}.png")
            img.save(local_img_path)
            img_paths.append(local_img_path)
            HTML_paths.append(local_img_path)
            #print(f"Downloaded {local_img_path}")
            print(f"Image for {keywords}, created in local folder")
            
            # Save image to the specified directory
            specified_img_path = os.path.join(images_directory, f"{keywords.replace(' ', '_')}_{i}.png")
            img.save(specified_img_path)
            img_paths.append(specified_img_path)
            #print(f"Saved to specified directory: {specified_img_path}")
            print(f"Image for {keywords}, created in collection.media folder")
            
        except Exception as e:
            print(f"Could not download image {i} due to {e}")
    
    # Generate HTML
    html = "<html>\n<head>\n<style>\n"
    html += "body {text-align: center;}\n"
    html += "img {margin: 10px;}\n"
    html += "</style>\n</head>\n<body>\n"
    
    for img_path in HTML_paths:
        img_filename = os.path.basename(img_path)
        html += f'<img src="{img_filename}" alt="{keywords} image">\n<br>\n'
    
    html += "</body>\n</html>"
    
    return html

def scrape_and_process_fastdic(word, word_number):
    url = f'https://fastdic.com/word/{word}'
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        #response = requests.get(url)
        #response = requests.get(url, allow_redirects=False, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            target_section = soup.find('section', class_='results__container')

            if target_section:
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

def scrape_and_process_faraazin_with_selenium(word, word_number):
    url = f'https://www.faraazin.ir/?q={word}'
    script_directory = os.path.dirname(os.path.realpath(__file__))
    chromedriver_path = os.path.join(script_directory, 'chromedriver-win64', 'chromedriver.exe') #Must Mach your Google Chrome version correctly. Download from this url: https://googlechromelabs.github.io/chrome-for-testing/
    driver = None
    
    try:
        options = Options()
        options.headless = True
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        driver = webdriver.Chrome(executable_path=chromedriver_path)
        driver.get(url)
        time.sleep(2)
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
        if driver:
            driver.quit()

def scrape_and_process_google_translate(word, word_number):
    translator = Translator()

    try:
        translation = translator.translate(word, src='en', dest='fa')
        translated_text = translation.text
        print(f"Word {word_number}: '{word}' translated by Google Translate: '{translated_text}'")
        return translated_text
    except Exception as e:
        return f'Error in Google Translate: {e}'
    

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

            cleaned_html = soup.prettify()
            print(f"Word {word_number}: '{word}' processed content from Google (Selenium)")
            return cleaned_html
        else:
            return f'Content for word "{word}" not found with the specific class on Google.'
    except Exception as e:
        return f'Error: words not found'
    finally:
        if driver:
            driver.quit()
