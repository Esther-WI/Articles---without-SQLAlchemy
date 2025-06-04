from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed():
    author1 = Author.create("Esther Agyapong")
    author2 = Author.create("John Doe")

    mag1 = Magazine.create("Tech Monthly", "Technology")
    mag2 = Magazine.create("Health Today", "Health")

    
    Article.create("How Python Changed the World", "A deep dive into Python’s impact.", author1.id, mag1.id)
    Article.create("Healthy Living Tips", "Tips to improve your health.", author2.id, mag2.id)
    Article.create("AI in 2025", "The future of artificial intelligence.", author1.id, mag1.id)

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
