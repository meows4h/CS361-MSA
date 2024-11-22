import zmq

context = zmq.Context()

print('Connecting to socket…')
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:13760')

while True:

    selection = 0
    selection = input("""Select what you would like to do:
           1. Create an account
           2. Edit an account
           3. Search for an account
           4. Delete an account\n
          Select one: """)
    
    print("\n")

    selection = int(selection)

    # create
    if selection == 1:

        print("Account Creation")
        username = input("Username: ")
        password = input("Password: ")
        request = f"create {username} {password}"

    # edit
    elif selection == 2:

        print("Account Editing")
        userid = input("Enter the User ID you are editing: ")
        userid = int(userid)

        parameter = input("""What are you editing?
                           1. Username
                           2. Password
                           3. Both\n
                          Select one: """)
        
        parameter = int(parameter)
        
        if parameter == 1:

            parameter = 'username'
            username = input("New Username: ")
            request = f"edit {parameter} {userid} {username}"

        elif parameter == 2:

            parameter = 'password'
            password = input("New Password: ")
            request = f"edit {parameter} {userid} {password}"

        elif parameter == 3:

            parameter = 'both'
            username = input("New Username: ")
            password = input("New Password: ")
            request = f"edit {parameter} {userid} {username} {password}"

    # search
    elif selection == 3:

        print("Account Search")
        username = input("Username: ")
        password = input("Password: ")
        request = f"search {username} {password}"

    # delete
    elif selection == 4:

        print("Account Deletion")
        userid = input("User ID: ")
        userid = int(userid)
        request = f"delete {userid}"

    else:
        print("Incorrect input.")
        request = 'this is an incorrect request'

    print(f'Request: {request}')
    request = request.encode('utf-8')
    socket.send(request)

    # displaying reply
    reply = socket.recv()
    reply = reply.decode('utf-8')
    print(f'Received response: {reply}')