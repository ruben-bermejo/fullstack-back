import sqlite3

def connect_to_database():
    connection = sqlite3.connect("almacen.db")
    return connection

def create_article(article_info, units, available):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO articles (article_info, units, available) VALUES (?, ?, ?)",
                   (article_info, units, available))
    connection.commit()
    connection.close()


def read_all_articles():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM articles")
    article = cursor.fetchall()
    connection.close()
    return article

def read_article(article_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM articles WHERE id=?", (article_id,))
    article = cursor.fetchone()
    connection.close()
    return article    

def update_article(article_id, article_info, units, available):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE articles SET article_info=?, units=?, available=? WHERE id=?",
                   (article_info, units, available, article_id))
    connection.commit()
    connection.close()

def delete_article(article_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM articles WHERE id=?", (article_id,))
    connection.commit()
    connection.close()


