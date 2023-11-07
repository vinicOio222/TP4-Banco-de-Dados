import sqlite3 as sql

class Livro:
    def __init__(self, titulo, id_autor):
        self.titulo = titulo
        self.id_autor = id_autor

class Autor:
    def __init__(self, id_autor, nome_autor):
        self.id_autor = id_autor
        self.nome_autor = nome_autor

class DataBase:
    def __init__(self):
        self.conn = sql.connect("BD-TP4//Biblioteca.db")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        query_livro = '''CREATE TABLE IF NOT EXISTS Livro(
                ID_Livro INTEGER PRIMARY KEY AUTOINCREMENT,
                Titulo TEXT NOT NULL,
                ID_Autor INTEGER NOT NULL,
                FOREIGN KEY(ID_Autor) REFERENCES Autor(ID_Autor) ON UPDATE CASCADE ON DELETE CASCADE
                );'''
        query_autor = '''CREATE TABLE IF NOT EXISTS Autor(
                ID_Autor INTEGER PRIMARY KEY,
                Nome_Autor TEXT NOT NULL
                );'''
        self.cursor.execute(query_livro)
        self.cursor.execute(query_autor)
        self.conn.commit()

    def adicionar_livro(self, livro):
        query_livro = '''INSERT INTO Livro(Titulo, ID_Autor) VALUES (?, ?)'''
        values = (livro.titulo, livro.id_autor)
        self.cursor.execute(query_livro, values)
        self.conn.commit()
        print("Livro adicionado com sucesso!")

    def adicionar_autor(self, autor):
        query_autor = '''INSERT INTO Autor(ID_Autor, Nome_Autor) VALUES (?, ?)'''
        values = (autor.id_autor, autor.nome_autor)
        self.cursor.execute(query_autor, values)
        self.conn.commit()
        print("Autor adicionado com sucesso!")

    def pesquisar_livro(self, id):
        query = '''SELECT * FROM Livro
                   WHERE ID_Livro = ?;'''
        values = (id,)
        result = self.cursor.execute(query, values).fetchone()
        if result is not None:
            print("---Livro Encontrado---\n")
            print(f"ID do Livro: {result[0]}")
            print(f"Titulo: {result[1]}")
            print(f"Autor: {result[2]}")

        self.conn.commit()

    def pesquisar_autor(self, id):
        query = '''SELECT * FROM Autor
                   WHERE ID_Autor = ?;'''
        values = (id,)
        result = self.cursor.execute(query, values).fetchone()
        if result is not None:
            print("---Livro Encontrado---")
            print(f"ID do Autor: {result[0]}")
            print(f"Nome do Autor: {result[1]}")

        self.conn.commit()

    def listar_livros(self):
        query = '''SELECT * FROM Livro;'''
        result = self.cursor.execute(query).fetchall()
        if result is not None:
            print("-- Lista de Livros ---")
            for tupla in result:
                print(f"ID do Livro: {tupla[0]}")
                print(f"Titulo: {tupla[1]}")
                print(f"ID Autor: {tupla[2]}\n")
        else:
            print("Lista de livros vazia!")

        self.conn.commit()

    def listar_autores(self):
        query = '''SELECT * FROM Autor'''
        result = self.cursor.execute(query).fetchall()
        if result is not None:
            print("-- Lista de Autores ---")
            for tupla in result:
                print(f"ID do Autor: {tupla[0]}")
                print(f"Nome do Autor: {tupla[1]}\n")
        else:
            print("Lista de livros vazia!")

        self.conn.commit()

    def atualizar_livro(self, id_livro, campo, novo_valor):
        if campo == "Titulo":
            query = "UPDATE Livro SET Titulo = ? WHERE ID_Livro = ?"
        elif campo == "ID_Autor":
            query = "UPDATE Livro SET ID_Autor = ? WHERE ID_Livro = ?"
        elif campo == "ID_Livro":
            query = "UPDATE Livro SET ID_Livro = ? WHERE ID_Livro = ?"
        else:
            print("Campo inválido")

        existencia = self.cursor.execute("SELECT 1 FROM Livro WHERE ID_Livro = ?", (id_livro,)).fetchone()
        if existencia:
            values = (novo_valor, id_livro)
            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"Campo {campo} do livro com ID {id_livro} atualizado para {novo_valor} com sucesso!")
        else:
           print(f"Livro com ID {id_livro} não encontrado.")

    def atualizar_autor(self, id_autor, campo, novo_valor):
        if campo == "Nome_Autor":
            query = "UPDATE Autor SET Nome_Autor = ? WHERE ID_Autor = ?"
        elif campo == "ID_Autor":
            query = "UPDATE Autor SET ID_Autor = ? WHERE ID_Autor = ?"
        else:
            print("Campo inválido")

        existencia = self.cursor.execute("SELECT 1 FROM Autor WHERE ID_Autor = ?", (id_autor,)).fetchone()
        if existencia:
            values = (novo_valor, id_autor)
            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"Campo {campo} do autor com ID {id_autor} atualizado para {novo_valor} com sucesso!")
        else:
            print(f"Autor com ID {id_autor} não encontrado.")

    def remover_autor(self, id):
        existencia = self.cursor.execute("SELECT 1 FROM Autor WHERE ID_Autor = ?", (id,)).fetchone()
        if existencia:
            query_remocao = "DELETE FROM Autor WHERE ID_Autor = ?;"
            values = (id,)
            self.cursor.execute(query_remocao, values)
            self.conn.commit()
            print(f"Autor com ID {id} foi removido com sucesso!")
        else:
            print(f"Autor com ID {id} não encontrado.")

    def remover_livro(self, id):
        existencia = self.cursor.execute("SELECT 1 FROM Livro WHERE ID_Livro = ?", (id,)).fetchone()
        if existencia:
            query_remocao = "DELETE FROM Livro WHERE ID_Livro = ?;"
            values = (id,)
            self.cursor.execute(query_remocao, values)
            self.conn.commit()
            print(f"Livro com ID {id} foi removido com sucesso!")
        else:
            print(f"Livro com ID {id} não encontrado.")

    def buscar_letras_titulo_livro(self, letras_livro):
       query = "SELECT * FROM Livro WHERE Titulo LIKE ?"
       values = ("%" + letras_livro + "%",)
       resultados = self.cursor.execute(query, values).fetchall()

       if resultados:
           for linha in resultados:
               print(f"ID do Livro: {linha[0]}")
               print(f"Titulo: {linha[1]}")
               print(f"Autor: {linha[2]}\n")
       else:
           print("Nenhum livro correspondente encontrado.")

    def buscar_letras_nome_autor(self, letras_nome):
       query = "SELECT * FROM Autor WHERE Nome_Autor LIKE ?"
       values = ("%" + letras_nome + "%",)
       resultados = self.cursor.execute(query, values).fetchall()

       if resultados:
           for linha in resultados:
               print(f"ID do Autor: {linha[0]}")
               print(f"Nome do Autor: {linha[1]}")
       else:
           print("Nenhum autor correspondente encontrado.")

    def adicionar_lista_livros(self, lista_livros):
        for livro in lista_livros:
            titulo = livro.titulo
            id_autor = livro.id_autor
            query = "INSERT INTO Livro(Titulo, ID_Autor) VALUES (?, ?)"
            values = (titulo, id_autor)
            self.cursor.execute(query, values)
        self.conn.commit()
        print("Livros adicionados com sucesso!")

    def fechar_conexao(self):
        self.cursor.close()


# db = DataBase()
# a1 = Autor(121, "Soul Dur Guetto")
# db.adicionar_autor(a1)
# a2 = Autor(122, "Gojivaldo Saturado")
# db.adicionar_autor(a2)
# l1 = Livro("Vazio Roxo", 122)
# db.adicionar_livro(l1)
# db.pesquisar_autor(122)
# db.atualizar_livro(1, "ID_Livro", 333)
# db.remover_autor(122)
# db.listar_autores()
# db.listar_livros()
# db.buscar_letras_titulo("io Ro")
# db.buscar_letras_nome_autor("Soul")
# livros = [
#     Livro("Um pesadelo chamado Vida", 121),
#     Livro("Como lidar com desafios pessoais", 121),
#     Livro("Vazio Branco", 122),
#     Livro("Manual da Mente", 121),
#     Livro("Vazio Vermelho", 122)
# ]

# db.adicionar_lista_livros(livros)
#db.atualizar_livro(2, "Titulo", "Um pesadelo chamado Morte")
# db.atualizar_autor(122, "ID_Autor", 133)
# db.fechar_conexao()
