# Web Scraping to Markdown Script

## Overview

This Python script allows you to scrape web pages and save the content as Markdown files. It's designed to be user-friendly, prompting you for the necessary inputs like the URL to scrape and the CSS selectors for the main content and links.

## Features

- **Scrape Web Pages**: Based on user-provided URL and CSS selectors.
- **Save as Markdown**: Saves scraped content in Markdown format.
- **Follow Links**: Follows links within the main content to scrape additional pages.
- **Resume Feature**: Ability to resume scraping from where it left off.
- **Delayed Timing**: Includes a delay between requests to avoid overloading the server.
- **HTML to Markdown**: Converts basic HTML elements to Markdown format.

## Requirements

- Python 3.x
- BeautifulSoup
- Requests

## Installation

1. Clone this repository or download the ZIP file.
2. Navigate to the project directory and install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Script

1. Navigate to the project directory in your terminal.
2. Run the script:
    ```bash
    python your_script.py
    ```
3. Follow the prompts to enter the URL and CSS selectors.

### Creating an Executable

1. Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2. Create the executable:
    ```bash
    pyinstaller --onefile your_script.py
    ```
3. The executable will be in the `dist` folder. Double-click to run it.

## Delayed Timing

The script includes a delay between each request to avoid overloading the server. This is particularly useful when the script is set to follow multiple links on a webpage.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you'd like to change.

## License

This project is licensed under the Apache License 2.0.