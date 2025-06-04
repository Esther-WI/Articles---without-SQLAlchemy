from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.connection import get_connection


conn = get_connection()


def list_authors():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()
    for author in authors:
        print(f"Author ID: {author['id']}, Name: {author['name']}")


def show_author_articles(author_id):
    author = Author.find_by_id(author_id)
    if author:
        print(f"\nArticles by {author.name}:")
        for article in author.articles():
            print(f"- {article['title']}")
    else:
        print("Author not found.")


def magazines_with_multiple_authors():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT m.name, COUNT(DISTINCT a.author_id) AS author_count
    FROM magazines m
    JOIN articles a ON m.id = a.magazine_id
    GROUP BY m.id
    HAVING author_count > 2
    """)
    magazines = cursor.fetchall()
    print("\nMagazines with more than 2 contributors:")
    for mag in magazines:
        print(f"- {mag['name']} ({mag['author_count']} authors)")


if __name__ == "__main__":
    list_authors()
    show_author_articles(1)  
    magazines_with_multiple_authors()
