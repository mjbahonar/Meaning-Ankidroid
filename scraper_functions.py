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
from dotenv import load_dotenv
import pyperclip
import re
from deep_translator import GoogleTranslator



# =========================
# SAFE NETWORK LAYER
# =========================

import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def safe_get(url, timeout=15):
    time.sleep(3 + random.uniform(0, 3))
    return session.get(url, headers=HEADERS, timeout=timeout)


# =========================
# Image Downloader
# =========================

def download_images(keywords, word_number, n=5):
    try:
        keywords = re.sub(r'[\\/*?:"<>|]', '_', str(keywords))

        # Get the current working directory
        directory = os.getcwd()
        
        # Directory to save images
        load_dotenv()
        images_directory = os.getenv('ADDRESS')
        
        # Create the Images directory if it doesn't exist
        local_images_directory = os.path.join(directory, 'Images')
        if not os.path.exists(local_images_directory):
            os.makedirs(local_images_directory)
        
        # Google Image URL
        url = "https://www.google.com/search?hl=en&tbm=isch&q=" + "+".join(keywords.split())+"+clipart"
        
        # Header to mimic a browser visit
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        # Send request to Google
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # This checks for HTTP errors
            # Process response data here
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return "Error from recieving from net. I hate you GOOGLE!!!"
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        image_elements = soup.find_all('img', limit=n+1)  # +1 to skip the first irrelevant image
        
        img_paths = []
        HTML_paths = []
        
        # Download and save images
        print(f"Word {word_number} : is processing by google image function")
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
    except ChunkedEncodingError as e:
        return f'Error: {e}'
    

# =========================
# Fastdic Scraper
# =========================

