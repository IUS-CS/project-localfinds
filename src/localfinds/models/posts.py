import sqlite3

def initialize_posts(posts):
    conn = sqlite3.connect(posts)
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


def store_post(posts, subject, content, author_id, address, tags=None):
    conn = sqlite3.connect(posts)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO posts (subject, content, author_id, address, tags)
        VALUES (?, ?, ?, ?, ?)
    """, (subject, content, author_id, address, tags))

    conn.commit()
    conn.close()


def get_post(posts, post_id):
    conn = sqlite3.connect(posts)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    
    conn.close()
    return dict(post) if post else None


def get_all_posts(posts):
    conn = sqlite3.connect(posts)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts ORDER BY updated_at DESC")
    posts = cursor.fetchall()

    conn.close()
    return [dict(post) for post in posts]


def update_post(posts, post_id, subject, content, address, tags=None):
    conn = sqlite3.connect(posts)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE posts
        SET subject = ?, content = ?, tags = ?, address = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (subject, content, tags, address, post_id))

    conn.commit()
    conn.close()

def update_all_posts_author(posts, old_author, new_author):
    conn = sqlite3.connect(posts)
    cursor = conn.cursor()

    cursor.execute("""
            UPDATE posts
            SET author_id = ?
            WHERE author_id = ?
        """, (new_author, old_author))

    conn.commit()
    conn.close()


def delete_post(posts, post_id):
    conn = sqlite3.connect(posts)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))

    conn.commit()
    conn.close()

def delete_all_posts_by_author(posts, author_id):
    conn = sqlite3.connect(posts)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts WHERE author_id = ?", (author_id,))

    conn.commit()
    conn.close()

def clear_posts(posts):
    conn = sqlite3.connect(posts)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts")

    conn.commit()
    conn.close()
