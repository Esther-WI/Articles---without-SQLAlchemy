from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None, bio=None):
        self.id = id
        self.name = name
        self.bio = bio


    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO authors (name, bio) VALUES (?, ?)",
            (self.name, self.bio)
        )
        conn.commit()
        self.id = cursor.lastrowid

    @property
    def articles(self):
        from lib.models.article import Article  
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE author_id = ?", (self.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [Article(id=row["id"], title=row["title"], content=row["content"],
                    magazine_id=row["magazine_id"], author_id=row["author_id"]) for row in rows]



    @classmethod
    def create(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name, ))
        conn.commit()
        id = cursor.lastrowid
        conn.close()
        return cls(name=name, id=id)
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], name=row["name"], bio=row["bio"] if "bio" in row.keys() else None)
        else:
            return None
        
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], name=row["name"], bio=row["bio"] if "bio" in row.keys() else None)
        return None

 

    @classmethod
    def all(cls):
       conn = get_connection()
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM authors")
       rows = cursor.fetchall()
       conn.close()
       return [cls(id=row["id"], name=row["name"], bio=row.get("bio")) for row in rows]
    
    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.name, COUNT(ar.id) as article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], name=row["name"])
        return None
    
    def magazines(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.id, m.name, m.category
            FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row["id"], row["name"], row["category"]) for row in rows]
    
    def add_article(self, magazine, title):
        from lib.models.article import Article
        return Article.create(
            title=title,
            content="No content",
            author_id=self.id,
            magazine_id=magazine.id
        )


    
    