def scrape_and_process_fastdic(word, word_number):
    print(f"[FASTDICT] ({word_number}) {word}")

    url = f"https://fastdic.com/word/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return f"Fastdic HTTP {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        # Main result container
        target_section = soup.find("section", class_="results__container")
        if not target_section:
            return f'Fastdic: result section not found for "{word}"'

        # --------------------------------
        # REMOVE UNWANTED IDS
        # --------------------------------
        for unwanted_id in ("faqs", "cite"):
            tag = target_section.find(id=unwanted_id)
            if tag:
                tag.decompose()

        # --------------------------------
        # REMOVE UNWANTED CLASSES
        # --------------------------------
        selectors_to_remove = [
            ".fd-sidebar.js-sidebar",
            ".relevant",
            ".tab-wrapper.tab-big",
        ]

        for selector in selectors_to_remove:
            for el in target_section.select(selector):
                el.decompose()

        # Remove junk UI classes
        for cls in ("suggestion-form-btn", "yn", "js-sidebar"):
            for el in target_section.find_all(class_=cls):
                el.decompose()

        # Remove scripts & styles
        for tag in target_section.find_all(["script", "style"]):
            tag.decompose()

        # --------------------------------
        # FINAL HTML (ANKI SAFE)
        # --------------------------------
        content = target_section.prettify()

        html = f"""
        <div>
            {content}
        </div>
        """

        print(f"[FASTDICT] DONE: {word}")
        return html.replace('"', "'")

    except Exception as e:
        print(f"[FASTDICT] ERROR: {e}")
        return f"Fastdic error: {e}"

    
# =========================
# Faraazin Scraper with Selenium
# =========================    

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
            content = content.replace('"', "'")
            print(f"Word {word_number}: '{word}' done by faraazin (with Selenium)")
            return content
        else:
            return f'Details for word "{word}" not found.'
    except Exception as e:
        return f'Error: {e}'
    finally:
        if driver:
            driver.quit()

# =========================
# Google Translate Scraper
# =========================

def scrape_and_process_google_translate(word, word_number):
    time.sleep(4 + random.uniform(0, 4))
    try:
        translated_text = GoogleTranslator(source='en', target='fa').translate(word)
        print(f"Word {word_number}: '{word}' translated by Google Translate")
        return translated_text
    except Exception as e:
        print(f"Google Translate FAILED for '{word}': {e}")
        return ""

    
# =========================
# Google Define with Selenium Scraper
# =========================

def scrape_and_process_google_define_with_selenium(word, word_number):
    url = f'https://www.google.com/search?client=firefox-b-d&q=dictionary+{word}'
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
            soup = BeautifulSoup(lr_container_element.get_attribute("outerHTML"), 'html.parser', from_encoding='utf-8')
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
            #for tag in soup.find_all(text=True):
            #    if 'Similar' in tag:
            #        tag.replace_with(tag.replace('Similar', '<span style="color: green; font-weight: bold;">Similar</span>'))
            #    if 'Opposite' in tag:
            #        tag.replace_with(tag.replace('Opposite', '<span style="color: blue; font-weight: bold;">Opposite</span>'))

            # Get the prettified HTML content as a string
            #cleaned_html_with_style = soup.prettify(formatter=None)  # Disable automatic entity conversion
            
            # Read style.css file content
            style_css_path = os.path.join(script_directory, 'style.css')
            if os.path.exists(style_css_path):
                with open(style_css_path, 'r' , encoding='utf-8') as css_file:
                    css_content = css_file.read()
               
                # Create a <style> tag and insert the CSS content
                style_tag = soup.new_tag('style')
                style_tag.string = css_content
                
                # Insert the <style> tag at the beginning of the body content
                soup.insert(0, style_tag)

            
            # Get the updated prettified HTML content
            cleaned_html_with_style = soup.prettify(formatter=None)


            html_content = str(soup)
            cleaned_html_with_style = html_content.replace('"', "'")


            print(f"Word {word_number}: '{word}' processed content from Google (Selenium)")
            # Copy the string to the clipboard
            string_to_copy=cleaned_html_with_style
            pyperclip.copy(string_to_copy)

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

# =========================
# Cambridge Define with Selenium Scraper
# =========================

def scrape_and_process_cambridge_define_with_selenium(word, word_number):
    url = f'https://www.google.com/search?client=firefox-b-d&q=cambridge+dictionary+{word}'
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
        lr_container_element = driver.find_element(By.CLASS_NAME, "hgKElc")

        if lr_container_element:
            soup = BeautifulSoup(lr_container_element.get_attribute("outerHTML"), 'html.parser', from_encoding='utf-8')
            for script_or_style in soup(['script', 'style']):
                script_or_style.extract()

        
            # Get the updated prettified HTML content
            cleaned_html_with_style = soup.prettify(formatter=None)


            html_content = str(soup)
            cleaned_html_with_style = html_content.replace('"', "'")


            print(f"Word {word_number}: '{word}' processed content from CAMBRIDGE (Selenium)")
            # Copy the string to the clipboard
            string_to_copy=cleaned_html_with_style
            pyperclip.copy(string_to_copy)

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

# =========================
# Dictionary.com Scraper
# =========================

def scrape_and_process_dictionary_com(word, word_number):
    print(f"[DICT] ({word_number}) {word}")

    try:
        url = f"https://www.dictionary.com/browse/{word}"
        r = safe_get(url)

        print(f"[DICT] HTTP {r.status_code}")
        if r.status_code != 200:
            return f"Dictionary HTTP {r.status_code}"

        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.find("h1", class_="hdr-headword-dcom-1")
        phon = soup.find("span", class_="txt-phonetic")
        ipa = soup.find("span", class_="txt-ipa")

        audio_html = ""
        audio_box = soup.find("div", class_="box-audio-pronunciation")

        if audio_box:
            button = audio_box.find("button", class_="common-btn-headword-audio")
            if button:
                origin = button.get("data-audioorigin")
                src = button.get("data-audiosrc")
                if origin and src:
                    audio_url = f"{origin}/{src}"
                    audio_html = download_dictionary_audio(word, audio_url)
                else:
                    print("[DICT] Audio attributes missing")
            else:
                print("[DICT] Audio button not found")
        else:
            print("[DICT] Audio box not found")

        def sec(id_):
            s = soup.find(id=id_)
            print(f"[DICT] {id_}:", "FOUND" if s else "NOT FOUND")
            return s.prettify() if s else ""

        html = f"""
        <div class="dictionary-com">
            <h1>{title.text if title else word}</h1>
            <div>{phon.text if phon else ''} {ipa.text if ipa else ''}</div>
            {audio_html}
            {sec('id-sec-entry-group-dcom')}
            {sec('id-sec-entry-group-british')}
            {sec('id-sec-example-sentences')}
            {sec('id-sec-related-words')}
            {sec('id-sec-other-word-forms')}
            {sec('id-sec-entry-group-idiom')}
        </div>
        """

        print(f"[DICT] DONE: {word}")
        return html.replace('"', "'")

    except Exception as e:
        print(f"[DICT] EXCEPTION: {e}")
        return f"Dictionary error: {e}"

# =========================
# dictionary.com Audio Downloader
# =========================

def download_dictionary_audio(word, audio_url):
    print(f"[AUDIO] Downloading audio for '{word}'")

    load_dotenv()
    media_dir = os.getenv("ADDRESS")

    local_audio_dir = os.path.join(os.getcwd(), "Audio")
    os.makedirs(local_audio_dir, exist_ok=True)

    if not media_dir:
        print("[AUDIO] ERROR: ADDRESS not set")
        return ""

    filename = f"{word}_pronunciation.mp3"
    local_path = os.path.join(local_audio_dir, filename)
    media_path = os.path.join(media_dir, filename)

    try:
        r = safe_get(audio_url)
        print(f"[AUDIO] HTTP {r.status_code}")

        if r.status_code != 200:
            print("[AUDIO] Download failed")
            return ""

        with open(local_path, "wb") as f:
            f.write(r.content)

        with open(media_path, "wb") as f:
            f.write(r.content)

        print("[AUDIO] Saved locally and to ADDRESS")

        return f"""
        <audio controls>
            <source src="{filename}" type="audio/mpeg">
        </audio>
        """

    except Exception as e:
        print(f"[AUDIO] EXCEPTION: {e}")
        return ""

# =========================
# thesaurus.com Scraper
# =========================

def scrape_and_process_thesaurus_com(word, word_number):
    print(f"[THES] ({word_number}) {word}")

    url = f"https://www.thesaurus.com/browse/{word}"
    r = safe_get(url)

    if r.status_code != 200:
        return f"Thesaurus HTTP {r.status_code}"

    soup = BeautifulSoup(r.text, "html.parser")

    panels = soup.select("section.synonym-antonym-panel")

    if not panels:
        return "Thesaurus: no synonym/antonym panels found"

    data = {"synonyms": {}, "antonyms": {}}

    for panel in panels:
        label_div = panel.find("div", class_="synonym-antonym-panel-label")
        if not label_div:
            continue

        label = label_div.get_text(strip=True).lower()
        target = "synonyms" if "synonym" in label else "antonyms"

        level_labels = panel.select("div.similarity-level-label")
        word_lists = panel.select("div.similarity-level-word-list")

        for lvl, words_div in zip(level_labels, word_lists):
            level_name = lvl.get_text(strip=True)

            words = [
                a.get_text(strip=True)
                for a in words_div.select("a.word-chip.synonym-antonym-word-chip")
            ]

            if words:
                data[target][level_name] = words

    # -------- HTML output --------
    html = "<div class='thesaurus'>"

    for kind in ("synonyms", "antonyms"):
        if data[kind]:
            html += f"<h3>{kind.capitalize()}</h3>"
            for level, words in data[kind].items():
                html += f"<b>{level}</b>: " + ", ".join(words) + "<br>"

    html += "</div>"

    print(
        f"[THES] Synonyms: {sum(len(v) for v in data['synonyms'].values())}, "
        f"Antonyms: {sum(len(v) for v in data['antonyms'].values())}"
    )

    return html.replace('"', "'")
