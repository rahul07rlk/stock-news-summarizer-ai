import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.fetch_news import fetch_stock_news

def load_nifty_500_stocks(filename="data/nifty500_stocks.csv"):
    stocks = []
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            for row in reader:
                if row and row[0].strip():
                    stocks.append(row[0].strip())
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return stocks

def save_news_to_file(news_data, filename="data/latest_stock_news.txt"):
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
