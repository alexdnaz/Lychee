import sqlite3
from flask import g
from article import Article  # Assuming you have an Article class defined in article.py

class ArticleManager:
    def __init__(self, db):
        """Initialize the ArticleManager with a database connection."""
        self.conn = db  # Use the provided connection instead of connecting again
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create the necessary database tables if they don't exist."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS votes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    article_id INTEGER,
                    vote INTEGER NOT NULL,
                    FOREIGN KEY (article_id) REFERENCES articles (id)
                )
            ''')

    def add_category(self, category_name):
        """Add a new category to the database."""
        with self.conn:
            self.conn.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (category_name,))

    def submit_article_for_vote(self, title, content, category):
        """Submit an article for voting under a specific category."""
        with self.conn:
            # Get category ID
            category_id = self.conn.execute('SELECT id FROM categories WHERE name = ?', (category,)).fetchone()
            if category_id:
                self.conn.execute('INSERT INTO articles (title, content, category_id) VALUES (?, ?, ?)',
                                  (title, content, category_id[0]))

    def search_articles(self, query):
        """Search for articles that match the query."""
        with self.conn:
            results = self.conn.execute('SELECT * FROM articles WHERE title LIKE ? OR content LIKE ?',
                                        ('%' + query + '%', '%' + query + '%')).fetchall()
        return results

    def vote_on_article(self, article_id: int, vote: int):
        """Vote on an article by its ID."""
        with self.conn:
            self.conn.execute('INSERT INTO votes (article_id, vote) VALUES (?, ?)', (article_id, vote))

    def get_all_categories(self):
        """Retrieve all categories from the database."""
        with self.conn:
            categories = self.conn.execute('SELECT name FROM categories').fetchall()
        return [cat[0] for cat in categories]

    def get_articles_json(self):
        """Get all articles in JSON format."""
        with self.conn:
            articles = self.conn.execute('SELECT title, content, category_id FROM articles').fetchall()
        return [{'title': title, 'content': content, 'category_id': category_id} for title, content, category_id in articles]

    def get_categories_json(self):
        """Get all categories in JSON format."""
        with self.conn:
            categories = self.conn.execute('SELECT name FROM categories').fetchall()
        return [{'name': name[0]} for name in categories]



    def view_pending_articles(self):
        """Fetch articles with no votes (pending) along with their categories."""
        with self.conn:
            rows = self.conn.execute(
                '''
                SELECT a.id, a.title, a.content, c.name
                FROM articles a
                LEFT JOIN categories c ON a.category_id = c.id
                LEFT JOIN votes v ON v.article_id = a.id
                GROUP BY a.id, c.name
                HAVING COUNT(v.id) = 0
                '''
            ).fetchall()
        pending_articles = []
        for _id, title, content, category in rows:
            pending_articles.append(Article(id=_id, title=title, content=content, category=category, total_votes=0))
        return pending_articles

    def get_all_articles(self):
        """Retrieve all articles with their category names and vote counts."""
        with self.conn:
            rows = self.conn.execute(
                '''
                SELECT a.id, a.title, a.content, c.name, COALESCE(SUM(v.vote), 0)
                FROM articles a
                LEFT JOIN categories c ON a.category_id = c.id
                LEFT JOIN votes v ON v.article_id = a.id
                GROUP BY a.id, c.name
                '''
            ).fetchall()
        return [Article(id=_id, title=title, content=content, category=category, total_votes=total_votes)
                for _id, title, content, category, total_votes in rows]

    def get_article_by_id(self, article_id):
        """Retrieve a single article by ID with its category name and vote count."""
        with self.conn:
            row = self.conn.execute(
                '''
                SELECT a.id, a.title, a.content, c.name, COALESCE(SUM(v.vote), 0)
                FROM articles a
                LEFT JOIN categories c ON a.category_id = c.id
                LEFT JOIN votes v ON v.article_id = a.id
                WHERE a.id = ?
                GROUP BY a.id, c.name
                ''', (article_id,)
            ).fetchone()
        if row:
            _id, title, content, category, total_votes = row
            return Article(id=_id, title=title, content=content, category=category, total_votes=total_votes)
        return None

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()

# Optional demonstration code for running the script independently
if __name__ == '__main__':
    db_file = 'lychee.db'
    conn = sqlite3.connect(db_file)
    manager = ArticleManager(conn)
    manager.create_tables()
    # Add some categories 
    manager.add_category('Technology')
    manager.add_category('Science')

    # Submit some articles
    manager.submit_article_for_vote('Python for Beginners', 'A tutorial on Python basics', 'Technology')
    manager.submit_article_for_vote('The Future of AI', 'An article about artificial intelligence', 'Technology')
    manager.submit_article_for_vote('Quantum Computing Explained', 'A deep dive into quantum computing', 'Science')

    # Get all categories
    categories = manager.get_all_categories()
    print('All Categories:')
    for category in categories:
        print(category)

    manager.close_connection()
