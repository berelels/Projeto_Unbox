import sqlite3

class Unbox_Model:
    """
    Classe para lógica de negócio e gerenciamento de estado.
    Atualizada com Locations, Staff e Controle de Estoque Mínimo.
    """
    
    def __init__(self):
        self.conn = None
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
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                building TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                role TEXT DEFAULT 'Professor'
            )
        """)
            
        cur.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                serial_number TEXT UNIQUE,
                category_id INTEGER,
                location_id INTEGER,
                quantity_available INTEGER DEFAULT 0,
                min_stock INTEGER DEFAULT 1,
                FOREIGN KEY (category_id) REFERENCES categories(id),
                FOREIGN KEY (location_id) REFERENCES locations(id)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventory_id INTEGER,
                staff_id INTEGER,
                type TEXT NOT NULL, 
                quantity INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (inventory_id) REFERENCES inventory(id),
                FOREIGN KEY (staff_id) REFERENCES staff(id)
            )
        """)
        
        self.conn.commit()


    def create_location(self, name, building="Principal"):
        """
        Cria um novo local (location) no banco de dados.

        Este método insere um novo registro de localização na tabela 'locations'
        com o nome e edifício especificados.

        Args:
            name (str): Nome do local a ser criado.
            building (str, optional): Nome do edifício ao qual o local pertence.
                                      Padrão é "Principal".
        """
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO locations (name, building) VALUES (?, ?)", (name, building))
            self.conn.commit()
            print(f"[OK] Local '{name}' criado.")
        except Exception as e:
            print(f"[X] Erro ao criar local: {e}")
            

    def create_staff(self, name, role="Professor"):
        """
        Cria um novo membro da equipe no banco de dados.

        Este método insere um registro de um novo membro da equipe na tabela 'staff',
        atribuindo um nome e um papel. O papel padrão é 'Professor'.

        Args:
            name (str): O nome do membro da equipe a ser criado.
            role (str, opcional): O papel do membro da equipe. O padrão é 'Professor'.
        """
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO staff (name, role) VALUES (?, ?)", (name, role))
            self.conn.commit()
            print(f"[OK] Staff '{name}' criado.")
        except Exception as e:
            print(f"[X] Erro ao criar staff: {e}")


    def create_category(self, name):
        """
        Cria uma nova categoria no banco de dados.
        
        Este método insere um novo registro na tabela 'categories' com o nome da categoria fornecido. 
        Em caso de erro durante a inserção, a transação é revertida e uma mensagem de erro é exibida.

        Args:
            name (str): O nome da categoria a ser criada.
        """
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"[X] Erro Categoria: {e}")
            

    def create_item(self, name, serial_number, category_name, location_name, min_stock=1):
        """
        Cria um novo item no inventário.
        Este método insere um item no banco de dados, associando-o a uma categoria e a um local específicos.
        Se a categoria ou o local não forem encontrados, uma mensagem de erro será exibida.
        Args:
            name (str): O nome do item a ser criado.
            serial_number (str): O número de série do item.
            category_name (str): O nome da categoria à qual o item pertence.
            location_name (str): O nome do local onde o item será armazenado.
            min_stock (int, opcional): A quantidade mínima em estoque do item. O padrão é 1.
        """
        try:
            cur = self.conn.cursor()
            
            cur.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            cat_res = cur.fetchone()
            cur.execute("SELECT id FROM locations WHERE name = ?", (location_name,))
            loc_res = cur.fetchone()

            if cat_res and loc_res:
                category_id = cat_res[0]
                location_id = loc_res[0]
                
                cur.execute("""
                    INSERT INTO inventory (name, serial_number, category_id, location_id, min_stock, quantity_available) 
                    VALUES (?, ?, ?, ?, ?, 0)""", 
                    (name, serial_number, category_id, location_id, min_stock)
                )
                self.conn.commit()
                print(f"[OK] Item '{name}' criado em '{location_name}'.")
                
            else:
                print(f"[X] Erro: Categoria '{category_name}' ou Local '{location_name}' não encontrados.")
                            
        except Exception as e:
            self.conn.rollback()
            print(f"[X] Erro Item: {e}")


    def register_movement(self, serial_number, movement_type, quantity, staff_name):
        """
        Registra um movimento de entrada ou saída de um item no inventário.
        
        Este método atualiza a quantidade disponível de um item no inventário e registra o movimento
        realizado por um funcionário. Se o movimento for de saída, verifica se há estoque suficiente.
        Args:
            serial_number (str): O número de série do item a ser movimentado.
            movement_type (str): O tipo de movimento ('IN' para entrada, 'OUT' para saída).
            quantity (int): A quantidade a ser movimentada.
            staff_name (str): O nome do funcionário que está realizando o movimento.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, quantity_available FROM inventory WHERE serial_number = ?", (serial_number,))
            if not (item := cursor.fetchone()):
                 raise ValueError("Item não encontrado.")
            inventory_id, current_stock = item

            cursor.execute("SELECT id FROM staff WHERE name = ?", (staff_name,))
            if not (staff_res := cursor.fetchone()):
                 raise ValueError(f"Funcionário '{staff_name}' não cadastrado.")
            staff_id = staff_res[0]
            
            delta = -quantity if movement_type == 'OUT' else quantity
            
            if movement_type == 'OUT' and current_stock < quantity:
                raise ValueError(f"Estoque insuficiente! Disponível: {current_stock}")

            new_stock = current_stock + delta

            cursor.execute("UPDATE inventory SET quantity_available = ? WHERE id = ?", (new_stock, inventory_id))
            cursor.execute("""
                INSERT INTO movements (inventory_id, staff_id, type, quantity) 
                VALUES (?, ?, ?, ?)""", (inventory_id, staff_id, movement_type, quantity)
            )

            self.conn.commit()
            print(f"[OK] Movimento '{movement_type}' registrado para {staff_name}.")

        except Exception as e:
            self.conn.rollback()
            print(f"[X] Erro Movimento: {e}")