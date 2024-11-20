from app import create_app, db
from app.collectors import NewsCollector
import threading
from app.tasks import start_scheduler

app = create_app()

def start_collection_scheduler():
    """Démarrer le planificateur de collecte dans un thread séparé"""
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Première collecte au démarrage
        collector = NewsCollector()
        collector.collect_all()
        
        # Démarrer le planificateur
        start_collection_scheduler()
        
    app.run(debug=True)