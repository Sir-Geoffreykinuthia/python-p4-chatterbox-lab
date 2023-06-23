from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/messages', methods=['GET'])
def get_all_messages():
    all_messages = Message.query.order_by(Message.created_at.asc()).all()
    messages_data = [message.to_dict() for message in all_messages]
    return jsonify(messages_data)


@app.route('/messages', methods=['POST'])
def create_message():
    body = request.json.get('body')
    username = request.json.get('username')

    if not body or not username:
        return make_response(jsonify({'error': 'Missing required fields'}), 400)

    new_message = Message(body=body, username=username)
    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201


@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)
    if not message:
        return make_response(jsonify({'error': 'Message not found'}), 404)

    body = request.json.get('body')
    if body is not None:
        message.body = body
        db.session.commit()

    return jsonify(message.to_dict())


@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return make_response(jsonify({'error': 'Message not found'}), 404)

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'Message deleted'}), 204


if __name__ == '__main__':
    app.run(port=5555)