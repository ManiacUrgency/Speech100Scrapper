'''
import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
URL = "https://www.americanrhetoric.com/speeches/mlkihaveadream.htm"
# Send a GET request to the URL
page = requests.get(URL)

# Parse the HTML content of the page
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

title = None
author_date = None
speech_text = None

# Extracting the title based on the provided HTML structure
title_section = soup.find('font', color="#041E42")
if title_section:
    title_tag = title_section.find('i')
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        print("Italic tag for title not found.")
else:
    print("Font tag with specified color for title not found.")
    title = "No Title Found"

# Extracting the author and date based on the provided HTML structure
author_date_section = soup.find('font', size="1", color="#8F8D8F")
if author_date_section:
    author_date = author_date_section.get_text(strip=True)
else:
    print("Author/date section not found.")
    author_date = "No Author/Date Found"

# Extracting the speech text based on the provided HTML structure
speech_text_list = []
for p_tag in soup.find_all('p', align="left"):
    for font_tag in p_tag.find_all('font', face="Verdana"):
        speech_text_list.append(font_tag.get_text(strip=True))
speech_text = ' '.join(speech_text_list).replace('"', "'")

# Construct the new speech data structure only if all components were found
if title and author_date and speech_text:
    new_speech = {
        "type": "speech",
        "title": title,
        "citation": author_date,
        "text": speech_text,
        "source": URL
    }

    # Specify the file path (Make sure to use the correct file path where the file is located)
    file_path = 'AP_exam_MCQ_speech_documents.json'

    # Load the existing data or create a new structure if the file doesn't exist
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'speeches': []}

    # Append the new speech to the "speeches" list within the data dictionary
    data['speeches'].append(new_speech)

    # Save the updated data back to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    # Output the file path for confirmation
    print(f"Updated JSON saved to {file_path}")
else:
    print("Webscraping did not find all required elements, no new speech added.")
'''

import requests
from bs4 import BeautifulSoup
import json

# The URL you want to scrape
URL = "https://www.americanrhetoric.com/speeches/mlkihaveadream.htm"

# The user-agent string of a web browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}

# Make the GET request with the user-agent header
response = requests.get(URL, headers=headers)

# Continue with your code if the request was successful
if response.ok:
    # Parse the content with BeautifulSoup or your preferred parser
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())

    title = None
    author_date = None
    speech_text = None

    # Extracting the title based on the provided HTML structure
    title_section = soup.find('font', color="#041E42")
    if title_section:
        title_tag = title_section.find('i')
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            print("Italic tag for title not found.")
    else:
        print("Font tag with specified color for title not found.")
        title = "No Title Found"

    # Extracting the author and date based on the provided HTML structure
    author_date_section = soup.find('font', size="1", color="#8F8D8F")
    if author_date_section:
        author_date = author_date_section.get_text(strip=True)
    else:
        print("Author/date section not found.")
        author_date = "No Author/Date Found"

    # Extracting the speech text based on the provided HTML structure
    speech_text_list = []
    for p_tag in soup.find_all('p', align="left"):
        for font_tag in p_tag.find_all('font', face="Verdana"):
            speech_text_list.append(font_tag.get_text(strip=True))
    speech_text = ' '.join(speech_text_list).replace('"', "'")

    # Construct the new speech data structure only if all components were found
    if title and author_date and speech_text:
        new_speech = {
            "type": "speech",
            "title": title,
            "citation": author_date,
            "text": speech_text,
            "source": URL
        }

        # Specify the file path (Make sure to use the correct file path where the file is located)
        file_path = 'AP_exam_MCQ_speech_documents.json'

        # Load the existing data or create a new structure if the file doesn't exist
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {'speeches': []}

        # Append the new speech to the "speeches" list within the data dictionary
        data['speeches'].append(new_speech)

        # Save the updated data back to the JSON file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        # Output the file path for confirmation
        print(f"Updated JSON saved to {file_path}")
    else:
        print("Webscraping did not find all required elements, no new speech added.")
else:
    print(f"Failed to retrieve the page: Status code {response.status_code}")
