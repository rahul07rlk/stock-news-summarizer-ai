# AI Stock News Summarizer

## Project Overview
AI Stock News Summarizer is an advanced Python-based application that fetches and summarizes the latest stock-related news articles using AI. The project utilizes **Google News RSS**, **BeautifulSoup**, and **Newspaper3k** for data extraction, while **Facebook's BART model** is employed for summarization. The goal is to provide traders and investors with concise, high-quality summaries of stock news for better decision-making.

## Features
- Fetches stock news from **Google News RSS**.
- Extracts full article text using **Newspaper3k** and **BeautifulSoup**.
- Summarizes articles using **Facebook's BART model** via Hugging Face's Transformers library.
- Utilizes **Selenium** as a fallback for retrieving full articles.
- Supports **batch processing** for Nifty 500 stocks.
- Saves summarized news to a structured text file.

## Tech Stack
- **Python 3.8+**
- **Hugging Face Transformers** (for AI-powered summarization)
- **Feedparser** (for parsing RSS feeds)
- **BeautifulSoup** (for web scraping)
- **Newspaper3k** (for extracting full article text)
- **Selenium** (for fetching JavaScript-rendered content)
- **Torch (PyTorch)** (for running AI models on GPU)

## Installation
### Prerequisites
- Ensure you have Python 3.8+ installed.
- Install required dependencies using the provided `requirements.txt` file.

```sh
pip install -r requirements.txt
```

## Usage
### Running the Script
To fetch and summarize stock news, run:

```sh
python main.py
```

### Configuration
- **Stock List:** Modify `nifty500_stocks.csv` to include stock symbols of interest.
- **Summarization Settings:** Adjust model parameters inside `main.py` as needed.

## Project Structure
```
stock-news-summarizer-ai/
├── data/
│   ├── latest_stock_news.txt  # Output file containing summarized news
│   ├── nifty500_stocks.csv    # List of stock symbols
├── src/
│   ├── fetch_news.py          # Module for fetching news articles
│   ├── summarize.py          # Module for AI summarization
│   ├── main.py                # Main script to execute
├── README.md                  # Project documentation
├── requirements.txt           # Required dependencies
```

## How to Upload to GitHub
1. **Initialize Git Repository** (if not already initialized)
```sh
git init
```

2. **Add Remote Repository** (replace with your actual GitHub repository URL)
```sh
git remote add origin https://github.com/rahul07rlk/stock-news-summarizer-ai.git
```

3. **Add and Commit Changes**
```sh
git add .
git commit -m "Initial commit - AI Stock News Summarizer"
```

4. **Push Code to GitHub**
```sh
git branch -M main
git push -u origin main
```

## Author
Developed by **Rahul Kumar**.

## License
This project is open source.

