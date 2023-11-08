from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'hisataka'


@app.route('/', methods=['GET'])
@app.route('/<version_id>', methods=['GET'])
def index(version_id=None):
    before_version_id = version_id
    # カレントディレクトリ内の .db ファイルをリストアップ
    db_files = [f for f in os.listdir('database') if f.endswith('.db')]
    # 選択されたデータベース名を取得、もしくは前回のセッションから取得
    db_name = request.args.get('db_name', session.get('db_name', 'default.db'))
    # 選択されたデータベース名をセッションに保存
    session['db_name'] = db_name
    db_name = "database/" + db_name
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # 特定のバージョンが指定されている場合、そのバージョンのデータを取得
    if db_name != 'database/default.db':
        if version_id:
            c.execute('''
                SELECT 
                    canvas_categories.category_name, 
                    canvas_elements.content,
                    canvas_versions.title,
                    canvas_versions.comment
                FROM canvas_elements
                JOIN canvas_categories ON canvas_elements.category_id = canvas_categories.id
                LEFT JOIN canvas_versions ON canvas_elements.version_id = canvas_versions.version_id
                WHERE canvas_elements.version_id = ?
            ''', (version_id,))
        else:
            c.execute('''
                SELECT 
                    canvas_categories.category_name, 
                    canvas_elements.content,
                    canvas_versions.title,
                    canvas_versions.comment
                FROM canvas_elements
                JOIN canvas_categories ON canvas_elements.category_id = canvas_categories.id
                LEFT JOIN canvas_versions ON canvas_elements.version_id = canvas_versions.version_id
                WHERE canvas_elements.version_id = (SELECT MAX(version_id) FROM canvas_elements)
            ''')

        data = c.fetchall()
        title = data[0][2] if data else None
        comment = data[0][3] if data else None
        c.execute('SELECT DISTINCT version_id FROM canvas_elements')
        versions = [row[0] for row in c.fetchall()]
        version_id = max(versions) if versions else None
        if not version_id:
            version_id = create_empty_data(c)  # この関数で新しい空のバージョンを作成
        c.execute(
            'SELECT DISTINCT canvas_elements.version_id, title FROM canvas_elements JOIN canvas_versions ON canvas_elements.version_id = canvas_versions.version_id')
        versions_with_title = c.fetchall()

        # data を canvas_data という辞書に変換
        canvas_data = {item[0]: item[1] for item in data}
        conn.close()
        # return render_template('index.html', data=data)
        if before_version_id is None:
            before_version_id = version_id
        return render_template('cambus.html', canvas_data=canvas_data, versions=versions_with_title, title=title, comment=comment, version_id=version_id, before_version_id=before_version_id)
    return render_template('index.html', db_files=db_files)

@app.route('/edit/<version_id>', methods=['GET', 'POST'])
def edit(version_id=None):
    db_name = session.get('db_name', 'default.db')
    db_name = "database/" + db_name
    if request.method == 'POST':
        # データベースにデータを保存する
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        for key in request.form.keys():
            c.execute('UPDATE canvas_elements SET content=? WHERE name=?', (request.form[key], key))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        # 編集画面を表示する
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('''
            SELECT 
                canvas_categories.category_name, 
                canvas_elements.content,
                canvas_versions.title,
                canvas_versions.comment
            FROM canvas_elements
            JOIN canvas_categories ON canvas_elements.category_id = canvas_categories.id
            LEFT JOIN canvas_versions ON canvas_elements.version_id = canvas_versions.version_id
            WHERE canvas_elements.version_id = ?
        ''', (version_id,))
        data = c.fetchall()
        canvas_data = {item[0]: item[1] for item in data}
        title = data[0][2] if data else None
        comment = data[0][3] if data else None
        conn.close()
        return render_template('edit.html', canvas_data=canvas_data,title=title, comment=comment, version_id=version_id)


