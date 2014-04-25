# create the database 'images.sqlite' and create a table 'image_store' inside
# of it.

import sqlite3
import sys

def create():
    db = sqlite3.connect('images.sqlite')
    db.execute('CREATE TABLE image_store (i INTEGER PRIMARY KEY, image BLOB, description TEXT, file_name TEXT, user TEXT)')
    db.execute('CREATE TABLE users_store (i INTEGER PRIMARY KEY, user TEXT, password TEXT)')
    db.commit()
    db.close()

    # here, the database is images.sqlite; it contains one table, image_store;
    # 'i' is a column that provides a unique key for retrieval (and is optimized
    #   for that; 'image_store' is another column that contains large binary
    #   objects (blobs).

def insert(image_data):
    # connect to the already existing database
    db = sqlite3.connect('images.sqlite')

    # configure to allow binary insertions
    db.text_factory = bytes
    c = db.cursor()

    # insert!
    c.execute('INSERT INTO image_store (image, description, file_name, user) VALUES (?,?,?,?)', (image_data["data"],image_data["description"], image_data["file_name"], image_data["user"]))
    db.commit()
    db.close()

def create_user(username, password):
    # connect to the already existing database
    db = sqlite3.connect('images.sqlite')

    # configure to allow binary insertions
    db.text_factory = bytes
    c = db.cursor()

    # insert!
    c.execute('INSERT OR REPLACE INTO users_store (user, password) VALUES (?,?)', (username, password))
    db.commit()
    db.close()

def authenticate(username, password):
    # connect to database
    db = sqlite3.connect('images.sqlite')

    # configure to retrieve bytes, not text
    db.text_factory = bytes

    # get a query handle (or "cursor")
    c = db.cursor()

    # select all of the images
    c.execute('SELECT * FROM users_store WHERE user=?', (username, ))

    # grab the first result (this will fail if no results!)
    user_item = c.fetchone()
    pass_db = None;
    if user_item:
        pass_db = user_item[2]
        if password == pass_db:
            return True

    return False

def update(img):
    # connect to the already existing database
    db = sqlite3.connect('images.sqlite')

    # configure to allow binary insertions
    db.text_factory = bytes
    c = db.cursor()

    c.execute('INSERT OR REPLACE INTO image_store (image, description, file_name, user) VALUES (?,?,?,?)', (img["data"],img["description"], img["file_name"], img["user"]))

    db.commit()
    db.close()

def retrieve(image_name):
    # connect to database
    db = sqlite3.connect('images.sqlite')

    # configure to retrieve bytes, not text
    db.text_factory = bytes

    # get a query handle (or "cursor")
    c = db.cursor()

    # select all of the images
    c.execute('SELECT i, image FROM image_store ORDER BY i DESC LIMIT 1')
    #          ^      ^             ^           ^
    #          ^      ^             ^           ^----- details of ordering/limits
    #          ^      ^             ^
    #          ^      ^             ^--- table from which you want to extract
    #          ^      ^
    #          ^      ^---- choose the columns that you want to extract
    #          ^
    #          ^----- pick zero or more rows from the database


    # grab the first result (this will fail if no results!)
    i, image = c.fetchone()

    # write 'image' data out to sys.argv[1]
    print 'writing image', i
    open(image_name, 'w').write(image)

def load_all_images():
    # connect to database
    db = sqlite3.connect('images.sqlite')

    # configure to retrieve bytes, not text
    db.text_factory = bytes

    # get a query handle (or "cursor")
    c = db.cursor()

    imageList = []
    for row in c.execute('SELECT * FROM image_store'):
        imgForm = {}
        imgForm["data"] = row[1]
        imgForm["description"] = row[2]
        imgForm["file_name"] = row[3]
        imgForm["user"] = row[4]
        imageList.append(imgForm)

    db.commit()
    db.close()

    print 'imageList length: ', len(imageList)

    return imageList

def delete_image(file_name):
    db = sqlite3.connect('images.sqlite')
    db.execute('DELETE FROM image_store WHERE file_name=(?)', (file_name,))
    db.commit()
