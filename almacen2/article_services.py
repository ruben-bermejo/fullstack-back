import sqlite3

def connect_to_database():
    connection = sqlite3.connect("almacen.db")
    return connection

def receive_article(article_id, units_received):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT units, available FROM articles WHERE id=?", (article_id,))
    article = cursor.fetchone()
    units = article[0] + units_received
    available = True
    cursor.execute("UPDATE articles SET units=?, available=? WHERE id=?", (units, available, article_id))
    conn.commit()
    print("Article updated successfully")

def send_article(article_id, units_sent):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT units, available FROM articles WHERE id=?", (article_id,))
    article = cursor.fetchone()
    units = article[0] - units_sent
    if units <= 0:
        units = 0
        available = False
    else:
        available = True
    cursor.execute("UPDATE articles SET units=?, available=? WHERE id=?", (units, available, article_id))
    conn.commit()
    print("Article updated successfully")
