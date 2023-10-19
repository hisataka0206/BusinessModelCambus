import sqlite3

def init_db(db_name):
    conn = sqlite3.connect(db_name)
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

    conn.commit()
    conn.close()

# 初期データベース作成

if __name__ == '__main__':
    print("データベース名を入力してください")
    db_name = input()
    init_db("database/"+db_name+".db")
