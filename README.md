# User Account SQL Database Microservice

## Overview
This is a microservice for an account storage system, built using Python, ZeroMQ, and the MySQL connector for connecting to a SQL database.

- main.py : The microservice itself
- test.py : Test program to prove it can receive and return calls
- requirements.txt : The required Python libraries to run 'main.py'

## UML Sequence Diagram
![UML Sequence Diagram](https://github.com/meows4h/CS361-MSA/blob/main/images/UMLDiagram.PNG)

## Example Calls
Requests and responses to the service include:

### Create
- Requests
    - create {username} {password}
- Responses
    - On success: Created account (username: {username}; password: {password})
    - On failure: It will hand back the SQL server error if there is a problem with the query

### Edit
- Requests
    - edit {parameter} {userid} [{username} || {password}] (overall usage)
    - edit username {userid} {username}
    - edit password {userid} {password}
    - edit both {userid} {username} {password}
- Responses
    - On success: Edited account (id: {userid}; username: {username}; password {password})
    - On failure: It will hand back the SQL server error if there is a problem with the query

### Search
- Requests
    - search {username} {password}
- Responses
    - On success: Found account with id: {userid}
    - On failing to find user: No account found
    - On query failure: It will hand back the SQL server error if there is a problem with the query

### Delete
- Requests
    - delete {userid}
- Responses
    - On success: Deleted account (id: {userid})
    - On failure: It will hand back the SQL server error if there is a problem with the query

### Additional Responses & Information
It may generate a response saying "Invalid syntax (too many/few values; incorrect command)" in the case of there being a space located in the call, everything should be contained within the format listed without additional spaces.

## Setup
If you need to use this on your own, there is a section at the top of 'main.py' where you can change the SQL server, username, password, and database name to connect to your own service and such. Additionally, there is a port variable to change to have more control over the socket connection.

Use the following to install the required libraries:
````
pip install requirements.txt
````
