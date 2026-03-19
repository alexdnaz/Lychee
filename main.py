#!/usr/bin/env python3

import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask, g, jsonify, redirect, render_template, request, url_for

from article_manager import ArticleManager

app = Flask(__name__)

# Load environment variables from .env file (if present)
load_dotenv()

# Require FLASK_SECRET_KEY for session security (no insecure fallback)
_secret = os.environ.get("FLASK_SECRET_KEY")
if not _secret:
    raise RuntimeError("FLASK_SECRET_KEY is required. Set it in your environment or .env")
app.secret_key = _secret

app.config["DATABASE"] = "lychee.db"  # Configure the database path

def get_db():
    """Connects to the database, creates a new connection if not already connected."""
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_article', methods=['GET', 'POST'])
def submit_article():
    db = get_db()  # Get the database connection for this request
    article_manager = ArticleManager(db)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['body']  # Using 'body' to match the textarea name in create_article.html
        category = request.form['category']
        article_manager.submit_article_for_vote(title, content, category)
        return redirect(url_for('home'))
    
    categories = article_manager.get_all_categories()
    return render_template('submit_article.html', categories=categories)

@app.route('/search', methods=['GET', 'POST'])
def search():
    db = get_db()  # Get the database connection for this request
    article_manager = ArticleManager(db)

    if request.method == 'POST':
        query = request.form['query']
        results = article_manager.search_articles(query)
        return render_template('search_results.html', results=results)
    
    return render_template('search.html')

@app.route('/articles')  # JSON response
def get_all_articles_json():
    db = get_db()
    article_manager = ArticleManager(db)
    articles = article_manager.get_articles_json()
    return jsonify(articles)

@app.route('/categories')
def view_all_categories():
    db = get_db()  # Use the active database connection
    article_manager = ArticleManager(db)  # Pass the connection to ArticleManager
    categories = article_manager.get_categories_json()  # Fetch categories
    return render_template('view_all_categories.html', categories=categories)  # Render the template




@app.route('/vote/<int:article_id>', methods=['POST'])
def vote_on_article(article_id: int):
    db = get_db()
    vote_str = request.form.get('vote')
    # Map approve/reject to 1/0
    vote_val = 1 if vote_str == 'approve' else 0
    article_manager = ArticleManager(db)
    article_manager.vote_on_article(article_id, vote_val)
    return redirect(url_for('home'))

@app.route('/pending_articles')
def view_pending_articles():
    db = get_db()
    article_manager = ArticleManager(db)
    pending_articles = article_manager.view_pending_articles()
    return render_template('view_pending_articles.html', pending_articles=pending_articles)

@app.route('/view_article/<int:article_id>')
def view_article(article_id):
    db = get_db()
    article_manager = ArticleManager(db)
    article = article_manager.get_article_by_id(article_id)
    return render_template('view_article.html', article=article)

@app.route('/view_all_articles')
def view_all_articles_page():
    db = get_db()
    article_manager = ArticleManager(db)
    articles = article_manager.get_all_articles()
    print("Fetched articles:", articles)  # Debugging output
    return render_template('view_all_articles.html', articles=articles)


@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    with app.app_context():
        print(app.url_map)  # This will show all routes and their names
    # Allow overriding port via PORT env var (default: 8000)
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
