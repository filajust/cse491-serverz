# create the database 'images.sqlite' and create a table 'image_store' inside
# of it.

import sqlite3
import sys

def create():
    db = sqlite3.connect('images.sqlite')
    # db.execute('CREATE TABLE image_store (i INTEGER PRIMARY KEY, image BLOB)');
    db.execute('CREATE TABLE image_store (i INTEGER PRIMARY KEY, image BLOB, description TEXT, file_name TEXT)');
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
    # db.execute('INSERT INTO image_store (image) VALUES (?)', (image_data,))
    c.execute('INSERT INTO image_store (image, description, file_name) VALUES (?,?,?)', (image_data["data"],image_data["description"], image_data["file_name"]))
    db.commit()
    db.close()

def update(img):
    # connect to the already existing database
    db = sqlite3.connect('images.sqlite')

    # configure to allow binary insertions
    db.text_factory = bytes
    c = db.cursor()

    c.execute('INSERT OR REPLACE INTO image_store (image, description, file_name) VALUES (?,?,?)', (img["data"],img["description"], img["file_name"]))

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
        imageList.append(imgForm)

    db.commit()
    db.close()

    print 'imageList length: ', len(imageList)

    return imageList
