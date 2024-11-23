import sqlite3

from flask import Flask, render_template, request
from weather import weather_get

import sql_oderman_database
app = Flask(__name__)



sql_oderman_database.start_conetion_db()


menu_positions = sql_oderman_database.select_query_func()

table_is_not_null=None
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
    if table_is_not_null == True:
        return render_template("start_page.html", link="http://127.0.0.1:5001/menu/", action=True,
                           proposition_image=weather_proposition[0],
                           proposition_title=weather_proposition[1],
                           proposition_text=weather_proposition[2],
                           proposition_cost=weather_proposition[3]
                           )
    return render_template("start_page.html", link="http://127.0.0.1:5001/menu/", action=False
                           )




@app.get(f"/admin/")
def admin_page():
    return render_template("admin_page.html", menu=menu_positions, message=False)


@app.post(f"/admin/")
def menu_add():
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
      return render_template("error_page.html", error="Невідома помилка, перевірте чи немає такої піци вже")

@app.get("/menu/")
def menu():
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
    #ТУТ ДОЛЖЕН БЫТЬ ЗАПУСК СКЛ