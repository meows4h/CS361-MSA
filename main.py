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
        return f"Created account (username: {username}; password: {password})"
    
    except Error as e:
        return f"The error '{e}' occurred"
    
# edit an account
def edit_account(userid, username='', password=''):
    cursor = connection.cursor()

    query = ''
    reply = ''

    if username == '':
        query = f"""
        UPDATE
          `accounts`
        SET  
          password = '{password}'
        WHERE
          id = {userid}
        """

        reply = f"Edited account (id: {userid}; password: {password})"

    elif password == '':
        query = f"""
        UPDATE
          `accounts`
        SET  
          username = '{username}'
        WHERE
          id = {userid}
        """

        reply = f"Edited account (id: {userid}; username: {username})"

    else:
        query = f"""
        UPDATE
          `accounts`
        SET  
          username = '{username}', password = '{password}'
        WHERE
          id = {userid}
        """

        reply = f"Edited account (id: {userid}; username: {username}; password: {password})"

    try:
        cursor.execute(query)
        connection.commit()
        return reply
    
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
        return f"Deleted account (id: {userid})"
    
    except Error as e:
        return f"The error '{e}' occurred"
    
# search & validate an account
def search_account(username, password):
    cursor = connection.cursor()

    query = f"""
    SELECT
      'id'
    FROM
      `accounts`
    WHERE
      username = '{username}'
    AND
      password = '{password}'
    """

    try:
        cursor.execute(query)
        connection.commit()
        return f"Found account with id: "
    
    except Error as e:
        return f"The error '{e}' occurred"

# zeromq
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:13762')

while True:
    
    reply = ''

    message = socket.recv()
    message = message.decode('utf-8')
    print(f'Received request: "{message}"')

    # create & search
    message_arr = message.split(' ')
    if len(message_arr) == 3:
        request = message_arr[0]
        username = message_arr[1]
        password = message_arr[2]

        # ex: 'create [username] [password]'
        if request == 'create':
          
            reply = create_account(username, password)

        # ex: 'search [username] [password]'
        elif request == 'search':

            reply = search_account(username, password)

    # delete
    elif len(message_arr) == 2:
        request = message_arr[0]
        userid = message_arr[1]

        # ex: 'delete [userid]'
        if request == 'delete':

            reply = delete_account(userid)

    # edit
    elif len(message_arr) >= 4:
        request = message_arr[0]
        parameter = message_arr[1]
        userid = message_arr[2]
        first_input = message_arr[3]

        if len(message_arr) >= 5:
            second_input = message_arr[4]

        # ex: 'edit [param] [userid] ...'
        if request == 'edit':

            # ex: 'edit username [userid] [username]'
            if parameter == 'username':

                reply = edit_account(userid, username=first_input)

            # ex: 'edit username [userid] [password]'
            elif parameter == 'password':

                reply = edit_account(userid, password=first_input)

            # ex: 'edit both [userid] [username] [password]'
            elif parameter == 'both':

                reply = edit_account(userid, first_input, second_input)

    # ex: missing components or not enough queries, or other problems
    # return: '400 Bad Request'
    else:
        reply = '400 Bad Request'

    socket.send(reply)