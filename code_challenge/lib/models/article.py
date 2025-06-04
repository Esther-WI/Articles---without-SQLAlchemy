from lib.db.connection import get_connection
from lib.models.author import Author


class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    
   
    @classmethod
    def create(cls, title, content, author_id, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
            (title, content, author_id, magazine_id),
        )
        conn.commit()
        id = cursor.lastrowid
        conn.close()
        return cls(id, title, content, author_id, magazine_id)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"])
        else:
            return None
        
    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"])
        return None


    
    def author(self):
        return Author.find_by_id(self.author_id)


    def magazine(self):
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)
