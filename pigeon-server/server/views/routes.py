from flask import Blueprint, jsonify, request
from server.models import db
from server.models.server import Message, Client_Info
from . import generate_key_pair
import json
from uuid import UUID
from flask_sqlalchemy import SQLAlchemy

api = Blueprint("api", __name__, url_prefix="/api/v1")

"""
Query the health of the service.
"""


@api.route("/health")
def health():
    return jsonify({"status": "ok"})


"""
Sends all unreceived messages to a particular user
"""


@api.route("/messages/<pigeon_id>", methods=["GET"])
def pop_messages(pigeon_id):
    if not is_valid_uuid(pigeon_id):
        return bad_request("uuid")

    msgs = db.session.query(Message).filter_by(to_addr=pigeon_id)

    result = []
    for msg in msgs:
        result.append(msg.to_response())
        db.session.delete(msg)

    db.session.commit()

    return jsonify(result), 200


"""
Stores a message that is to be received
"""


@api.route("/messages/<pigeon_id>", methods=["POST"])
def push_message(pigeon_id):
    if not is_valid_uuid(pigeon_id):
        return bad_request("uuid")

    json = request.get_json(force=True)
    meta = json.get("meta")

    msg = Message(
        from_addr=meta.get("from"),
        to_addr=meta.get("to"),
        sent_at=meta.get("datetime"),
        message=json.get("message"),
    )
    return jsonify({"Nice": "Nice"}), 200
    db.session.add(msg)
    db.session.commit()
    return jsonify(msg.to_response()), 201


"""
Initial Message Confirmation for exchange of public key
"""


@api.route("/messages/<pigeon_id1>/request/<input>", methods=["POST"])
def push_message(pigeon_id1, input):
    if not is_valid_uuid(pigeon_id1):
        return bad_request("uuid")

    if input is "yes":

        generated_key_pair = generate_key_pair()

        account = Client_Info.query.get(pigeon_id1)
        if not account or account == []:

            client = Client_Info(
                pigeon_id=pigeon_id1,
                private_key=generated_key_pair[0],
                public_key=generated_key_pair[1],
            )

            db.session.add(client)
            db.session.commit()

        sender_public_key = generated_key_pair[1]

        return jsonify({"Successful Sender's Public Key is ": sender_public_key}), 201


"""
Defines bad request resposne
"""


def bad_request(msg=""):
    return jsonify({"Error:": "Bad request - " + msg}), 400


"""
Returns true iff valid uuid
"""


def is_valid_uuid(uuid):
    try:
        uuid_obj = UUID(uuid)
    except ValueError:
        return False
    return str(uuid_obj) == uuid
