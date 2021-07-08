# importing Library
import xml.etree.ElementTree as ET
import sqlite3

# make a database and cursor
con = sqlite3.connect('iTunesTrack.sqlite')
cur = con.cursor()

# always make new tables
cur.executescript('''
DROP TABLE IF EXISTS Artist ;
DROP TABLE IF EXISTS Album ;
DROP TABLE IF EXISTS Track ;

CREATE TABLE Artist(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE
);

CREATE TABLE Track(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    length INTEGER,
    rating INTEGER,
    count INTEGER
);
''')
# end of table CREATE in database

# taking xml file of Tracks
file = input("Enter file: ")
# set default file
if len(file) < 1 :
    file = 'Library.xml'

# local function for tey val check
def lookup(d, key):
    # a flag
    found = False
    # iterate thorugh each dict in file
    for child in d :
        if found :
            # return the text for key
            return child.text
        # if found
        if child.tag == 'key' and child.text == key :
            found = True
    # if not then
    return None

# handle for xml file
fh = ET.parse(file)

# create a list of all dict in file
lst = fh.findall('dict/dict/dict')

# how many dict found message
print('Dict Count: ', len(lst))

# loop for all dict in xml file
for line in lst :
    # to check if dict contant track id
    if (lookup(line, 'Track ID') is None) :
        continue

    # getting all the data for a track
    name = lookup(line, 'Name')
    artist = lookup(line, 'Artist')
    album = lookup(line, 'Album')
    count = lookup(line, 'Play Count')
    rating = lookup(line, 'Rating')
    length = lookup(line, 'Total Time')

    # if main info is None
    if name is None or artist is None or album is None :
        continue # Skip

    # if get all then print
    print('Sound: ', name, artist, album, count, rating, length)

    # command database for INSERT
    # insert unique artist or IGNORE of repeated
    cur.execute('''
    INSERT OR IGNORE INTO Artist (name) VALUES ( ? )''',
    (artist,))
    # get unique artist_id
    cur.execute('''
    SELECT id FROM Artist WHERE name = ? ''',
    (artist,))
    artist_id = cur.fetchone()[0]

    # insert unique album or IGNORE of repeated
    cur.execute('''
    INSERT OR IGNORE INTO Album (title, artist_id) VALUES ( ?, ? )''',
    (album, artist_id))
    # get unique album_id
    cur.execute('''
    SELECT id FROM Album WHERE title = ? ''',
    (album,))
    album_id = cur.fetchone()[0]

    # insert unique Track or REPLACE of repeated
    cur.execute('''
    INSERT OR REPLACE INTO Track
    (title, album_id, count, rating, length)
    VALUES ( ?, ?, ?, ?, ?)''',
    (name, album_id, count, rating, length))

    # store in database
    con.commit()

# close the path to file
cur.close()

# all done :)
