import zmq
import mysql.connector
from mysql.connector import Error

# MySQL Setup
server = 'example.server.net'
user_login = 'my_username'
password = 'my_password'
db_name = 'my_database'

# ZeroMQ Setup
port = "13760" # example port



# mysql connection
connection = None
try:
    connection = mysql.connector.connect(
        host=server,
        user=user_login,
        passwd=password,
        database=db_name
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
      ('{username}', '{password}')
    """

    print(query)

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

    print(query)

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

    print(query)

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
      id
    FROM
      `accounts`
    WHERE
      username = '{username}'
    AND
      password = '{password}'
    """

    print(query)

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        if len(results) == 0:
            return "No account found"
        else:
            results = results[0][0]

        return f"Found account with id: {results}"
    
    except Error as e:
        return f"The error '{e}' occurred"

# zeromq
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f'tcp://*:{port}')
print("Connected to socket.")

# general socket loop
while True:
    
    reply = ''

    message = socket.recv()
    message = message.decode('utf-8')
    print(f'Received request: "{message}"')

    # splitting it into seperate arguments to be read
    message_arr = message.split(' ')

    # create & search
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

        else:  
          reply = "Invalid syntax (incorrect command)"

    # delete
    elif len(message_arr) == 2:
        request = message_arr[0]
        userid = message_arr[1]

        # ex: 'delete [userid]'
        if request == 'delete':
            reply = delete_account(userid)

        else:
            reply = "Invalid syntax (too few values / incorrect command)" 

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

        else:
            reply = "Invalid syntax (too many values / incorrect command)" 

    # ex: missing components or not enough queries, or other problems
    # return: 'Bad Request'
    else:
        reply = 'Bad Request'

    # sends the reply off
    reply = reply.encode('utf-8')
    socket.send(reply)