from lib.db.connection import get_connection
from lib.models.article import Article

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (name, category),
        )
        conn.commit()
        id = cursor.lastrowid
        conn.close()
        return cls(id, name, category)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["name"], row["category"])
        else:
            return None

    
    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in rows]
    
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["name"], row["category"])
        return None

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.id, a.name
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row["name"], row["id"]) for row in rows]
    
    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row["title"] for row in rows]
    
    def contributing_authors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.name, COUNT(ar.id) as article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING article_count > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row["name"], row["id"]) for row in rows]

    @classmethod
    def with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            HAVING COUNT(DISTINCT a.author_id) > 1
        """)
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["id"], row["name"], row["category"]) for row in rows]

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.name, COUNT(a.id) as count
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
        """)
        rows = cursor.fetchall()
        conn.close()
        return [(row["name"], row["count"]) for row in rows]

    
    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        row = cursor.fetchone()
        conn.close()
        if row:
           return cls(row["id"], row["name"], row["category"])
        return None
    
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
            self.id = cursor.lastrowid
            conn.commit()
        else:
            cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
            conn.commit()
        conn.close()


         