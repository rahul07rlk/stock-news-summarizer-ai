import feedparser
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from src.summarize import ai_summarize


def fetch_full_article(url):
    # Method 1: Using Newspaper3k
    try:
        article = Article(url)
        article.download()
        article.parse()
        if len(article.text) > 500:
            return ai_summarize(article.text)
    except Exception as e:
        print(f"Newspaper3k failed for {url}: {e}")

    # Method 2: Using BeautifulSoup
    try:
        headers = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/110.0.0.0 Safari/537.36")
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        full_text = " ".join([p.get_text() for p in paragraphs if len(p.get_text()) > 50])
        if full_text:
            return ai_summarize(full_text)
    except Exception as e:
        print(f"BeautifulSoup failed for {url}: {e}")

    # Method 3: Using Selenium (fallback for JavaScript-heavy pages)
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(3)
        text = driver.find_element(By.TAG_NAME, "body").text
        driver.quit()
        if len(text) > 500:
            text = text[:3000]
            return ai_summarize(text)
        else:
            return "Full article text could not be retrieved."
    except Exception as e:
        print(f"Selenium failed for {url}: {e}")

    return "Full article text could not be retrieved."


def fetch_google_news(stock, max_articles=3):
    rss_url = f"https://news.google.com/rss/search?q={stock}+stock&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries[:max_articles]:
        full_text = fetch_full_article(entry.link)
        articles.append({
            "title": entry.title,
            "published": entry.get("published", "N/A"),
            "link": entry.link,
            "full_text": full_text
        })
    return articles


def fetch_stock_news(stock, max_articles=3):
    return {"Google News": fetch_google_news(stock, max_articles)}
