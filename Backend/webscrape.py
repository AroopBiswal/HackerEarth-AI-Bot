import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://help.hackerearth.com/"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def scrape_articles(url):
    soup = get_soup(url)
    articles = soup.find_all('div', class_='c-article-card')
    
    content = ""
    for article in articles:
        title = article.find('h3', class_='c-article-card__title').get_text(strip=True)
        link = BASE_URL + article.find('a')['href']
        article_content = scrape_article_content(link)
        content += f"Title: {title}\n"
        content += f"Link: {link}\n"
        content += f"Content:\n{article_content}\n\n"
    
    return content

def scrape_article_content(url):
    soup = get_soup(url)
    paragraphs = soup.find_all('p')
    text = "\n".join([para.get_text(strip=True) for para in paragraphs])
    return text

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    main_page_url = BASE_URL
    content = scrape_articles(main_page_url)
    
    save_to_file(content, './Knowledge_Base/hackerearth_help.txt')

if __name__ == "__main__":
    main()
