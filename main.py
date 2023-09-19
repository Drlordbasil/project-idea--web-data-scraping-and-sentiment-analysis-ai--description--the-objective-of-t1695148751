import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer


class WebDataScraper:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def scrape_data_from_website(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape data from {url}. Error: {e}")
            return None

    def analyze_sentiment(self, text):
        sentiment_score = self.sia.polarity_scores(text)
        sentiment = self.get_sentiment_from_score(sentiment_score['compound'])
        return sentiment, sentiment_score

    @staticmethod
    def get_sentiment_from_score(score):
        if score > 0:
            return 'positive'
        elif score < 0:
            return 'negative'
        else:
            return 'neutral'


class SentimentAnalyzer:
    def __init__(self, scraper):
        self.scraper = scraper

    def analyze_sentiment(self, urls):
        results = []
        for url in urls:
            content = self.scraper.scrape_data_from_website(url)
            if content is not None:
                sentiment, sentiment_score = self.scraper.analyze_sentiment(content)
                results.append({'url': url, 'sentiment': sentiment, 'sentiment_score': sentiment_score})
        return results


class SentimentAnalysisVisualizer:
    def __init__(self):
        self.sentiment_labels = ['positive', 'negative', 'neutral']

    def visualize_sentiment_distribution(self, sentiment_scores):
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        for sentiment_score in sentiment_scores:
            sentiment = sentiment_score['sentiment']
            sentiment_counts[sentiment] += 1

        counts = [sentiment_counts[sentiment] for sentiment in self.sentiment_labels]

        plt.bar(self.sentiment_labels, counts)
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.title('Sentiment Distribution')
        plt.show()


class WebDataAnalyzer:
    def __init__(self, scraper):
        self.scraper = scraper
        self.sentiment_analyzer = SentimentAnalyzer(scraper)
        self.visualizer = SentimentAnalysisVisualizer()

    def analyze_sentiment(self, urls):
        sentiment_scores = self.sentiment_analyzer.analyze_sentiment(urls)
        self.visualizer.visualize_sentiment_distribution(sentiment_scores)


class WebDataAnalyzerApp:
    def __init__(self):
        self.scraper = WebDataScraper()
        self.analyzer = WebDataAnalyzer(self.scraper)

    def run_sentiment_analysis(self, urls):
        self.analyzer.analyze_sentiment(urls)


if __name__ == "__main__":
    app = WebDataAnalyzerApp()
    news_urls = [
        'http://example.com/news1',
        'http://example.com/news2'
    ]
    app.run_sentiment_analysis(news_urls)

    product_url = 'http://example.com/product'
    app.run_sentiment_analysis([product_url])

    platform = 'http://example.com/twitter'
    keyword = 'python'
    search_url = f"{platform}/search?q={keyword}"
    app.run_sentiment_analysis([search_url])

    job_portal_url = 'http://example.com/jobs'
    app.run_sentiment_analysis([job_portal_url])

    financial_platform_url = 'http://example.com/stocks'
    app.run_sentiment_analysis([financial_platform_url])