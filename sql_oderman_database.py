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

    print("getted")

    cursor.execute(table_select)

    return1 = cursor.fetchall()

    cursor.close()
    sqlite_connection.close()

    return return1
