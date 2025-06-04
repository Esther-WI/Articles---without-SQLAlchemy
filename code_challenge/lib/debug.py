from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

new_author = Author.create("Esther is the author")
print(new_author.id)
print(new_author.name)


found_author = Author.find_by_id(1)
print(found_author.name)

article = Article.create(
    "How Python Changed the World",
    "A deep dive into Python’s impact.",
    1,  
    1   
)

print(article.title)
print(article.author().name)    
print(article.magazine().name)

mag = Magazine.create("Tech Monthly", "Technology")
print(mag.name)
for article in mag.articles():
    print(article.title)