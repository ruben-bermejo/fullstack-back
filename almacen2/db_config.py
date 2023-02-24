import sqlite3

def init_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table 'articles' if it doesn't exist
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_info TEXT NOT NULL,
            units INTEGER NOT NULL,
            available BOOLEAN NOT NULL
        );
        '''
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Call `init_db` function with the path to the database file
#init_db("almacen.db")

