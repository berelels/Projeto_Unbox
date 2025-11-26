import sqlite3

class Unbox_Model:
    """
    Classe para lógica de negócio e gerenciamento de estado.
    """
    
    def __init__(self):
        self.conn = None
        self.categoria = ""
        self.item = ""
        self.conn = sqlite3.connect('inventory.db')
        self.conn.execute("PRAGMA foreign_keys = ON")
        cur = self.conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
            
        cur.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                serial_number TEXT UNIQUE,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        
        self.conn.commit()