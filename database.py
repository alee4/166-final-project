import sqlite3
import hashlib
import random
import string
from base64 import b64encode
import os # << hint
from datetime import datetime
def create_db():
    """ Create table 'userDatas' in 'userData' database """
    try:
        conn = sqlite3.connect('userData.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE userDatas
                    (
                    userName text,
                    password text,
                    accessLevel text
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def addUser(newUserName, newPassword):
    """ Example data insert into plants table """
    #newUserName = str(input("Please create a new user name: "))  # Need exception handling
    # newUserName = enterUserName()
    #
    # # newPassword = str(input("Please create a new password: "))  # Need to create valid input check
    # newPassword = enterPassword()

    hashedPW = hash_pw(newPassword)

    #DEFAULT SETS TO 1
    #todo change to other numbers for initialization
    privalege = 1

    data_to_insert = [(newUserName, hashedPW, privalege)]
    try:
        conn = sqlite3.connect('userData.db')
        c = conn.cursor()
        c.executemany("INSERT INTO userDatas VALUES (?, ?, ?)", data_to_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Success")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def query_db():
    """ Display all records in the userData table """
    try:
        conn = sqlite3.connect('userData.db')
        c = conn.cursor()
        for row in c.execute("SELECT * FROM userDatas"):
            print(row)
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def enterUserName():
    newUserName = str(input("Please create a new user name: "))
    # can be anything looks like
    return newUserName

def enterPassword():
    # pass must
    newPassword = str(input("Please create a new password: "))  # Need to create valid input check

    return newPassword

#
# create_db()  # Run create_db function first time to create the database
# addUser()  # Add a plant to the database (calling multiple times will add additional plants)
query_db()  # View all data stored in the


def authenticate(stored, plain_text, salt_length=None) -> bool:
    """
    Authenticate by comparing stored and new hashes.

    :param stored: str (salt + hash retrieved from database)
    :param plain_text: str (user-supplied password)
    :param salt_length: int
    :return: bool
    """
    #salt_length = salt_length or 40  # set salt_length


    salt = stored[:salt_length]  # extract salt from stored value
    stored_hash = stored[salt_length:]  # extract hash from stored value

    print("salt: " + salt)
    print("stroed hash: " + stored_hash)

    hashable = salt + plain_text  # concatenate hash and plain text

    print("hashable: " + hashable)

    hashable = hashable.encode('utf-8')  # convert to bytes
    this_hash = hashlib.sha256(hashable).hexdigest()  # hash and digest
    print("this_Hash = " + this_hash)
    print("stored hash = " + stored_hash)
    return this_hash == stored_hash  # compare

def hash_pw(plain_text, salt='') -> str:

    randomThing = os.urandom(40)
    salt = b64encode(randomThing).decode('utf-8')

    hashable = salt + plain_text  # concatenate salt and plain_text

    print("hahsable in hash_pw: " + hashable)
    hashable = hashable.encode('utf-8')  # convert to bytes

    this_hash = hashlib.sha256(hashable).hexdigest()  # hash w/ SHA-256 and hexdigest
    return salt + this_hash  # prepend hash and return

# generate pass with at least one upper, one lower, one number, and one special char
def getRandomPassword(length):
    sampleSpecialChars = '?!#$%&*'

    random_source = string.ascii_letters + string.digits + sampleSpecialChars
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice(sampleSpecialChars)

    for i in range(length):
        password += random.choice(random_source)

    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    # print("randomm pass" + password)
    return password