from requests import get
import sqlite3
def insert_character(conn, name, element_type,weapon_type, data):
    print('insert:',name)
    sql = '''INSERT INTO base_character(name,type,weapon_type,data)
             VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (name,element_type,weapon_type,data))
    conn.commit()
    return cur.lastrowid

characters = get("https://genshin-db-api.vercel.app/api/v5/characters?query=names&matchCategories=true").json()

with sqlite3.connect('db.sqlite3') as conn:
    conn.execute("DELETE FROM `base_character`") # THIS DELETE EVERYTHINK IN base_character !!!
    
    for character in characters:
        r = get(f"https://genshin-db-api.vercel.app/api/v5/characters?query={character}")
        insert_character(conn,character,r.json()['elementType'],r.json()['weaponType'],r.text)

