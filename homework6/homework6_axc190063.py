from bs4 import BeautifulSoup
import requests
import re
import os
import fnmatch
import string
import sqlite3
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def web_crawler(topic_url):
    urls = []
    domain = re.findall(r"https?://(?:www\.)?([^\s]+)", topic_url)[0]

    response = requests.get(topic_url)
    data = response.text
    soup = BeautifulSoup(data)

    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            # link_str = str(link.get('href'))
            # print(link_str)
            if domain in href:
                urls.append(href)
            elif 'http' in href:
                urls.append(href)

    urls_list = list(set(urls))[:15]  # return first 15 unique URLs
    print(urls_list)

    return urls_list


def scrape_page_text(urls_list):
    for url in urls_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        with open(f"{url.split('/')[-1]}.txt", "w", encoding='utf-8') as f:
            f.write(text)


def clean_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ').replace('\t', ' ')

    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    sentences = sent_tokenize(text)
    sentences = [sentence for sentence in sentences if sentence not in stopwords.words('english')]

    with open(f"cleaned_{os.path.basename(file_path)}", "w", encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f"{sentence}\n")


def find_files(path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)


def extract_terms(text):
    # Tokenize text
    tokens = word_tokenize(text.lower())

    # Remove stop words and punctuation
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    tokens = [token for token in tokens if token not in stop_words]

    # Compute term frequency
    term_freq = Counter(tokens)

    # Get top 25-40 terms
    top_terms = [term for term, count in term_freq.most_common(40)]

    return top_terms


# Load knowledge base from database
def load_base():
    conn = sqlite3.connect('knowledge_base.db')
    c = conn.cursor()
    c.execute("SELECT * FROM facts")
    rows = c.fetchall()
    kb = {}

    for row in rows:
        kb[row[0]] = row[1]

    conn.close()

    return kb


if __name__ == '__main__':
    starter_url = "https://www.dallascowboys.com"

    scrape_page_text(web_crawler(starter_url))

    for text_file in find_files(r'Documents/Github/Natural_Language_Processing/homework6', '*.txt'):
        clean_text(text_file)
        extract_terms(text_file)

    # Connect to database
    conn = sqlite3.connect('knowledge_base.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS facts (term text, fact text)''')

    # Insert facts into table
    facts = {
        'sport': 'Sport is an activity involving physical exertion and skill in which an individual or team competes against another or others for entertainment.',
        'team': 'A team is a group of people who come together to achieve a common goal.',
        'game': 'A game is a structured form of play, usually undertaken for enjoyment and sometimes used as an educational tool.',
        'player': 'A player is a participant in a game or sport, especially someone who competes professionally.',
        'championship': 'A championship is a competition in which the winner is declared the best in a particular field, such as a sport or game.',
        'score': 'A score is the number of points or goals achieved in a game or competition.',
        'coach': 'A coach is a person who trains and directs a sports team or individual players.',
        'strategy': 'Strategy is a plan of action designed to achieve a particular goal or set of goals.',
        'training': 'Training is the process of preparing someone or something for a particular task or activity.',
        'athlete': 'An athlete is a person who competes in one or more sports, often at a professional level.'
    }

    for term, fact in facts.items():
        c.execute("INSERT INTO facts (term, fact) VALUES (?, ?)", (term, fact))

    # Save changes and close connection
    conn.commit()
    conn.close()
