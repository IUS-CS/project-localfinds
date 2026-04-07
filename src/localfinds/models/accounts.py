import sqlite3

def initialize_accounts(accounts):
    conn = sqlite3.connect(accounts)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            joined DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def store_account(accounts, username, password):
    conn = sqlite3.connect(accounts)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO accounts (username, password)
            VALUES (?, ?)
        """, (username, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        # Duplicate username
        success = False

    conn.close()
    return success


def get_account(accounts, account_id):
    conn = sqlite3.connect(accounts)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    account = cursor.fetchone()
    
    conn.close()
    return dict(account) if account else None

def get_account_by_username(accounts, username):
    conn = sqlite3.connect(accounts)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM accounts WHERE username = ?",
        (username,)
    )

    account = cursor.fetchone()
    conn.close()
    return dict(account) if account else None

def get_all_accounts(accounts):
    conn = sqlite3.connect(accounts)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts ORDER BY joined")
    accounts = cursor.fetchall()

    conn.close()
    return [dict(account) for account in accounts]

def update_account(accounts, account_id, username, password):
    conn = sqlite3.connect(accounts)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE accounts
        SET username = ?, password = ?
        WHERE id = ?
    """, (username, password, account_id))

    conn.commit()
    conn.close()


def delete_account(accounts, account_id):
    conn = sqlite3.connect(accounts)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))

    conn.commit()
    conn.close()

def clear_accounts(accounts):
    conn = sqlite3.connect(accounts)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM accounts")

    conn.commit()
    conn.close()
