class Article:
    def __init__(self, id, title, content, category, total_votes):
        self.id = id
        self.title = title
        self.content = content
        # For templates
        self.category = category
        self.total_votes = total_votes

    def __repr__(self):
        return (
            "Article("
            f"id={self.id}, title={self.title!r}, category={self.category!r}, total_votes={self.total_votes}"
            ")"
        )
