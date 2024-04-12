import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_and_parse_speech(url, data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensures HTTPError is raised for unsuccessful responses
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())
    # Extracting title, citation, and text based on the given structure
    title = soup.title.text.strip() if soup.title else "No Title Found"
    title = title.replace('\r', '').replace('\n', '').replace('"', "'").replace('\t', '')
    
    citation_tag = soup.find('font', size="1", face="Arial")
    citation = citation_tag.text.strip() if citation_tag else "No Citation Found"
    citation = citation.replace('\r', '').replace('\n', '').replace('"', "'").replace('\t', '')
    
    speech_text = " ".join(p.text.strip() for p in soup.find_all('p', align="left", style="line-height: 150%"))
    speech_text = speech_text.replace('\r', '').replace('\n', '').replace('"', "'").replace('\t', '')

    return {
        "type": "speech",
        "title": title,
        "citation": citation,
        "text": speech_text,
        "url": url
    }

    

# Example usage
def extract_speech_urls(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensures HTTPError is raised for unsuccessful responses
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    speech_links = soup.find_all('a', href=True)  # Find all <a> tags with an href attribute

    urls = []
    for link in speech_links:
        href = link['href']
        if 'speeches' in href and not href.endswith('.pdf') and 'mp3clips' not in href:
            if not href.startswith(('http://', 'https://')):
                href = f"https://www.americanrhetoric.com/{href}"
            urls.append(href)
    
    return urls

# Example usage
file_path='AP_exam_MCQ_speech_documents.json'
base_url = "https://www.americanrhetoric.com/top100speechesall.html"
speech_urls = extract_speech_urls(base_url)

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

print(f"Found {len(speech_urls)} speech URLs.")

for i, url in enumerate(speech_urls):
    if i <= 5:
        continue
    else:
        # print("Url of speech webpage: ", url)
        speech_data = fetch_and_parse_speech(url, data)
        if speech_data:
            data['speeches'].append(speech_data)
        else:
            print("No data was extracted.")

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)










import requests
from bs4 import BeautifulSoup
import json
import os

def extract_color(tag):
    # Check for 'style' attribute color
    if 'style' in tag.attrs:
        styles = tag['style'].split(';')
        for style in styles:
            if 'color' in style:
                color = style.split(':')[-1].strip()
                if color:  # Ensure the color value is not empty
                    return color
    # Check for 'color' attribute
    if 'color' in tag.attrs:
        return tag['color']
    return None  # No color found

def fetch_and_parse_speech(url, data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensures HTTPError is raised for unsuccessful responses
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())
    
    # Extracting title, citation, and text based on the given structure
    title = soup.title.text.strip() if soup.title else "No Title Found"
    title = title.replace('\r', '').replace('\n', '').replace('"', "'").replace('\t', '')
    
    citation_tag = soup.find('font', size="1", face="Arial")
    citation = citation_tag.text.strip() if citation_tag else "No Citation Found"
    citation = citation.replace('\r', '').replace('\n', '').replace('"', "'").replace('\t', '')
    
    # Using the extract_color function to get the color of the citation
    if citation_tag:
        citation_color = extract_color(citation_tag)
    else:
        citation_color = "No color found"
    
    speech_text = " ".join(p.text.strip() for p in soup.find_all('p', align="left", style="line-height: 150%"))
    speech_text = speech_text.replace('\r', '').replace('\n', '').replace('"', "'").replace('\t', '')

    return {
        "type": "speech",
        "title": title,
        "citation": citation,
        "citation_color": citation_color,
        "text": speech_text,
        "url": url
    }

# Additional functions and main script usage remain the same.

# Example usage
# This part of the script remains unchanged.


def extract_color(tag):
    # Check for 'style' attribute color
    if 'style' in tag.attrs:
        styles = tag['style'].split(';')
        for style in styles:
            if 'color' in style:
                color = style.split(':')[-1].strip()
                return color
    # Check for 'color' attribute
    if 'color' in tag.attrs:
        return tag['color']
    return None

# Example usage
def extract_speech_urls(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensures HTTPError is raised for unsuccessful responses
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    speech_links = soup.find_all('a', href=True)  # Find all <a> tags with an href attribute

    urls = []
    for link in speech_links:
        href = link['href']
        if 'speeches' in href and not href.endswith('.pdf') and 'mp3clips' not in href:
            if not href.startswith(('http://', 'https://')):
                href = f"https://www.americanrhetoric.com/{href}"
            urls.append(href)
    
    return urls

# Example usage
file_path='AP_exam_MCQ_speech_documents.json'
base_url = "https://www.americanrhetoric.com/top100speechesall.html"
speech_urls = extract_speech_urls(base_url)

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

print(f"Found {len(speech_urls)} speech URLs.")

for i, url in enumerate(speech_urls):
    if i != 9:
        continue
    else:
        print("\n\n\nUrl of speech webpage: \n\n\n", url)
        speech_data = fetch_and_parse_speech(url, data)
        if speech_data:
            data['speeches'].append(speech_data)
        else:
            print("No data was extracted.")

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
