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
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventory_id INTEGER,
                type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (inventory_id) REFERENCES inventory(id)
            )
        """)
        
        self.conn.commit()


    def create_category(self, name):
        """
        Cria categoria para o banco de dados.
        
        :param self: self
        :param name: Nome da categoria
        """
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            self.conn.commit()
            print(f"Categoria '{name}' criada com sucesso!")
        except Exception as e:
            print(f"[X] Erro: {e}")
    
    
    def create_item(self, name, serial_number, category_name):
        """
        Cria item para adicionar a tabela desejada.
        
        :param self: self
        :param name: Nome do item
        :param serial_number: Número de indentificação do item
        :param category_name: Nome da categoria
        """
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            coluna = cur.fetchone()
            
            if coluna:
                try:
                    category_id = coluna[0]
                    cur.execute("""
                                INSERT INTO inventory (name, serial_number, category_id) 
                                VALUES (?, ?, ?)""", (name, serial_number, category_id)
                                )
                    self.conn.commit()
                    
                except Exception as e:
                    print(f"[X] Erro: {e}")
                             
        except Exception as e:
            print(f"[X] Erro: {e}")