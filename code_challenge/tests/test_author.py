import pytest
from lib.models.author import Author

def test_create_and_find_author():
    author = Author.create("Test Author")
    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.name == "Test Author"

def test_find_nonexistent_author():
    author = Author.find_by_id(-1)
    assert author is None
