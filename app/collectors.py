#from bs4 import BeautifulSoup
import feedparser
import requests
from datetime import datetime
from app.models import Article
from app import db

class NewsCollector:
    def __init__(self):
        self.sources = {
            'le_monde_rss': 'https://www.lemonde.fr/rss/une.xml',
            'reuters_rss': 'https://www.reutersagency.com/feed/',
            'france24_rss': 'https://www.france24.com/fr/rss',
            'africa_news': 'https://www.africanews.com/feed/rss'
        }
        
    def collect_rss_feed(self, source_name, source_url):
        feed = feedparser.parse(source_url)
        
        for entry in feed.entries:
            existing_article = Article.query.filter_by(url=entry.link).first()
            if not existing_article:
                # Rechercher l'image dans le flux RSS
                image_url = None
                
                # Chercher dans les médias enclos
                if hasattr(entry, 'media_content'):
                    image_url = entry.media_content[0]['url']
                # Chercher dans les enclosures
                elif hasattr(entry, 'enclosures') and entry.enclosures:
                    for enclosure in entry.enclosures:
                        if 'image' in enclosure.type:
                            image_url = enclosure.href
                # Chercher dans le contenu HTML
                elif hasattr(entry, 'content'):
                    soup = BeautifulSoup(entry.content[0].value, 'html.parser')
                    img_tag = soup.find('img')
                    if img_tag and img_tag.get('src'):
                        image_url = img_tag['src']
                
                # Image par défaut si aucune image n'est trouvée
                if not image_url:
                    image_url = '/static/images/default-article.jpg'

                article = Article(
                    title=entry.title,
                    content=entry.description,
                    source=source_name,
                    theme='General',
                    date=datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z'),
                    url=entry.link,
                    image_url=image_url
                )
                db.session.add(article)
        
        db.session.commit()

    def collect_newsapi(self, api_key):
        url = f'https://newsapi.org/v2/top-headlines'
        params = {
            'country': 'fr',
            'apiKey': api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            news = response.json()
            
            for article_data in news['articles']:
                existing_article = Article.query.filter_by(url=article_data['url']).first()
                if not existing_article:
                    article = Article(
                        title=article_data['title'],
                        content=article_data['description'],
                        source='NewsAPI',
                        theme=article_data.get('category', 'General'),
                        date=datetime.strptime(article_data['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                        url=article_data['url'],
                        image_url=article_data.get('urlToImage', '/static/images/default-article.jpg')
                    )
                    db.session.add(article)
            
            db.session.commit()

    def collect_all(self):
        """Collecter les articles de toutes les sources"""
        # Collecter depuis les flux RSS
        for source_name, source_url in self.sources.items():
            try:
                self.collect_rss_feed(source_name, source_url)
            except Exception as e:
                print(f"Erreur lors de la collecte de {source_name}: {str(e)}")
