import sqlite3


def insert_result(db, name, score,
                  accuracy):  # Функция, позволяющая внести данные в БД
    if name == '':
        name = 'Player'
    con = sqlite3.connect(db)
    cur = con.cursor()
    sqlite_insert_with_param = """INSERT INTO maintable(NAME, SCORE, ACCURACY) VALUES(?, ?, ?)"""
    data_tuple = (name, score, accuracy)
    cur.execute(sqlite_insert_with_param, data_tuple)
    con.commit()
    con.close()

