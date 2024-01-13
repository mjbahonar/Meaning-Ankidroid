# Persian Meaning for Ankidroid

This GitHub repository, "Persian Meaning for Ankidroid," contains a Python script designed to retrieve Persian meanings for a list of words from two sources: Fastdic and Faraazin. The words should be provided in an Excel file with no headers in the first column.

## Code Overview

The Python script processes the words from the input Excel file and queries two sources, Fastdic and Faraazin, to obtain their Persian meanings. The extracted data is then stored in an output Excel file. The resulting information, formatted in HTML, can be seamlessly integrated into Ankidroid decks or other compatible platforms.

## Instructions

1. **Input Data**: Prepare an Excel file with the words in the first column and no headers.

2. **Prerequisites**: Install the required dependencies by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

3. **Faraazin Source**: To fetch meanings from Faraazin, ensure Chromedriver is installed. For Chrome version 120, place the `chromedriver-win64` executable in the same folder as the code. Adjust the Chromedriver version as needed for your Chrome browser.

4. **Running the Code**: Execute the script to fetch meanings from both Fastdic and Faraazin. The results will be stored in an Excel file in HTML format, suitable for integration into Ankidroid decks.

5. **Output Files**:

   - **Excel File**: Persian meanings will be saved in an Excel file with HTML-formatted content.
   - **CSV File**: A CSV file with the same information will also be generated.

6. **Important Note for Faraazin**: Ensure `chromedriver-win64` is in the code's folder. Adjust the version as needed for your Chrome browser.

Feel free to contribute, report issues, or suggest improvements!
