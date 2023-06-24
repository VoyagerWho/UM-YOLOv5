import os
import sqlite3
import shutil


DEST_PATH = "dest/"
TRAIN_LIMIT = 1000
TEST_LIMIT = 500

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

def fun(path):
    if path.startswith(DEST_PATH):
        return
    if not path.endswith(".jpg"):
        return
    cursor.execute("INSERT INTO files VALUES (?, ?)", [os.path.basename(path), os.path.dirname(path)+'/'])
    

def search_path(start_path):
    for root, dirs, files in os.walk(start_path):
        for name in files:
            file_path = os.path.join(root, name)
            fun(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            fun(dir_path)


cursor.execute("CREATE TABLE files (filename TEXT, path TEXT)")
shutil.rmtree(DEST_PATH, True)
search_path('.') 
connection.commit()

os.makedirs(DEST_PATH)
cursor.execute("SELECT DISTINCT path FROM files ORDER BY LENGTH(path)")
for path, in cursor:
    os.makedirs(DEST_PATH + path)
    
cursor1 = connection.cursor()
cursor2 = connection.cursor()
cursor3 = connection.cursor()
cursor1.execute("SELECT DISTINCT path FROM files ORDER BY LENGTH(path)")
for path, in cursor1:
    cursor2.execute("SELECT DISTINCT LENGTH(filename) FROM files WHERE path = ? ORDER BY LENGTH(filename)", [path])
    for length, in cursor2:
        limit = TRAIN_LIMIT if "train" in path else TEST_LIMIT
        cursor3.execute("SELECT filename FROM files WHERE path = ? AND LENGTH(filename) = ? ORDER BY RANDOM() LIMIT ?", [path, length, limit])
        for filename, in cursor3:
            shutil.copyfile(path + filename, DEST_PATH + path + filename)
            

