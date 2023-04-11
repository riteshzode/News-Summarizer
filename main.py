import gradio as gr
from gradio import components
from newspaper import Article
from textblob import TextBlob


def summarize_news(url):
    if not url:
        return "Error: Please enter a valid URL."

    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        title = article.title
        source_url = article.url
        authors = ", ".join(article.authors)
        publication_date = article.publish_date
        summary = article.summary

        blob = TextBlob(article.text)
        sentiment = "Positive" if blob.polarity > 0 else "Negative" if blob.polarity < 0 else "Neutral"

        output_str = f"Title: {title}\n\nSource URL: {source_url}\n\nAuthors: {authors}\n\nPublication Date: {publication_date}\n\nSummary: {summary}\n\nSentiment: {sentiment}"

        return output_str

    except:
        return "Error: Failed to summarize the news. Please check the URL and try again."


# Create an input component for URL
input_url = components.Textbox(label="Enter URL of news article", lines=1)

# Create an output component for displaying the results as text
output = "text"

example_news = [['https://www.thesun.co.uk/sport/21998096/leicester-dean-smith-chelsea-john-terry/'],
                [
                    'https://www.livemint.com/market/live-blog/share-market-live-updates-sensex-nifty-bse-nse-stock-market-today-11-04-2023-11681172305830.html'],
                [
                    'https://www.cnbctv18.com/market/share-market-live-updates-nifty-sensex-bse-nse-stock-market-today-delta-corp-kalpataru-adani-16372361.htm']]

# Create a Gradio interface
demo = gr.Interface(summarize_news, inputs=input_url, outputs=output, title="News Summarizer",
                    description="Enter the URL of a news article to get its title, source URL, authors, publication date, summary, and sentiment.",
                    examples=example_news)

demo.launch()
