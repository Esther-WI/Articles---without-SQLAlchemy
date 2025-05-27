import pytest
from lib.models.magazine import Magazine

def test_create_and_find_magazine():
    magazine = Magazine.create("Test Magazine", "Test Category")
    found = Magazine.find_by_id(magazine.id)
    assert found is not None
    assert found.name == "Test Magazine"
    assert found.category == "Test Category"

def test_find_nonexistent_magazine():
    magazine = Magazine.find_by_id(-1)
    assert magazine is None
