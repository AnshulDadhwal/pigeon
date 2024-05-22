# description

this will hold all the code for the client side subsystem

# installing

`poetry install`

# running

`poetry run python client/__init__.py`

# components
- database module
- encryption & decryption module
- gui module
- sending & recieving of messages module
- Dockerfile

# technonologies
- poetry for dependency management
- docker for easy deployability
- SQLite for database because its also easy
- SQLAlchemy because no one likes writing SQL. and so we can easily change databases if we need to later
- browser based UI because its easy
- potentially multithreading for asynchronous sending and recieving??

# how it can work

1. the first time a user runs the application, they are assigned a randomly generated UUID. this can just be written in plaintext to a file. there is no changing this or logging in and out
2. they can switch between contacts/chats. they only recieving messages for the chat they are currently viewing - there is no notifications.
3. when viewing a chat, there are two threads running - one to send messages and the other recieving messages
