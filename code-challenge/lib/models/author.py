from lib.db.connection import get_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name


    @classmethod
    def create(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name, ))
        conn.commit()
        id = cursor.lastrowid
        conn.close()
        return cls(id, name)
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["name"])
        else:
            return None
 

    @classmethod
    def all(cls):
       conn = get_connection()
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM authors")
       rows = cursor.fetchall()
       conn.close()
       return [cls(row["id"], row["name"]) for row in rows]
