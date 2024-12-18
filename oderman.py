import sqlite3

from flask import Flask, render_template, request, redirect
from weather import weather_get

import sql_oderman_database

app = Flask(__name__)

sql_oderman_database.start_conetion_db()

table_is_not_null = None
try:
    if sql_oderman_database.select_query_func()[-1] == weather_get():
        table_is_not_null = True
        weather_proposition = sql_oderman_database.select_query_func(f"WHERE for_weather == '{weather_get()}'")[0]
    else:
        table_is_not_null = False
except TypeError as error:
    print("пустая таблица")


@app.get("/")
def start():
    menu_positions = sql_oderman_database.select_query_func()

    if table_is_not_null == True:
        return render_template("start_page.html", link="http://127.0.0.1:5001/menu/", action=True,
                               proposition_image=weather_proposition[0],
                               proposition_title=weather_proposition[1],
                               proposition_text=weather_proposition[2],
                               proposition_cost=weather_proposition[3]
                               )
    return render_template("start_page.html", link="http://127.0.0.1:5001/menu/", action=False
                           )


@app.get("/opros")
def result_get():
        return render_template("opros.html")

@app.post("/opros")
def result():
    apros = request.form["opros"]
    print("a")
    with open("results.txt", "a", encoding="utf-8") as file:
        file.write(apros + "\n")
    with open("results.txt", "r", encoding="utf-8") as file:
        text = file.read()
        list = text.split("\n")
        dict = {}

        for w in list:
            count = list.count(w)
            dict[w] = count

        ret1 = ""
        for w, i in dict.items():
            ret1 += f"{w} - {i}\n"

        return ret1


@app.get(f"/admin/")
def admin_page():
    menu_positions = sql_oderman_database.select_query_func()

    return render_template("admin_page.html", menu=menu_positions, message=False)


@app.post(f"/admin/")
def menu_add():
    menu_positions = sql_oderman_database.select_query_func()

    try:
        url = request.form["image"]
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        weather_form = request.form["weather"]
        nums = "1234567890"
        for number in nums:
            if number in name:
                return render_template("error_page.html", error="У назві не можуть бути цифри")

        for num in price:
            if num.isalpha():
                return render_template("error_page.html", error="У ціні не можуть бути букви")

        sql_oderman_database.insert_query_func(url, name, description, price, weather_form)

        return render_template("admin_page.html", menu=menu_positions, message=True)

    except sqlite3.Error():
        return render_template("error_page.html", error="Невідома помилка, перевірте чи немає такої піци вже",
                               link="http://127.0.0.1:5001/admin/")


@app.post("/delete/")
def delete():
    id = request.form["id_delete"]
    sql_oderman_database.delete_query_func(int(id))
    return redirect("/admin/")


@app.get("/edit/<int:pizza_id>")
def edit(pizza_id):
    edit_column = sql_oderman_database.select_query_func(where=f"WHERE id={pizza_id}")
    return render_template("edit.html", editing_column=edit_column[0])


@app.post("/edit/<int:pizza_id>")
def edit_post(pizza_id):
    try:
        url = request.form["image"]
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        nums = "1234567890"
        for number in nums:
            if number in name:
                return render_template("error_page.html", error="У назві не можуть бути цифри")

        for num in price:
            if num.isalpha():
                return render_template("error_page.html", error="У ціні не можуть бути букви")

        sql_oderman_database.update_query_func(url, name, description, int(price), id=pizza_id)

        return redirect("/admin/")

    except sqlite3.Error():
        return render_template("error_page.html", error="Невідома помилка, перевірте чи немає такої піци вже",
                               link=f"http://127.0.0.1:5001/edit/{pizza_id}")


@app.get("/menu/")
def menu():
    menu_positions = sql_oderman_database.select_query_func()
    return render_template("menu_page.html",
                           menu=menu_positions,

                           action_title="Пепероні",
                           action_last_cost="1̶9̶9̶ грн",
                           action_new_cost="169грн"
                           )


@app.get("/comments/")
def comments():
    return render_template("comments_page.html", comments_len=0, comments_start=0)


@app.errorhandler(404)
def error(error):
    return render_template("not_found_page.html")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
    # ТУТ ДОЛЖЕН БЫТЬ ЗАПУСК СКЛ
