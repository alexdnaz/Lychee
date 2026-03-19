import sqlite3
from article_manager import ArticleManager

class Lychee:
    def __init__(self):
        self.title = "The Lychee Project:"
        self.description = "A knowledge base, built by you. The Lychee Encyclopedia is a place to store, read, and organize facts and knowledge."
        self.article_manager = ArticleManager('lychee.db')  # Initialize with database file

    def create_article(self, title, content, category):
        self.article_manager.submit_article_for_vote(title, content, category)

    def search_articles(self, query):
        return self.article_manager.search_articles(query)

    def create_initial_categories(self):
        categories = [
            "Science", "History", "Technology", "Politics", "Society", "Culture", 
            "Arts", "Environment", "Health", "Education", "Lifestyle", "Finance", 
            "Business", "Animals", "Nature", "Food", "Travel", "Geography", "Biographies"
        ]
        for category in categories:
            self.article_manager.add_category(category)

    def run(self):
        print(f"{self.title}\n{self.description}\n\nLychee is Running\n\nCategories:")
        for category in self.article_manager.get_all_categories():
            print(f" • {category}")
