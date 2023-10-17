import sqlite3

# データベースをセットアップ
def setup_db():
    with sqlite3.connect("business_model_canvas.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS canvas_elements (
                id TEXT PRIMARY KEY,
                content TEXT
            )
        """)
        conn.commit()

# ユーザーに要素を入力させる
def input_elements():
    ids = [
        "key_partners_1", "key_partners_2", "key_partners_3", "key_partners_4",
        # 他の要素のIDもリストに追加
        # "key_activity_1", "key_activity_2", ...
    ]
    
    for element_id in ids:
        content = input(f"Enter content for {element_id}: ")
        with sqlite3.connect("business_model_canvas.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO canvas_elements (id, content) VALUES (?, ?)", (element_id, content))
            conn.commit()

setup_db()
input_elements()
