from app.collectors import NewsCollector
from datetime import datetime
import schedule
import time

def update_news():
    print(f"Mise à jour des nouvelles - {datetime.now()}")
    collector = NewsCollector()
    collector.collect_all()

def start_scheduler():
    # Mettre à jour toutes les heures
    schedule.every(1).hours.do(update_news)
    
    while True:
        schedule.run_pending()
        time.sleep(60)