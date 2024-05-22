## this is only temporary until we have a frontend
import encryption
from networking import server_messages
import threading
import uuid
import os
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

# Load the models
from models import db
from models.mesages import Message
from models.users import Users

OPTIONS = """Options:
\list           list pigeon contacts
\select <id>    select contact with <id> to message
\\add <id>      invite a pigeon user with <id> to be a contact
\options        print these options
Anything entered besides the above will be considered a message and will be sent."""
BAD_CMD = 'Invalid command.'
NO_SELECT = 'No contact selected.'


def select_contact(session, user_id, contact_id):
    """
    TODO: Return the chat history of the selected contact in order of sent and recieved datetimes
    """
    sent_list = session.query(Message).filter(Message.sender==user_id, Message.recipient==contact_id).all()
    recieved_list = session.query(Message).filter(Message.sender==contact_id, Message.recipient==user_id).all()

    all_sorted = [d.to_dict() for d in sent_list + recieved_list]
    all_sorted = sorted(all_sorted, key=lambda x: x['mid'])

    return all_sorted

def add_contact(session, contact_id):
    """
    for now, just add id to database
    TODO: later implement invite functionality
    """
    new_contact = Users(uid=contact_id)
    # print(new_contact)
    session.add(new_contact)
    session.commit()

def view_contacts(session):
    """
    Return a list of all contacts
    """
    contacts = session.query(Users).all()
    # print(contacts)

    return contacts

def send(session, user_id, reciever_id, message):
    """
    encrypt the selected message
    store message in the database
    send message to server
    """

    # TODO: encrypt message

    time = datetime.now()
    str_time = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    # construct json body
    msg_json = {
        'meta': {
            'to': reciever_id,
            'from': user_id,
            'datetime': str_time,
        },
        'message': message
    }

    # add message to db
    new_message = Message(created_at=time,
                            sender=user_id,
                            recipient=reciever_id,
                            message=message)
    session.add(new_message)
    session.commit()

    server_messages.send_message(user_id, msg_json, reciever_id)

def recieve(session, user_id, sender_id):
    """
    poll server for new messages
    store new messages in the database
    decrypt the new messages for the selected contact
    return the list of decrypted new messages
    """
    new_msgs = server_messages.recieve_messages(user_id)
    sender_msgs = []
    for msg in new_msgs:
        # if message is from contact, collect them all
        if msg.get('from') == sender_id:
            sender_msgs.append(msg)

        # add message to db
        new_message = Message(created_at=msg.get('sent_at'),
                                sender=msg.get('from_addr'),
                                recipient=msg.get('to_addr'),
                                message=datetime.fromisoformat(msg.get('message')))
        session.add(new_message)
        session.commit()

    # TODO: decrypt all messages in sender_msgs
    # sender_msgs_decrypt = []

    return sender_msgs

def recieving_thread(session, pigeon_id):
    print(random.randint(1,99))
    return
    new_msgs = server_messages.recieve_messages(pigeon_id)
    for msg in new_msgs:
        new_message = Message(created_at=msg.get('sent_at'),
                        sender=msg.get('from_addr'),
                        recipient=msg.get('to_addr'),
                        message=datetime.fromisoformat(msg.get('message')))
        session.add(new_message)
        session.commit()



def input_thread(quitEvent, user):
    """
    The input thread for the client, constantly takes in user input
    from stdin and sends it to the server.
    Status: Given
    Args:
        quitEvent (threading.Event): Event on which the user must exit.
        user (User): the user object used by this chatclient.
    """
    while not quitEvent.is_set():
        try:
            message = input().strip()
        except EOFError:
            continue
        if not user.send(message):  # ConnectionResetError occured
            quitEvent.set()

def run():

    session = create_db()

    # get user id or generate one
    pigeon_id = ''
    try:
        with open('pigeon_id.txt', 'r') as id:
            pigeon_id = id.readline()
    except:
        with open('pigeon_id.txt', 'w') as id:
            pigeon_id = str(uuid.uuid4())
            id.write(pigeon_id)

    # friend_id = input('Friend ID: ')
    friend_id = None

    print(f'Welcome user {pigeon_id} to Pigeon, the super secret instant messanger!')
    print(OPTIONS)
    print()
    print(NO_SELECT)
    # quitEvent = threading.Event()
    # Initialize and begin reading and writing threads
    # inputThread = threading.Thread(target=input_thread, args=(quitEvent, pigeon_id,))
    # inputThread.daemon = True
    # try:
    #     inputThread.start()
    # except:  # exit if threads can't be created
    #     exit(1)
    
    # # Wait for threads to complete before exiting the program
    # while not quitEvent.is_set():
    #     continue
    # exit(0)  # input thread is daemon and will exit itself

    while True:
        threading.Thread(target=recieving_thread, args=(session, pigeon_id)).start()

        entered = input()

        if entered == '\list':
            contacts = view_contacts(session)
            if not contacts:
                print('You have no contacts')
                print()
                continue
            print('These are your contacts:')
            for c in contacts:
                print(c)
            print()
            continue
        elif entered.startswith('\select'):
            parts = entered.split()
            if len(parts) != 2:
                print(BAD_CMD)
                continue
            friend_id = parts[1]
            print(f'Messaging {friend_id}')
            history = select_contact(session, pigeon_id, friend_id)
            for m in history:
                sender = m['contents']['from']
                at = m['created_at']
                body = m['contents']['message']
                print(f'{sender} [{at}] $ {body}')
            continue
        elif entered.startswith('\\add'):
            parts = entered.split()
            # print(f'adding contact {parts[1]}')
            if len(parts) != 2:
                print(BAD_CMD)
                continue
            add_contact(session, parts[1])
            print(f'Contact {parts[1]} has been added')
            print()
            continue
        elif entered == '\options':
            print()
            print(OPTIONS)
            print()
            continue

        # everything else is considered a message to send
        if not friend_id:
            print(NO_SELECT)
            continue
        else:
            send(session, pigeon_id, friend_id, entered)

        recieved = recieve(session, pigeon_id, friend_id)
        # recieved = []
        
        for msg in recieved:
            print(f"{friend_id} ({msg.get('sent_at')}): " + msg.get('message'))

# TODO: may need to add threading for asynchronous message send and recieve


# def _recieving_thread():
#     pass

# def sending_thread():
#     pass

def create_db(config_overrides=None):

    # engine = create_engine("sqlite:///pigeondb.db", echo=True)
    engine = create_engine("sqlite:///pigeondb.db")

    db.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

if __name__ == '__main__':
    run()