# Stock News Summarizer

This project fetches and summarizes stock news for companies in the Nifty 500 using the Google News RSS feed. The news articles are automatically summarized with an AI model (Facebook's BART large CNN) using Hugging Face's transformers library. The summarized news is saved in a human-readable text file.

## Features

- **Fetch News:** Retrieves stock-related news from Google News RSS.
- **Article Summarization:** Uses AI to summarize full article content.
- **Concurrent Processing:** Fetches news for multiple stocks in parallel for efficiency.
- **Dynamic Summarization:** Automatically adjusts summarization parameters based on input length.
- **Output File:** Generates a text file with a professional, multi-line summary for each stock.

## Prerequisites

- Python 3.7 or later
- A compatible GPU is recommended for faster summarization (optional)

## Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/rahul07rlk/stock-news-summarizer-ai
   cd stock-news-summarizer-ai
