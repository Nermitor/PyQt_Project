"""Служебный файл, производит очистку данных. При запуске очищает всё."""

import glob
import os
import sqlite3 as sql


def clean_temp_folder():
    """Очищает папку temp"""
    for f in glob.glob(r"pictures\temp\*.png"):
        os.remove(f)


def clean_best_folder():
    """Очищает папку best"""
    for f in glob.glob(r"pictures\best\*.png"):
        os.remove(f)


def clean_db():
    """Очищает базу данных"""
    con = sql.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("""
        delete from users where TRUE
    """)
    cur.execute("""
        delete from score where TRUE
    """)
    cur.execute("""
        delete from best_pictures where TRUE
    """)
    con.commit()


def clean_all():
    clean_db()
    clean_best_folder()
    clean_temp_folder()


if __name__ == '__main__':
    clean_all()
