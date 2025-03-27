import csv
import feedparser
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import torch
from transformers import pipeline
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import textwrap
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Optionally, uncomment for synchronous CUDA error reporting (for debugging)
# os.environ["CUDA_LAUNCH_BLOCKING"] = "1"

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load AI summarization model (forcing GPU usage)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if device == "cuda" else -1)


# Function to wrap and summarize text with dynamic max_length adjustments
def ai_summarize(text):
    max_input_chars = 3000
    if len(text) > max_input_chars:
        text = text[:max_input_chars]
    if len(text) < 300:
        return text
    # Dynamically adjust max_length based on input length.
    if len(text) < 500:
        dynamic_max_length = 217
    else:
        dynamic_max_length = min(len(text) // 4, 512)
    min_length = max(100, dynamic_max_length // 2)
    try:
        summary = summarizer(text, max_length=dynamic_max_length, min_length=min_length, do_sample=False)[0][
            'summary_text']
        return textwrap.fill(summary, width=80)
    except Exception as e:
        print(f"Summarization failed: {e}")
        fallback = text[:1000] + "..."
        return textwrap.fill(fallback, width=80)


# Function to fetch full article text using multiple methods
def fetch_full_article(url):
    # Method 1: Using newspaper3k
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


# Function to fetch Google News RSS for a given stock
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


# Function to fetch stock news from Google News (only source)
def fetch_stock_news(stock, max_articles=3):
    return {"Google News": fetch_google_news(stock, max_articles)}


# Function to load the list of Nifty 500 stocks from a CSV file
def load_nifty_500_stocks(filename="nifty500_stocks.csv"):
    stocks = []
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip header if present
            for row in reader:
                if row and row[0].strip():
                    stocks.append(row[0].strip())
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return stocks


# Function to save news data to a file
def save_news_to_file(news_data, filename="latest_stock_news.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Latest Stock News Summary\n")
        file.write("=" * 100 + "\n\n")
        for stock, sources in news_data.items():
            file.write(f"Stock: {stock}\n")
            file.write("-" * 100 + "\n")
            for source_name, articles in sources.items():
                file.write(f"Source: {source_name}\n")
                for art in articles:
                    file.write(f"Title     : {art.get('title', '')}\n")
                    file.write(f"Published : {art.get('published', '')}\n")
                    file.write(f"Link      : {art.get('link', '')}\n")
                    file.write("Full Article Summary:\n")
                    file.write(art.get('full_text', '') + "\n")
                    file.write("-" * 50 + "\n")
                file.write("\n")
            file.write("=" * 100 + "\n\n")
    print(f"News saved to {filename}")


# Main function to fetch and save news concurrently for all Nifty 500 stocks
def main():
    stocks = load_nifty_500_stocks()
    if not stocks:
        print("No stocks found. Please ensure the CSV file exists and is correctly formatted.")
        return

    news_data = {}
    max_workers = min(20, len(stocks))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_stock = {executor.submit(fetch_stock_news, stock): stock for stock in stocks}
        for future in as_completed(future_to_stock):
            stock = future_to_stock[future]
            try:
                news_data[stock] = future.result()
            except Exception as e:
                print(f"Error fetching news for {stock}: {e}")

    save_news_to_file(news_data)


if __name__ == "__main__":
    main()