@app.route('/save', methods=['POST'])
def save():
    db_name = session.get('db_name', 'default.db')
    db_name ="database/" + db_name
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
        title = request.form.get('title')
        comment = request.form.get('comment')
        # 現在の日時を取得
        now = datetime.now()

        # yyyymmddHHMMSS の形式に変換
        version_id = now.strftime('%Y%m%d%H%M%S')

        # データベースに接続
        conn = sqlite3.connect(db_name)
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
        c.execute('''
            INSERT INTO canvas_versions (version_id, title, comment) 
            VALUES (?, ?, ?)
        ''', (version_id, title, comment))
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


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    db_name = session.get('db_name', 'default.db')
    db_name = "database/" + db_name
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    if request.method == 'POST':
        versions_to_delete = request.form.getlist('delete_versions')
        for version in versions_to_delete:
            c.execute('DELETE FROM canvas_elements WHERE version_id=?', (version,))
            c.execute('DELETE FROM canvas_versions WHERE version_id=?', (version,))
        conn.commit()
        return redirect(url_for('index'))

    c.execute('SELECT DISTINCT canvas_elements.version_id, title FROM canvas_elements JOIN canvas_versions ON canvas_elements.version_id = canvas_versions.version_id')
    versions = c.fetchall()

    c.execute('SELECT MAX(version_id) FROM canvas_elements')
    version_id = c.fetchone()[0]
    conn.close()
    return render_template('delete.html', versions=versions, version_id=version_id)


def create_empty_data(c):
    # 新しいデータベースに初期データを挿入
    version_id = datetime.now().strftime('%Y%m%d%H%M%S')
    categories = [
        'key_activity', 'customer_relationship', 'key_partners',
        'value_proposition', 'customer_segment', 'key_resources',
        'channel', 'cost_structure', 'revenue_streams'
    ]
    for idx, category in enumerate(categories, 1):
        c.execute('''
            INSERT INTO canvas_elements (version_id, category_id, content) 
            VALUES (?, ?, ?)
        ''', (version_id, idx, ""))

    c.execute('''
        INSERT INTO canvas_versions (version_id, title, comment) 
        VALUES (?, ?, ?)
    ''', (version_id, "", ""))
    return version_id


@app.route('/create_database', methods=['GET', 'POST'])
def create_database():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        print("db1")
        if db_name:
            print("db2")
            # .db 拡張子がなければ追加
            if not db_name.endswith('.db'):
                db_name += '.db'
            db_path = os.path.join('database', db_name)
            print("db3", db_path)
            if not os.path.exists(db_path):
                print("db4", db_path)
                conn = sqlite3.connect(db_path)
                c = conn.cursor()

                # canvas_versionsのテーブルを作成
                c.execute('''
                    CREATE TABLE IF NOT EXISTS canvas_versions (
                        version_id INTEGER PRIMARY KEY,
                        title TEXT,
                        comment TEXT
                    )
                ''')

                # canvas_categoriesのテーブルを作成
                c.execute('''
                    CREATE TABLE IF NOT EXISTS canvas_categories (
                        id INTEGER PRIMARY KEY,
                        category_name TEXT NOT NULL UNIQUE
                    )
                ''')

                # canvas_elementsのテーブルを作成
                c.execute('''
                    CREATE TABLE IF NOT EXISTS canvas_elements (
                        id INTEGER PRIMARY KEY,
                        version_id TEXT NOT NULL,
                        category_id INTEGER,
                        content TEXT NOT NULL,
                        FOREIGN KEY(category_id) REFERENCES canvas_categories(id)
                    )
                ''')

                # canvas_categoriesにデフォルトのカテゴリを追加
                default_categories = [
                    "key_activity", "customer_relationship", "key_partners",
                    "value_proposition", "customer_segment", "key_resources",
                    "channel", "cost_structure", "revenue_streams"
                ]

                for category in default_categories:
                    try:
                        c.execute("INSERT INTO canvas_categories (category_name) VALUES (?)", (category,))
                    except sqlite3.IntegrityError:
                        # カテゴリがすでに存在する場合は追加しない
                        pass
                create_empty_data(c)

                conn.commit()
                conn.close()
                flash('Database created successfully!', 'success')
            else:
                flash('Database already exists.', 'danger')
            return redirect(url_for('index'))
    return render_template('create_db.html')


if __name__ == '__main__':
    app.run(debug=True)