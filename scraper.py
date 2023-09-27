import os
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to convert basic HTML to Markdown
def html_to_markdown(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    for h1 in soup.find_all('h1'):
        h1.string = f"# {h1.text}"
        
    for h2 in soup.find_all('h2'):
        h2.string = f"## {h2.text}"
        
    for b in soup.find_all('b'):
        b.string = f"**{b.text}**"
        
    for i in soup.find_all('i'):
        i.string = f"*{i.text}*"
         
    for a in soup.find_all('a'):
        a.string = f"[{a.text}]({a.get('href')})"
        
    return soup.get_text()

# Function to save content to a Markdown file
def save_to_markdown(filename, content):
    filename = filename.replace('/', '-').replace(' ', '_')
    filepath = os.path.join(output_dir, f"{filename}.md")
    
    markdown_content = html_to_markdown(content)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Successfully saved {filepath}")
    except Exception as e:
        print(f"Failed to save {filepath}. Error: {e}")

# ... (rest of your existing code remains the same)

# Function to get user input and validate it
def get_user_input(prompt, validation_func=None, optional=False):
    while True:
        user_input = input(prompt)
        if optional and user_input == "":
            return None
        if validation_func:
            if validation_func(user_input):
                return user_input
            else:
                print("Invalid input. Please try again.")
        else:
            return user_input


# Validation functions
def validate_url(url):
    return url.startswith("http")

def validate_selector(selector):
    return len(selector) > 0

# Get user input
base_url = get_user_input("Enter the base URL to start scraping from: ", validate_url)
main_content_selector = get_user_input("Enter the CSS selector for the main content: ", validate_selector)
# Get user input
links_selector = get_user_input("Enter the CSS selector for the links to follow (optional): ", validate_selector, optional=True)


# Create a directory to store the documentation files
output_dir = 'Scraped_Docs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# File to store visited URLs
visited_file = 'visited_urls.json'
try:
    with open(visited_file, 'r') as f:
        visited = set(json.load(f))
except FileNotFoundError:
    visited = set()

# Function to scrape a page and follow links
def scrape_page(url, visited, retries=3):
    if url in visited or retries <= 0:
        return
    visited.add(url)
    
    print(f"Scraping {url}...")
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}. Retrying...")
        time.sleep(5)
        scrape_page(url, visited, retries-1)
        return
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.select_one(main_content_selector)
        
        if main_content:
            title = soup.select_one('title').get_text().split('—')[0].strip()
            save_to_markdown(title, main_content.get_text())
            
            if links_selector:
                for a in main_content.select(links_selector):
                    link = a.get('href')
                    if link:
                        link = urljoin(url, link)
                        scrape_page(link, visited)
                    
            time.sleep(3)
        else:
            print(f"Could not find main content for {url}.")
    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")

    # Save visited URLs to file
    with open(visited_file, 'w') as f:
        json.dump(list(visited), f)

# Start scraping from the base URL
scrape_page(base_url, visited)

print("Scraping completed.")
