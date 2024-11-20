from flask import Blueprint, render_template, request
from app.models import Article
from datetime import datetime
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Nombre d'articles par page
    
    theme = request.args.get('theme')
    date_str = request.args.get('date')
    
    query = Article.query
    
    if theme:
        query = query.filter(Article.theme == theme)
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        query = query.filter(db.func.date(Article.date) == date.date())
    
    themes = db.session.query(Article.theme).distinct()
    
    pagination = query.order_by(Article.date.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    return render_template('index.html', 
                         articles=pagination.items,
                         pagination=pagination,
                         themes=themes)