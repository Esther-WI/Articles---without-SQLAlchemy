import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

def test_create_and_find_article():
    author = Author.create("Article Author")
    magazine = Magazine.create("Article Magazine", "Category")
    article = Article.create("Test Title", "Test Content", author.id, magazine.id)
    
    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.title == "Test Title"
    assert found.author_id == author.id
    assert found.magazine_id == magazine.id

def test_article_relations():
    author = Author.create("Rel Author")
    magazine = Magazine.create("Rel Magazine", "Category")
    article = Article.create("Rel Title", "Rel Content", author.id, magazine.id)

    assert article.author().id == author.id
    assert article.magazine().id == magazine.id

def test_find_nonexistent_article():
    article = Article.find_by_id(-1)
    assert article is None
