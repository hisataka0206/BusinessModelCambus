from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hisataka'


@app.route('/')
def index():
    # データベースからデータを取得して表示する
    conn = sqlite3.connect('business_model_canvas.db')
    c = conn.cursor()
    c.execute('''
        SELECT canvas_categories.category_name, canvas_elements.content
        FROM canvas_elements
        JOIN canvas_categories ON canvas_elements.category_id = canvas_categories.id
    ''')

    data = c.fetchall()


    # data を canvas_data という辞書に変換
    canvas_data = {item[0]: item[1] for item in data}
    conn.close()
    # return render_template('index.html', data=data)
    return render_template('cambus.html', canvas_data=canvas_data)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        # データベースにデータを保存する
        conn = sqlite3.connect('business_model_canvas.db')
        c = conn.cursor()
        for key in request.form.keys():
            c.execute('UPDATE canvas_elements SET content=? WHERE name=?', (request.form[key], key))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        # 編集画面を表示する
        conn = sqlite3.connect('business_model_canvas.db')
        c = conn.cursor()
        c.execute('''
            SELECT canvas_categories.category_name, canvas_elements.content
            FROM canvas_elements
            JOIN canvas_categories ON canvas_elements.category_id = canvas_categories.id
        ''')
        data = c.fetchall()
        conn.close()
        return render_template('edit.html', data=data)


@app.route('/save', methods=['POST'])
def save():
    try:
        # フォームからデータを取得
        key_activity = request.form.get('key_activity')
        customer_relationship = request.form.get('customer_relationship')
        key_partners = request.form.get('key_partners')
        value_proposition = request.form.get('value_proposition')
        customer_segment = request.form.get('customer_segment')
        key_resources = request.form.get('key_resources')
        channel = request.form.get('channel')
        cost_structure = request.form.get('cost_structure')
        revenue_streams = request.form.get('revenue_streams')

        # 現在の日時を取得
        now = datetime.now()

        # yyyymmddHHMMSS の形式に変換
        version_id = now.strftime('%Y%m%d%H%M%S')

        # データベースに接続
        conn = sqlite3.connect('business_model_canvas.db')
        c = conn.cursor()

        # データをデータベースに保存
        # この例では、canvas_versions テーブルから最新の version_id を取得して使用します。
        c.execute('SELECT MAX(version_id) FROM canvas_versions')

        # canvas_elements テーブルにデータを保存
        c.execute('''
            INSERT INTO canvas_elements (version_id, category_id, content) 
            VALUES (?, ?, ?)
        ''', (version_id, 1, key_activity)) # category_id 1 は key_activity に対応

        c.execute('''
            INSERT INTO canvas_elements (version_id, category_id, content) 
            VALUES (?, ?, ?)
        ''', (version_id, 2, customer_relationship)) # category_id 2 は customer_relationship に対応
        c.execute('''
            INSERT INTO canvas_elements (version_id, category_id, content) 
            VALUES (?, ?, ?)
        ''', (version_id, 3, key_partners)) # category_id 1 は key_activity に対応

        c.execute('''
            INSERT INTO canvas_elements (version_id, category_id, content) 
            VALUES (?, ?, ?)
        ''', (version_id, 4, value_proposition)) # category_id 2 は customer_relationship に対応
        c.execute('''
            INSERT INTO canvas_elements (version_id, category_id, content) 
            VALUES (?, ?, ?)
        ''', (version_id, 5, customer_segment)) # category_id 1 は key_activity に対応

        c.execute('''
            INSERT INTO canvas_elements (version_id, category_id, content) 
            VALUES (?, ?, ?)
        ''', (version_id, 6, key_resources)) # category_id 2 は customer_relationship に対応
        c.execute('''
            INSERT INTO canvas_elements (version_id, category_id, content) 
            VALUES (?, ?, ?)
        ''', (version_id, 7, channel)) # category_id 1 は key_activity に対応

        c.execute('''
            INSERT INTO canvas_elements (version_id, category_id, content) 
            VALUES (?, ?, ?)
        ''', (version_id, 8, cost_structure)) # category_id 2 は customer_relationship に対応
        c.execute('''
            INSERT INTO canvas_elements (version_id, category_id, content) 
            VALUES (?, ?, ?)
        ''', (version_id, 9, revenue_streams)) # category_id 1 は key_activity に対応

        # 変更をコミット
        conn.commit()

        # データベース接続を閉じる
        conn.close()

        # セーブ完了メッセージを表示
        flash('Data saved successfully!', 'success')
    except Exception as e:
        # エラーメッセージを表示
        print(e)  # コンソールにエラーメッセージを出力（デバッグ用）
        flash('An error occurred while saving data.', 'danger')

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)