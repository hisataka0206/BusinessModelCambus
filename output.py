from flask import Flask, render_template_string
import sqlite3
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def display_canvas():
    data = fetch_data_from_db()
    updated_html = update_and_display_html(data)
    print(updated_html[:2000])  # 最初の1000文字だけを表示しています
    return render_template_string(updated_html)


def fetch_data_from_db():
    with sqlite3.connect("business_model_canvas.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM canvas_elements")
        data = cursor.fetchall()
        return dict(data)


def update_and_display_html(data):
    with open("cambus.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    for element_id, content in data.items():
        tag = soup.find(id=element_id)
        if tag:
            tag.string = content

    return str(soup)


if __name__ == '__main__':
    app.run(debug=True)
