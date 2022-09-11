import sqlite3

file_name = "economy.db"


# shop_items = [
#     {"name": "watch", "cost": 100, "id": 1, "info": "It's a watch"},
#     {"name": "mobile", "cost": 1000, "id": 2, "info": "It's a mobile"},
#     {"name": "laptop", "cost": 10000, "id": 3, "info": "It's a laptop"}
#     # You can add your items here ...
# ]
# rshop = {
#     #TODO   alt + shift + up/down arrow
#     "watch" : {"cost":100 , "key":1 , "info":"It's a watch"},
#     "airpods" : {"cost":400 , "key":4 , "info":"They are airpods"},
#     "mobile" : {"cost":1000 , "key":2 , "info":"It's a mobile"},
#     "laptop" : {"cost":10000 , "key":3 , "info":"It's a laptop"}
# }



def hi():
    print("working")

def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)


def createTableifnotExists():
    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cols = ["wallet", "bank", "inventory"] # You can add as many as columns in this !!!
    cursor.execute("""CREATE TABLE IF NOT EXISTS economy(userID BIGINT)""")
    db.commit()
    try:
        for col in cols:
            typE = "BIGINT" if col != "inventory" else "TINYTEXT"
            cursor.execute(f"ALTER TABLE economy ADD COLUMN {col} {typE}")
        db.commit()
        cursor.close()
        db.close()
        print("Table created successfully !")
    except Exception as e:
        print(e)

async def open_bank(user):
    createTableifnotExists()
    columns = ["wallet", "bank","inventory"] # You can add more Columns in it !

    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO economy(userID) VALUES({user.id})")
        db.commit()
        for name in columns:
            empt=dict()

            cursor.execute(f"UPDATE economy SET {name} = 0 WHERE userID = {user.id}")
        db.commit()
        cursor.execute(f"UPDATE economy SET wallet = 5000 WHERE userID = {user.id}")
        db.commit()
    cursor.close()
    db.close()


async def get_bank_data(user):

    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    users = cursor.fetchone()
    cursor.close()
    db.close()
    return users


async def update_bank(user, amount=0, mode="wallet"):

    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    data = cursor.fetchone()
    if data is not None:
        cursor.execute(f"UPDATE economy SET {mode} = {mode} + {amount} WHERE userID = {user.id}")
        db.commit()
    cursor.execute(f"SELECT {mode} FROM economy WHERE userID = {user.id}")
    users = cursor.fetchone()
    cursor.close()
    db.close()
    return users


async def get_lb():

    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute("SELECT userID, wallet + bank FROM economy ORDER BY wallet + bank DESC")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return users

