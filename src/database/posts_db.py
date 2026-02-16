import sqlite3

posts_db = "./src/database/posts.db"

def initialize_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id TEXT NOT NULL,
            address TEXT NOT NULL,
            tags TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_post(db_path, subject, content, author_id, address, tags=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO posts (subject, content, author_id, address, tags)
        VALUES (?, ?, ?, ?, ?)
    """, (subject, content, author_id, address, tags))

    conn.commit()
    conn.close()


def get_post(db_path, post_id):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    
    conn.close()
    return dict(post) if post else None


def get_all_posts(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts ORDER BY updated_at DESC")
    posts = cursor.fetchall()

    conn.close()
    return [dict(post) for post in posts]


def update_post(db_path, post_id, subject, content, address, tags=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE posts
        SET subject = ?, content = ?, tags = ?, address = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (subject, content, tags, address, post_id))

    conn.commit()
    conn.close()


def delete_post(db_path, post_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))

    conn.commit()
    conn.close()

def clear_posts(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts")

    conn.commit()
    conn.close()
