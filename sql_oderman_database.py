import sqlite3




def start_conetion_db() -> None:
    sqlite_connection = sqlite3.connect("sql_oderman_menu.db")

    cursor = sqlite_connection.cursor()

    sqlite_select_query = "SELECT sqlite_version()"
    cursor.execute(sqlite_select_query)

    table_create_pizzas = """CREATE TABLE IF NOT EXISTS Pizzas (
      id INTEGER PRIMARY KEY,
      url_image TEXT NOT NULL,
      item TEXT NOT NULL UNIQUE,
      description TEXT NOT NULL,
      amount INTEGER NOT NULL,
      for_weather TEXT NOT NULL
      );
      """
    print("table checked")

    cursor.execute(table_create_pizzas)
    cursor.close()
    sqlite_connection.close()

def insert_query_func(*args) -> None:
    sqlite_connection = sqlite3.connect("sql_oderman_menu.db")

    cursor = sqlite_connection.cursor()

    sqlite_select_query = "SELECT sqlite_version()"
    cursor.execute(sqlite_select_query)

    table_insert = """INSERT INTO Pizzas (url_image, item, description, amount, for_weather)
        VALUES (?,?,?,?,?);"""

    print("inserted")

    cursor.execute(table_insert, args)

    cursor.close()
    sqlite_connection.commit()
    sqlite_connection.close()


def select_query_func(where: str | None = ""):
    sqlite_connection = sqlite3.connect("sql_oderman_menu.db")

    cursor = sqlite_connection.cursor()

    table_select = f"""SELECT * FROM Pizzas
        {where};"""

    cursor.execute(table_select)

    return1 = cursor.fetchall()

    print(f"getted {return1}")

    cursor.close()
    sqlite_connection.close()

    return return1


def delete_query_func(id: int):
    sqlite_connection = sqlite3.connect("sql_oderman_menu.db")

    cursor = sqlite_connection.cursor()

    table_delete = f"""DELETE FROM Pizzas WHERE id='{id}';"""

    cursor.execute(table_delete)

    cursor.close()
    sqlite_connection.commit()
    sqlite_connection.close()
    print(f"delete-{id}")


def update_query_func(*args, id:int) -> None:
    sqlite_connection = sqlite3.connect("sql_oderman_menu.db")

    cursor = sqlite_connection.cursor()

    table_insert = f"""UPDATE Pizzas
                      SET url_image = ?, item = ?, description = ?, amount = ?
                      WHERE id = ?;"""

    print("inserted")

    cursor.execute(table_insert, (args[0], args[1], args[2], args[3], id))

    cursor.close()
    sqlite_connection.commit()
    sqlite_connection.close()


def create_table_comments() -> None:
    sqlite_connection = sqlite3.connect("sql_oderman_menu.db")

    cursor = sqlite_connection.cursor()

    sqlite_select_query = "SELECT sqlite_version()"
    cursor.execute(sqlite_select_query)

    create_query = """
    CREATE TABLE IF NOT EXISTS Comments (
      id INTEGER PRIMARY KEY,
      text TEXT NOT NULL,
      stars INTEGER NOT NULL
      );
    """

    cursor.execute(create_query)


def select_query_comments(where: str | None = ""):
    sqlite_connection = sqlite3.connect("sql_oderman_menu.db")

    cursor = sqlite_connection.cursor()

    table_select = f"""SELECT * FROM Comments
        {where};"""

    cursor.execute(table_select)

    return1 = cursor.fetchall()

    print(f"getted {return1}")

    cursor.close()
    sqlite_connection.close()

    return return1



def insert_query_comments(*args) -> None:
    sqlite_connection = sqlite3.connect("sql_oderman_menu.db")

    cursor = sqlite_connection.cursor()

    table_insert = """INSERT INTO Comments (text, stars)
        VALUES (?,?);"""

    print("inserted")

    cursor.execute(table_insert, args)

    cursor.close()
    sqlite_connection.commit()
    sqlite_connection.close()