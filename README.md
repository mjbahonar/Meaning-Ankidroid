

# 🚀 Anki Word-Wizard: Automated Card Data Generator

[![GitHub Stars](https://img.shields.io/github/stars/mjbahonar/Meaning-Ankidroid?style=social)](https://github.com/mjbahonar/Meaning-Ankidroid/stargazers) [![GitHub Forks](https://img.shields.io/github/forks/mjbahonar/Meaning-Ankidroid?style=social)](https://github.com/mjbahonar/Meaning-Ankidroid/fork) [![License](https://img.shields.io/github/license/mjbahonar/Meaning-Ankidroid)](./LICENSE) [![Repo Size](https://img.shields.io/github/repo-size/mjbahonar/Meaning-Ankidroid)](https://github.com/mjbahonar/Meaning-Ankidroid) [![Last Commit](https://img.shields.io/github/last-commit/mjbahonar/Meaning-Ankidroid)](https://github.com/mjbahonar/Meaning-Ankidroid/commits) [![Contributors](https://img.shields.io/github/contributors/mjbahonar/Meaning-Ankidroid)](https://github.com/mjbahonar/Meaning-Ankidroid/graphs/contributors)

Anki Word-Wizard is a powerful Python-based tool designed to supercharge the flashcard creation process for language learners and dedicated **Anki** users. It takes a simple list of words and automatically enriches it with high-quality data scraped from multiple online sources, saving you countless hours of manual work.

The script generates detailed definitions, translations, usage examples, and relevant images, then compiles everything into clean, Anki-ready `.csv` and `.xlsx` files.

### 🤔 What is Anki/AnkiDroid?

For those new to it, [Anki](https://apps.ankiweb.net/) (and its Android version, [AnkiDroid](https://play.google.com/store/apps/details?id=com.ichi2.anki&hl=en&gl=US)) is a powerful, intelligent flashcard program that uses a **Spaced Repetition System (SRS)**. This learning technique schedules card reviews at increasingly long intervals, making it incredibly efficient for long-term memorization of vocabulary, concepts, and more. This script helps you create the rich, detailed cards needed for effective learning.

### Code Structure

The project is organized into two main files:

*   📜 `main_script.py`: This is the master script and your main point of interaction. It reads your word list from an Excel file, calls the various scraper functions for each word, and saves the final compiled data into output files.
*   🦾 `scraper_functions.py`: This file is a library of specialized "worker" functions. Each function is designed to perform a specific task, such as scraping a particular website (like Fastdic or Cambridge) or downloading images from Google. This modular design makes it easy to maintain and customize.

## ✨ Features

*   **📚 Multi-Source Scraping**: Gathers data from a variety of reliable sources:
    *   **Fastdic** (English-Persian Dictionary)
    *   **Faraazin** (English-Persian Dictionary)
    *   **Google Translate** (For quick translations into any language)
    *   **Google Dictionary** (For in-depth English definitions, synonyms, and antonyms)
    *   **Cambridge Dictionary** (For detailed definitions and example sentences)
    *   **Dictionary.com** (Audio and meanings)
*   **🖼️ Automatic Image Downloader**: Fetches and downloads relevant clipart images for each word to create visually engaging flashcards.
*   **⚙️ Powerful Batch Processing**: Processes an entire vocabulary list from an Excel file in one go.
*   **✔️ Anki-Ready Output**: Generates clean, styled HTML content in the output files, perfect for direct import and mapping to your Anki card fields.
*   **🔧 Highly Customizable**: Easily choose which scrapers to run, change the translation language, or adjust the number of images to download.
*   **🤖 Robust and Automated**: Uses Selenium to interact with modern, JavaScript-heavy websites, ensuring reliable data extraction where simpler methods fail.

## 📦 Prerequisites

Before you begin, ensure you have the following set up:

1.  **🐍 Python 3.x**: Download it from the [official Python website](https://www.python.org/downloads/).
2.  **🌐 Google Chrome**: This script uses Selenium to control Chrome, so you must have the browser installed.
3.  **🔑 ChromeDriver**: You need the specific driver that **matches your Google Chrome version**.
    *   **Find Your Chrome Version**: In Chrome, go to `Settings` > `About Chrome` to see your version (e.g., `126.0.6478.127`).
    *   **Download ChromeDriver**: Go to the [Chrome for Testing availability dashboard](https://googlechromelabs.github.io/chrome-for-testing/) and download the `chromedriver` zip file for your version.
    *   **Place the Driver**: Unzip the file and place the `chromedriver.exe` executable inside the `chromedriver-win64` folder included in this project.

## 💻 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/mjbahonar/Meaning-Ankidroid.git
    cd your-repo-name
    ```

2.  **Install Required Libraries**
    Using a virtual environment is highly recommended.
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install all project dependencies
    pip install pandas openpyxl selenium beautifulsoup4 requests googletrans Pillow python-dotenv pyperclip
    ```

3.  **Set Up Environment Variables (Optional)**
    This step allows the script to save a copy of all downloaded images directly into your Anki media folder, making them instantly available in your collection.
    *   **Important Note:** To use this feature, you must have the [Anki desktop application for Windows](https://apps.ankiweb.net/) installed and have logged into your profile at least once. This is necessary because the script needs to save images to the `collection.media` folder, which is only created after you set up a profile in the Anki app.
    *   Create a file named `.env` in the project's root directory.
    *   Add the following line, replacing the path with the correct path for your system:
        ```
        # Example for Windows. "YourProfile" is the name of your Anki profile.
        ADDRESS="C:/Users/YourUser/AppData/Roaming/Anki2/YourProfile/collection.media"
        ```
        To find out the address of the where the media are collected, go to your Anki app on windows, `Tools`>`Check Media...`> at the bottom of the windows click on `view files`. Now the folder is open and you can copy the address from file explorer.

## ▶️ Usage

1.  **✍️ Prepare Your Word List**
    *   Create an Excel file (e.g., `3A-part3.xlsx`) in the root project directory.
    *   Put your vocabulary words in the first column (`A`). **Do not use a header row**.

2.  **⚙️ Configure the Main Script**
    *   Open `main_script.py`.
    *   Update the `baseName` variable to match your Excel file's name (without the `.xlsx` extension).
        ```python
        # If your file is named "My-Vocab-List.xlsx"
        baseName = 'My-Vocab-List'
        ```

3.  **🚀 Run the Script**
    Open your terminal in the project directory and execute:
    ```bash
    python main_script.py
    ```    The script will begin processing, and you'll see progress updates printed in your terminal.

4.  **🎉 Get Your Output**
    *   When the script is done, you will find two new timestamped files:
        *   `output_YYYY-MM-DD_HH-MM-SS_baseName.xlsx`
        *   `output_YYYY-MM-DD_HH-MM-SS_baseName.csv`
    *   These files contain your original words plus all the rich content scraped from the web.

## 🎨 Customization

You can easily tweak the script to fit your exact needs.

### How to Change the Google Translate Language

By default, words are translated to Persian (`fa`). You can change this to any other language.

1.  Open the `scraper_functions.py` file.
2.  Find the `scrape_and_process_google_translate` function.
3.  Change the `dest='fa'` parameter to your desired language code.
    ```python
    # Find this line:
    translation = translator.translate(word, src='en', dest='fa')

    # Change it for Spanish:
    translation = translator.translate(word, src='en', dest='es')

    # Or for French:
    translation = translator.translate(word, src='en', dest='fr')
    ```
    You can find a list of language codes [here](https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages).

### How to Change the Number of Downloaded Images

By default, the script downloads **4** images per word.

1.  Open the `main_script.py` file.
2.  Find the line where `download_images` is called.
3.  Change the value of the `n` parameter.
    ```python
    # To download 6 images instead of 4:
    df['Downloaded_Images_HTML'] = df.apply(lambda row: download_images(row['Words'], row.name + 1, n=6), axis=1)
    ```

## 📲 Importing to Anki & What Your Card Will Look Like

The generated `.csv` file is formatted for easy import into Anki.

1.  **In Anki**, go to `File` > `Import...` and select your `output_... .csv` file.
2.  The import dialog will appear. Make sure you:
    *   Select the correct **Note Type** (e.g., "Basic").
    *   Select the correct **Deck**.
    *   **Map the fields**: Map each column from the CSV to the corresponding field in your Anki note type. For example:
        *   Column 1 (`Words`) -> `Front` field
        *   Column 2 (`Processed_Content_Faraazin...`) -> `Faraazin Definition` field
        *   Column 5 (`Downloaded_Images_HTML`) -> `Images` field
    *   Ensure the "Allow HTML in fields" option is **checked**.

## V3.0 Release Notes

### ✨ Major Features and Improvements

#### 🚀 **New Word-by-Word Processing Logic**

The core processing logic has been fundamentally redesigned to operate on a word-by-word basis, significantly improving efficiency and reliability for long jobs.

* **Function Change:** The main execution script is now initiated via `main_script(word_by_word)`.
* **Output Structure:** The final output is now constructed **row-by-row** (one complete record at a time) instead of the previous column-by-column method.

#### 💾 **Robust Auto-Save and Parallel Execution**

To support the new processing logic and prevent data loss, auto-saving and parallel processing capabilities have been integrated.

* **Autosave:** Data is now saved incrementally after processing a specified number of words.
* **Parallelism:** The script can now leverage multi-threading to speed up non-Selenium tasks.

**Configuration Changes in `main_script(word_by_word).py` (or equivalent file):**

You must update the following settings to configure the new features:

| Setting | Default Value | Description |
| :--- | :--- | :--- |
| `AUTOSAVE_EVERY` | `5` | 💾 Autosave the progress and output file every N words processed. |
| `ENABLE_PARALLEL` | `True` | ⚡ Turn parallel processing ON (`True`) or OFF (`False`). |
| `MAX_WORKERS` | `3` | Defines the maximum number of worker threads for parallel, non-Selenium tasks. |

#### 🗣️ **Enhanced Audio Support**

Audio fetching has been updated and expanded:

* **New Source:** Added audio support from **FastDic** for two distinct accents: **US** and **UK**.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

Don't forget to give the project a star! Thanks again!

## ⚠️ Disclaimer

This tool automates the process of accessing publicly available information. It is intended for **personal and educational use only**. Please be respectful of the websites you are scraping and do not overload their servers. The developer is not responsible for any misuse of this tool.
