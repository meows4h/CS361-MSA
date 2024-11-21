import zmq
import mysql.connector
from mysql.connector import Error

# server : classmysql.engr.oregonstate.edu
# user : cs361_beecheco
# pass : zV6pVrlDQOXq

# mysql connection
connection = None
try:
    connection = mysql.connector.connect(
        host='classmysql.engr.oregonstate.edu',
        user='cs361_beecheco',
        passwd='zV6pVrlDQOXq'
    )
    print('Connection to database successful.')

except Error as e:
    print(f'The error "{e}" occurred')
    quit()

# create an account
def create_account(username, password):
    cursor = connection.cursor()

    query = f"""
    INSERT INTO 
      `accounts` (`username`, `password`)
    VALUES  
      ('{username}', '{password})
    """

    try:
        cursor.execute(query)
        connection.commit()
        return f"Successfully created an account (username: {username}; password: {password})"
    
    except Error as e:
        return f"The error '{e}' occurred"
    
# edit an account
def edit_account(userid, username, password):
    cursor = connection.cursor()

    query = f"""
    UPDATE
      `accounts`
    SET  
      username = '{username}', password = '{password}'
    WHERE
      id = {userid}
    """

    try:
        cursor.execute(query)
        connection.commit()
        return f"Successfully edited an account (id: {userid}; username: {username}; password: {password})"
    
    except Error as e:
        return f"The error '{e}' occurred"

# delete an account
def delete_account(userid):
    cursor = connection.cursor()

    query = f"""
    DELETE FROM
      `accounts`
    WHERE
      id = {userid}
    """

    try:
        cursor.execute(query)
        connection.commit()
        return f"Successfully deleted an account (id: {userid})"
    
    except Error as e:
        return f"The error '{e}' occurred"
    
# search & validate an account
def search_account(username, password):

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

create_users = """
INSERT INTO
  `users` (`name`, `age`, `gender`, `nationality`)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');
"""

# zeromq
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:13762')

while True:
    
    reply = ''

    message = socket.recv()
    message = message.decode('utf-8')
    print(f'Received request: "{message}"')

    message_arr = message.split(' ')
    if len(message_arr) >= 3:
        request = message_arr[0]
        username = message_arr[1]
        password = message_arr[2]

        # ex: 'create [username] [password]'
        # return if available: '201 Created: [username] [password] [id]'
        # return if not available: '409 Conflict: [username] not available'
        if request == 'create':

            account_check = False # if true: username taken

            if account_check:
                reply = f'409 Conflict: {username} not available'
            else:
                reply = f'201 Created: {username} {password}'

        # ex: 'delete [username] [password]'
        # return if found: '200 OK: Deleted [username] [id]'
        # return if not found: '404 Not Found: [username]'
        elif request == 'delete':

            reply = f'200 OK: Deleted {username}'
            reply = f'404 Not Found: {username}'

        # ex: 'search [username] [password]'
        # return if found: '200 OK: [id]'
        # return if not found: '404 Not Found: [username] [password]'
        elif request == 'search':

            reply = f'200 OK: [id]'
            reply = f'404 Not Found: {username} {password}'

    # ex: missing components or not enough queries, or other problems
    # return: '400 Bad Request'
    else:
        reply = '400 Bad Request'

    socket.send(reply)